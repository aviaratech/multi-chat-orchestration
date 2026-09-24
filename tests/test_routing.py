import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/multi-chat-orchestration/scripts/routing.py"
spec = importlib.util.spec_from_file_location("routing", SCRIPT)
routing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routing)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Path(self.temp.name) / "config.toml"

    def resolve_text(self, text, team="default"):
        self.config.write_text(text)
        return routing.resolve(self.config, team)

    def test_defaults_and_named_teams_keep_consequential_review_separate(self):
        defaults = routing.resolve()
        self.assertEqual(defaults["roles"]["owner"]["model"], "gpt-6-sol")
        self.assertEqual(defaults["roles"]["helper"]["model_reasoning_effort"], "high")
        product = routing.resolve(ROOT / "examples/config.toml", "product")
        research = routing.resolve(ROOT / "examples/config.toml", "research")
        self.assertEqual(product["roles"]["reviewer"]["model"], "gpt-6-sol")
        self.assertEqual(product["roles"]["consequential_reviewer"]["model"], "gpt-6-astra")
        self.assertEqual(research["roles"]["owner"]["model"], "gpt-6-astra")
        self.assertEqual(defaults, routing.resolve())

    def test_shared_then_team_override_and_explicit_profile_binding(self):
        result = self.resolve_text('''version=1
[roles.owner]
model="host-model-a"
model_reasoning_effort="medium"
[roles.reviewer]
agent_type="existing_reviewer"
[teams.product.roles.owner]
model="host-model-b"
model_reasoning_effort="high"
''', "product")
        self.assertEqual(result["roles"]["owner"]["model"], "host-model-b")
        self.assertEqual(result["roles"]["reviewer"]["agent_type"], "existing_reviewer")
        self.assertEqual(len(result["sources"]), 2)
        self.assertEqual(len(result["routing_sha256"]), 64)

    def test_invalid_or_unknown_fields_and_incomplete_model_override_fail(self):
        cases = [
            "version=2", "version=true", "roles=[]", "version=1\nsecret='not-a-setting'",
            "version=1\n[roles.enginer]\nmodel='x'", "version=1\n[roles.owner]\nmodel='x'",
            "version=1\n[roles.owner]\nmodel_reasoning_effort='typo'",
            "version=1\n[roles.owner]\nagent_type='bad-owner-role'",
            "version=1\n[teams.product]\nlead_thread='not-configuration'",
            "version=1\n[teams.unselected.roles.helper]\nunknown='must-fail-too'",
            "version=1\n[roles.helper]\nagent_type='../escape'", "invalid toml = [",
        ]
        for text in cases:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.resolve_text(text)
        with self.assertRaisesRegex(ValueError, "Unknown team"):
            routing.resolve(team="typo")

    def test_provenance_distinguishes_file_edits_from_effective_route_changes(self):
        text = 'version=1\n[roles.owner]\nmodel_reasoning_effort="high"'
        first = self.resolve_text(text)
        comment_only = self.resolve_text(text + '\n# explanatory comment\n')
        self.assertEqual(first["routing_sha256"], comment_only["routing_sha256"])
        self.assertNotEqual(first["sources"][1]["sha256"], comment_only["sources"][1]["sha256"])
        second = self.resolve_text('version=1\n[roles.owner]\nmodel_reasoning_effort="medium"')
        self.assertNotEqual(first["routing_sha256"], second["routing_sha256"])

    def test_cli_missing_explicit_file_fails_and_defaults_only_works(self):
        missing = subprocess.run([sys.executable, str(SCRIPT), "--config", str(self.config)],
                                 capture_output=True, text=True)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("Routing configuration error", missing.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--defaults-only"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"gpt-6-sol"', result.stdout)
