"""Fictional identities; no access to a user's live registry."""

from copy import deepcopy
import importlib.util
import json
import multiprocessing
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/multi-chat-orchestration/scripts/registry.py"
spec = importlib.util.spec_from_file_location("registry", SCRIPT)
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)


def entry(lead, issue, repo="example/app"):
    return {"lead": {"hostId": "local", "threadId": lead, "epoch": 1}, "issueTasks": [
        {"hostId": "local", "threadId": f"owner-{issue}", "provider": "github.com",
         "repository": repo, "issue": issue}]}


def concurrent_create(path, key, lead, issue, ready, start, results):
    ready.put(key)
    start.wait(10)
    try:
        registry.update(Path(path), key, ("local", lead), None, entry(lead, issue))
        results.put("ok")
    except ValueError as exc:
        results.put(str(exc))


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "registry.json"
        self.a, self.b = entry("lead-a", 12), entry("lead-b", 13)

    def seed(self):
        registry.update(self.path, "invocation:a", ("local", "lead-a"), None, self.a)
        registry.update(self.path, "invocation:b", ("local", "lead-b"), None, self.b)

    def test_same_repo_different_leads_and_one_invocation_multiple_repos(self):
        self.seed()
        next_a = deepcopy(self.a)
        next_a["issueTasks"] += entry("lead-a", 14, "example/other")["issueTasks"]
        registry.update(self.path, "invocation:a", ("local", "lead-a"), self.a, next_a)
        self.assertEqual(registry.resolve(self.path, "invocation:a", next_a["issueTasks"][1])["threadId"], "lead-a")
        self.assertEqual(registry.resolve(self.path, "invocation:b", self.b["issueTasks"][0])["threadId"], "lead-b")
        with self.assertRaisesRegex(ValueError, "Exact invocation"):
            registry.resolve(self.path, "invocation:b", self.a["issueTasks"][0])

    def test_foreign_actor_stale_expected_and_duplicate_ownership_leave_bytes_intact(self):
        self.seed()
        original = self.path.read_bytes()
        duplicate = deepcopy(self.a)
        duplicate["issueTasks"] += self.b["issueTasks"]
        for actor, expected, replacement in [
            (("local", "lead-b"), self.a, self.a),
            (("local", "lead-a"), None, self.a),
            (("local", "lead-a"), self.a, duplicate),
        ]:
            with self.subTest(actor=actor, expected=expected):
                with self.assertRaises(ValueError):
                    registry.update(self.path, "invocation:a", actor, expected, replacement)
                self.assertEqual(self.path.read_bytes(), original)

    def test_provider_alias_and_repository_case_do_not_allow_duplicate_issue(self):
        self.seed()
        duplicate = entry("lead-c", 12, "EXAMPLE/APP")
        duplicate["issueTasks"][0].update(threadId="other-owner", provider="github")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            registry.update(self.path, "invocation:c", ("local", "lead-c"), None, duplicate)

    def test_handoff_increments_only_its_epoch_and_blocks_old_lead(self):
        self.seed()
        next_a = deepcopy(self.a)
        next_a["lead"].update(threadId="lead-c", epoch=2)
        registry.update(self.path, "invocation:a", ("local", "lead-a"), self.a, next_a)
        self.assertEqual(registry.read(self.path)["outcomes"]["invocation:b"], self.b)
        self.assertEqual(registry.resolve(self.path, "invocation:a", self.a["issueTasks"][0])["epoch"], 2)
        with self.assertRaisesRegex(ValueError, "Only this invocation"):
            registry.update(self.path, "invocation:a", ("local", "lead-a"), next_a, next_a)

    def test_takeover_requires_explicit_mode_and_preserves_owners(self):
        self.seed()
        next_a = deepcopy(self.a)
        next_a["lead"].update(threadId="lead-c", epoch=2)
        with self.assertRaises(ValueError):
            registry.update(self.path, "invocation:a", ("local", "lead-c"), self.a, next_a)
        invalid = deepcopy(next_a)
        invalid["issueTasks"] = []
        with self.assertRaises(ValueError):
            registry.update(self.path, "invocation:a", ("local", "lead-c"), self.a, invalid, authorized_takeover=True)
        registry.update(self.path, "invocation:a", ("local", "lead-c"), self.a, next_a, authorized_takeover=True)

    def test_unknown_schema_and_lead_as_owner_fail_closed(self):
        self.path.write_text(json.dumps({"schemaVersion": 2, "outcomes": {}}))
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            registry.read(self.path)
        self.path.unlink()
        invalid = deepcopy(self.a)
        invalid["issueTasks"][0]["threadId"] = "lead-a"
        with self.assertRaisesRegex(ValueError, "lead cannot"):
            registry.update(self.path, "invocation:a", ("local", "lead-a"), None, invalid)

    def test_failed_publish_keeps_previous_registry_and_can_retry(self):
        self.seed()
        original = self.path.read_bytes()
        next_a = deepcopy(self.a)
        next_a["issueTasks"] = []
        with patch.object(registry.os, "replace", side_effect=OSError("injected interruption")):
            with self.assertRaises(OSError):
                registry.update(self.path, "invocation:a", ("local", "lead-a"), self.a, next_a)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(sorted(p.name for p in self.path.parent.iterdir()), ["registry.json", "registry.json.lock"])
        registry.update(self.path, "invocation:a", ("local", "lead-a"), self.a, next_a)
        registry.update(self.path, "invocation:a", ("local", "lead-a"), next_a, None)
        self.assertEqual(registry.read(self.path)["outcomes"], {"invocation:b": self.b})

    def test_concurrent_leads_preserve_both_invocations(self):
        self.run_concurrent(same_key=False)
        self.assertEqual(set(registry.read(self.path)["outcomes"]), {"invocation:a", "invocation:b"})

    def test_concurrent_same_invocation_one_wins_other_must_reconcile(self):
        self.run_concurrent(same_key=True)
        self.assertEqual(len(registry.read(self.path)["outcomes"]), 1)

    def run_concurrent(self, same_key):
        context = multiprocessing.get_context("spawn")
        ready, results, start = context.Queue(), context.Queue(), context.Event()
        jobs = [context.Process(target=concurrent_create, args=(
            str(self.path), "invocation:a" if same_key else f"invocation:{letter}",
            f"lead-{letter}", number, ready, start, results))
            for letter, number in (("a", 12), ("b", 13))]
        try:
            for job in jobs:
                job.start()
            for _ in jobs:
                ready.get(timeout=10)
            start.set()
            outcomes = [results.get(timeout=10) for _ in jobs]
            for job in jobs:
                job.join(timeout=10)
                self.assertEqual(job.exitcode, 0)
            self.assertEqual(outcomes.count("ok"), 1 if same_key else 2)
            if same_key:
                self.assertTrue(any("Binding changed" in result for result in outcomes))
        finally:
            for job in jobs:
                if job.is_alive():
                    job.terminate()
                    job.join(timeout=10)
            ready.close()
            results.close()
