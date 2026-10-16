import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_skill.py"
ROOT = SCRIPT.parents[1]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_skill", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_current_repository_passes(self):
        self.assertEqual(self.validator.collect_errors(ROOT), [])

    def test_reports_readme_section_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[Chinese](README.zh-CN.md)\n\n## One\n", encoding="utf-8")
            (root / "README.zh-CN.md").write_text("[英文](README.md)\n\n## 一\n\n## 二\n", encoding="utf-8")
            errors: list[str] = []
            self.validator.check_readme_editions(errors, root)
        self.assertTrue(any("section count differs" in error for error in errors))

    def test_reports_chinese_in_english_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[Chinese](README.zh-CN.md)\n\n中文\n", encoding="utf-8")
            (root / "README.zh-CN.md").write_text("[英文](README.md)\n\n中文\n", encoding="utf-8")
            errors: list[str] = []
            self.validator.check_readme_editions(errors, root)
        self.assertTrue(any("must not contain Chinese" in error for error in errors))

    def test_reports_link_outside_skill_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "interaction-risk-analysis"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("See [outside](../../README.md).\n", encoding="utf-8")
            (root / "README.md").write_text("readme\n", encoding="utf-8")
            errors: list[str] = []
            self.validator.check_package_links(errors, root)
        self.assertEqual(len(errors), 1)
        self.assertIn("link points outside the skill package", errors[0])
        self.assertIn("../../README.md", errors[0])

    def test_reports_missing_neighbor_in_description(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "person-deep-analysis"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: person-deep-analysis\n"
                "description: >-\n  Use when reading a profile. Escalate concrete risks to risk-focused guidance.\n"
                "license: MIT\n---\n# Example\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            self.validator.check_frontmatter("person-deep-analysis", errors, root)
        self.assertTrue(any("must name the neighboring skill interaction-risk-analysis" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
