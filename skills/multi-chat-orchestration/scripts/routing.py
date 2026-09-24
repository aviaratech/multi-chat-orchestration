#!/usr/bin/env python3
"""Resolve non-secret team routing without changing Codex or live task settings."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import tomllib

DEFAULTS = Path(__file__).resolve().parents[1] / "config/defaults.toml"
ROLES = {"lead", "owner", "helper", "reviewer", "consequential_owner", "consequential_reviewer"}
CHILD_ROLES = {"helper", "reviewer", "consequential_reviewer"}
EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"}
IDENTIFIER = re.compile(r"[a-zA-Z_][a-zA-Z0-9_-]*\Z")


def read_toml(path: Path) -> tuple[dict, dict]:
    data = path.read_bytes()
    try:
        value = tomllib.loads(data.decode("utf-8"))
    except (UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"Invalid TOML in {path}: {exc}") from exc
    return value, {"path": str(path.resolve()), "sha256": hashlib.sha256(data).hexdigest()}


def overlay_roles(target: dict, overlay: object, label: str) -> None:
    if not isinstance(overlay, dict) or set(overlay) - ROLES:
        raise ValueError(f"{label}: expected known role tables: {', '.join(sorted(ROLES))}")
    for role, values in overlay.items():
        allowed = {"model", "model_reasoning_effort"} | ({"agent_type"} if role in CHILD_ROLES else set())
        if not isinstance(values, dict) or set(values) - allowed:
            raise ValueError(f"{label}.{role}: unknown fields; allowed: {', '.join(sorted(allowed))}")
        if "model" in values and "model_reasoning_effort" not in values:
            raise ValueError(f"{label}.{role}: set model_reasoning_effort explicitly with model")
        for key, value in values.items():
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError(f"{label}.{role}.{key}: expected a nonempty trimmed string")
            if key == "model_reasoning_effort" and value not in EFFORTS:
                raise ValueError(f"{label}.{role}: unknown model_reasoning_effort")
            if key == "model" and any(character.isspace() for character in value):
                raise ValueError(f"{label}.{role}: model identifier must not contain whitespace")
            if key == "agent_type" and not IDENTIFIER.fullmatch(value):
                raise ValueError(f"{label}.{role}: invalid agent_type identifier")
        target[role].update(values)


def resolve(config_path: Path | None = None, team: str = "default") -> dict:
    defaults, provenance = read_toml(DEFAULTS)
    roles = {role: {} for role in ROLES}
    overlay_roles(roles, defaults["roles"], "defaults.roles")
    sources = [provenance]
    config = {"version": 1}
    if config_path is not None:
        config, provenance = read_toml(config_path.expanduser())
        sources.append(provenance)
    if set(config) - {"version", "roles", "teams"}:
        raise ValueError("Config accepts only version, roles, and teams")
    if type(config.get("version")) is not int or config["version"] != 1:
        raise ValueError("Config version must be 1")
    overlay_roles(roles, config.get("roles", {}), "roles")
    teams = config.get("teams", {})
    if not isinstance(teams, dict):
        raise ValueError("teams must contain named team tables")
    for name, definition in teams.items():
        if not IDENTIFIER.fullmatch(name) or not isinstance(definition, dict) or set(definition) != {"roles"}:
            raise ValueError("Each named team must contain only a roles table")
        # Validate every team, including unselected teams; typos never disappear.
        overlay_roles(deepcopy(roles), definition["roles"], f"teams.{name}.roles")
    if team != "default" and team not in teams:
        raise ValueError(f"Unknown team {team!r}; configure it explicitly")
    if team in teams:
        overlay_roles(roles, teams[team]["roles"], f"teams.{team}.roles")
    effective = {"version": 1, "team": team, "roles": roles}
    fingerprint = hashlib.sha256(json.dumps(effective, sort_keys=True).encode()).hexdigest()
    return {**effective, "routing_sha256": fingerprint, "sources": sources}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--config", type=Path, help="Selected override file; replaces user-file selection")
    source.add_argument("--defaults-only", action="store_true")
    parser.add_argument("--team", default="default")
    args = parser.parse_args()
    try:
        selected = args.config
        if selected is None and not args.defaults_only:
            user_file = Path.home() / ".codex/multi-chat-orchestration/config.toml"
            if user_file.exists() or user_file.is_symlink():
                selected = user_file
        print(json.dumps(resolve(selected, args.team), indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Routing configuration error: {exc}\n")


if __name__ == "__main__":
    main()
