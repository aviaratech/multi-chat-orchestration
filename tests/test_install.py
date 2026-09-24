"""Exercise the public installer through its CLI in isolated target directories."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/multi-chat-orchestration"
SCRIPT = ROOT / "scripts/install.py"


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skills = Path(self.temp.name) / "skills with spaces"
        self.target = self.skills / SOURCE.name

    def run_installer(self, action="install", success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), action, "--skills-dir", str(self.skills)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        return result

    def test_clean_install_repeat_and_uninstall_preserve_neighbors(self):
        self.skills.mkdir()
        neighbor = self.skills / "another-skill"
        neighbor.write_text("user-owned")
        self.run_installer()
        self.assertEqual(self.target.resolve(), SOURCE.resolve())
        self.assertTrue((self.target / "SKILL.md").is_file())
        self.assertTrue((self.target / "scripts/registry.py").is_file())
        self.run_installer()
        self.run_installer("uninstall")
        self.run_installer("uninstall")
        self.assertFalse(self.target.is_symlink())
        self.assertEqual(neighbor.read_text(), "user-owned")

    def test_existing_file_directory_and_dangling_link_are_preserved(self):
        for kind in ("file", "directory", "dangling"):
            with self.subTest(kind=kind):
                self.skills.mkdir(exist_ok=True)
                if kind == "file":
                    self.target.write_text("private")
                elif kind == "directory":
                    self.target.mkdir()
                else:
                    self.target.symlink_to(self.skills / "missing")
                self.run_installer(success=False)
                self.run_installer("uninstall", success=False)
                if kind == "directory":
                    self.assertTrue(self.target.is_dir())
                    self.target.rmdir()
                else:
                    if kind == "file":
                        self.assertEqual(self.target.read_text(), "private")
                    else:
                        self.assertTrue(self.target.is_symlink())
                    self.target.unlink()

    def test_requires_explicit_target(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "install"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.skills.exists())

    def test_optional_profiles_preflight_collisions_and_uninstall_only_owned_links(self):
        agents = Path(self.temp.name) / "agents"
        agents.mkdir()
        collision = agents / "mco-reviewer.toml"
        collision.write_text("existing profile")
        args = [sys.executable, str(SCRIPT), "install", "--skills-dir", str(self.skills),
                "--agents-dir", str(agents)]
        result = subprocess.run(args, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.target.exists())
        self.assertFalse((agents / "mco-worker.toml").exists())
        self.assertEqual(collision.read_text(), "existing profile")
        collision.unlink()
        result = subprocess.run(args, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(collision.is_symlink())
        self.assertTrue((agents / "mco-worker.toml").is_symlink())
        args[2] = "uninstall"
        result = subprocess.run(args, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(collision.is_symlink())
        self.assertFalse(self.target.is_symlink())
