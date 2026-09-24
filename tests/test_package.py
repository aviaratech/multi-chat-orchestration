import json
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_manifest_and_profiles_are_parseable_and_resolve(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        portable = json.loads((ROOT / "plugin.json").read_text())
        for key in ("name", "version", "license", "repository"):
            self.assertEqual(portable[key], manifest[key])
        self.assertEqual(manifest["name"], ROOT.name)
        self.assertEqual(manifest["license"], "MIT")
        skill_root = ROOT / manifest["skills"] / manifest["name"]
        self.assertTrue((skill_root / "SKILL.md").is_file())
        for path in (ROOT / "examples/agents").glob("*.toml"):
            with self.subTest(path=path.name):
                profile = tomllib.loads(path.read_text())
                self.assertTrue(profile["name"])
                self.assertTrue(profile["developer_instructions"])
                self.assertNotIn("model", profile)
                self.assertNotIn("model_reasoning_effort", profile)
        reviewer = tomllib.loads((ROOT / "examples/agents/mco-reviewer.toml").read_text())
        self.assertEqual(reviewer["sandbox_mode"], "read-only")

    def test_relative_markdown_links_resolve_within_package(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#")[0]).resolve()
                with self.subTest(source=str(path.relative_to(ROOT)), link=link):
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.exists())
