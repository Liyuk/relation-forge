import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync_shared_copies.py"


class SharedCopyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shared = self.root / "shared"
        common = shared / "common"
        common.mkdir(parents=True)
        (common / "note.md").write_text("shared note\n", encoding="utf-8")
        (self.root / "LICENSE").write_text("mit\n", encoding="utf-8")
        for name in ("interaction-risk-analysis", "person-deep-analysis"):
            (self.root / "skills" / name).mkdir(parents=True)
        manifest = {
            "files": [{
                "source": "LICENSE",
                "destinations": [
                    "skills/interaction-risk-analysis/LICENSE",
                    "skills/person-deep-analysis/LICENSE",
                ],
            }],
            "trees": [{
                "source": "shared/common",
                "destinations": [
                    "skills/interaction-risk-analysis",
                    "skills/person-deep-analysis",
                ],
            }],
        }
        (shared / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def module(self):
        spec = importlib.util.spec_from_file_location("sync_shared_copies", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_write_then_check_passes(self):
        module = self.module()
        written = module.write_copies(self.root)
        self.assertEqual(
            [
                "skills/interaction-risk-analysis/LICENSE",
                "skills/person-deep-analysis/LICENSE",
                "skills/interaction-risk-analysis/note.md",
                "skills/person-deep-analysis/note.md",
            ],
            written,
        )
        self.assertEqual([], module.copy_errors(self.root))

    def test_drift_is_reported(self):
        module = self.module()
        module.write_copies(self.root)
        (self.root / "skills/person-deep-analysis/note.md").write_text("edited copy\n", encoding="utf-8")
        errors = module.copy_errors(self.root)
        self.assertTrue(any("differs from shared/common/note.md" in error for error in errors))

    def test_identical_unlisted_file_is_reported(self):
        module = self.module()
        module.write_copies(self.root)
        for name in ("interaction-risk-analysis", "person-deep-analysis"):
            (self.root / "skills" / name / "extra.md").write_text("same\n", encoding="utf-8")
        errors = module.copy_errors(self.root)
        self.assertTrue(any("extra.md" in error and "not listed" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
