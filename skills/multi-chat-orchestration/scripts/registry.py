#!/usr/bin/env python3
"""Local invocation registry: locked compare-and-swap updates and exact routing.

This checks supplied identities; it does not authenticate the tool caller.
All writers must use this helper and the same local registry/lock paths.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import tempfile


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def provider_key(value: str) -> str:
    # Legacy local registries used both spellings; they are one issue namespace.
    return "github.com" if value == "github" else value


def validate(registry: object) -> None:
    if not isinstance(registry, dict) or set(registry) != {"schemaVersion", "outcomes"}:
        raise ValueError("Invalid registry fields")
    if type(registry["schemaVersion"]) is not int or registry["schemaVersion"] != 1:
        raise ValueError("Unsupported registry schema")
    outcomes = registry["outcomes"]
    if not isinstance(outcomes, dict):
        raise ValueError("outcomes must be an object")
    issues, tasks, leads = set(), set(), set()
    for key, entry in outcomes.items():
        if not nonempty(key) or not isinstance(entry, dict) or set(entry) != {"lead", "issueTasks"}:
            raise ValueError("Invalid invocation entry")
        lead = entry["lead"]
        if not isinstance(lead, dict) or set(lead) != {"hostId", "threadId", "epoch"}:
            raise ValueError("Invalid lead fields")
        if not all(nonempty(lead[k]) for k in ("hostId", "threadId")):
            raise ValueError("Missing lead identity")
        if type(lead["epoch"]) is not int or lead["epoch"] < 1:
            raise ValueError("Invalid lead epoch")
        leads.add((lead["hostId"], lead["threadId"]))
        if not isinstance(entry["issueTasks"], list):
            raise ValueError("issueTasks must be an array")
        for owner in entry["issueTasks"]:
            fields = {"hostId", "threadId", "provider", "repository", "issue"}
            if not isinstance(owner, dict) or set(owner) != fields:
                raise ValueError("Invalid issue owner fields")
            if not all(nonempty(owner[k]) for k in fields - {"issue"}):
                raise ValueError("Missing issue owner identity")
            if type(owner["issue"]) is not int or owner["issue"] < 1:
                raise ValueError("Invalid issue number")
            issue = (provider_key(owner["provider"]), owner["repository"].lower(), owner["issue"])
            task = (owner["hostId"], owner["threadId"])
            if issue in issues or task in tasks:
                raise ValueError("Duplicate issue or task ownership across invocations")
            issues.add(issue)
            tasks.add(task)
    if leads & tasks:
        raise ValueError("A lead cannot also be a registered issue owner")


def read(registry_path: Path) -> dict:
    if registry_path.is_symlink():
        raise ValueError("Registry must not be a symlink")
    if registry_path.exists():
        registry = json.loads(registry_path.read_text())
    else:
        registry = {"schemaVersion": 1, "outcomes": {}}
    validate(registry)
    return registry


def update(registry_path: Path, outcome: str, actor: tuple[str, str],
           expected: dict | None, replacement: dict | None, *,
           authorized_takeover: bool = False) -> dict:
    """Mutate only one invocation if its exact prior entry still matches."""
    if not nonempty(outcome):
        raise ValueError("Missing invocation key")
    registry_path = registry_path.expanduser().absolute()
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = registry_path.with_name(registry_path.name + ".lock")
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        registry = read(registry_path)
        current = registry["outcomes"].get(outcome)
        if current != expected:
            raise ValueError("Binding changed; re-read and reconcile before retrying")
        if current is None:
            if replacement is None:
                raise ValueError("Cannot delete an absent invocation")
            authority = replacement.get("lead", {})
            if authority.get("epoch") != 1:
                raise ValueError("New invocation must start at epoch 1")
        else:
            authority = current["lead"]
        if authorized_takeover:
            if current is None or replacement is None:
                raise ValueError("Takeover requires an existing invocation and replacement lead")
            validate({"schemaVersion": 1, "outcomes": {outcome: replacement}})
            incoming = replacement["lead"]
            if actor != (incoming["hostId"], incoming["threadId"]):
                raise ValueError("Authorized takeover actor must be the incoming lead")
            if actor == (authority["hostId"], authority["threadId"]):
                raise ValueError("Takeover must change the lead")
            if replacement["issueTasks"] != current["issueTasks"]:
                raise ValueError("Takeover cannot alter issue ownership")
        elif actor != (authority.get("hostId"), authority.get("threadId")):
            raise ValueError("Only this invocation's bound lead may update it")
        if replacement is None:
            if current["issueTasks"]:
                raise ValueError("Remove accepted terminal owners before retiring invocation")
            del registry["outcomes"][outcome]
        else:
            candidate = {"schemaVersion": 1, "outcomes": {outcome: replacement}}
            validate(candidate)
            if current:
                old, new = current["lead"], replacement["lead"]
                changed_lead = (old["hostId"], old["threadId"]) != (new["hostId"], new["threadId"])
                if new["epoch"] != old["epoch"] + int(changed_lead):
                    raise ValueError("Handoff must increment epoch once; other edits preserve it")
            registry["outcomes"][outcome] = replacement
        validate(registry)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=registry_path.parent,
                                             prefix=registry_path.name + ".", delete=False) as handle:
                temporary = Path(handle.name)
                json.dump(registry, handle, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, registry_path)
            # Flush the rename as well as the file before confirming completion.
            directory_fd = os.open(registry_path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            if read(registry_path) != registry:
                raise ValueError("Registry readback mismatch")
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return registry


def resolve(registry_path: Path, outcome: str, owner: dict) -> dict:
    registry = read(registry_path)
    entry = registry["outcomes"].get(outcome)
    if entry is None or owner not in entry["issueTasks"]:
        raise ValueError("Exact invocation and registered source identity required; do not send")
    return {"outcomeKey": outcome, **entry["lead"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show")
    show.add_argument("--outcome", required=True)
    change = commands.add_parser("update")
    change.add_argument("--outcome", required=True)
    change.add_argument("--actor-host", required=True)
    change.add_argument("--actor-thread", required=True)
    change.add_argument("--expected", required=True, type=Path, help="JSON prior entry, or null")
    change.add_argument("--replacement", required=True, type=Path, help="JSON next entry, or null")
    change.add_argument("--authorized-takeover", action="store_true",
                        help="Incoming lead only; requires separately verified operator approval")
    route = commands.add_parser("resolve")
    route.add_argument("--outcome", required=True)
    route.add_argument("--source-host", required=True)
    route.add_argument("--source-thread", required=True)
    route.add_argument("--provider", required=True)
    route.add_argument("--repository", required=True)
    route.add_argument("--issue", required=True, type=int)
    args = parser.parse_args()
    try:
        path = args.registry.expanduser().absolute()
        if args.command == "show":
            registry = read(path)
            if args.outcome not in registry["outcomes"]:
                raise ValueError("Unknown invocation")
            result = registry["outcomes"][args.outcome]
        elif args.command == "update":
            update(path, args.outcome, (args.actor_host, args.actor_thread),
                   json.loads(args.expected.read_text()), json.loads(args.replacement.read_text()),
                   authorized_takeover=args.authorized_takeover)
            result = {"updated": args.outcome}
        else:
            result = resolve(path, args.outcome, {
                "hostId": args.source_host, "threadId": args.source_thread,
                "provider": args.provider, "repository": args.repository, "issue": args.issue,
            })
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
