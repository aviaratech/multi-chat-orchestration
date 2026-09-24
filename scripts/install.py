#!/usr/bin/env python3
"""Install one skill symlink without replacing user-owned paths."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

SKILL_NAME = "multi-chat-orchestration"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / SKILL_NAME


def install(skills_dir: Path, *, agents_dir: Path | None = None, remove: bool = False) -> str:
    sources = [(SOURCE.resolve(strict=True), skills_dir.expanduser().absolute() / SKILL_NAME)]
    if not (sources[0][0] / "SKILL.md").is_file():
        raise ValueError(f"Missing skill: {SOURCE}")
    if agents_dir is not None:
        for name in ("mco-worker.toml", "mco-reviewer.toml"):
            source = Path(__file__).resolve().parents[1] / "examples/agents" / name
            sources.append((source.resolve(strict=True), agents_dir.expanduser().absolute() / name))
    # Preflight every target before changing any link.
    for source, target in sources:
        if target.is_symlink():
            if target.resolve() != source:
                raise ValueError(f"Refusing to replace foreign symlink: {target}")
        elif target.exists():
            raise ValueError(f"Refusing to replace existing path: {target}")
    results = []
    for source, target in sources:
        if remove:
            if target.is_symlink():
                target.unlink()
            results.append(f"Absent: {target}")
        elif target.is_symlink():
            results.append(f"Already installed: {target}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            # Atomic creation also refuses a path created after preflight.
            os.symlink(source, target, target_is_directory=source.is_dir())
            results.append(f"Installed {target} -> {source}")
    return "\n".join(results)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall"))
    parser.add_argument("--skills-dir", required=True, type=Path)
    parser.add_argument("--agents-dir", type=Path, help="Explicitly opt in to the two model-neutral native profiles")
    args = parser.parse_args()
    try:
        print(install(args.skills_dir, agents_dir=args.agents_dir, remove=args.action == "uninstall"))
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
