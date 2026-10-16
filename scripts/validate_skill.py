#!/usr/bin/env python3
"""Check repository packaging, skill frontmatter, and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.sync_shared_copies import copy_errors
SKILL_NAMES = ("interaction-risk-analysis", "person-deep-analysis")
REQUIRED_FILES = (
    "skills/interaction-risk-analysis/SKILL.md",
    "skills/interaction-risk-analysis/agents/openai.yaml",
    "skills/interaction-risk-analysis/modules/m1-needs-and-preferences.md",
    "skills/interaction-risk-analysis/modules/m2-self-cognition.md",
    "skills/interaction-risk-analysis/modules/m3-experience-and-development.md",
    "skills/interaction-risk-analysis/modules/m4-shadow-risk.md",
    "skills/interaction-risk-analysis/modules/m5-interaction-patterns.md",
    "skills/interaction-risk-analysis/dlc/fictional-character-analysis.md",
    "skills/interaction-risk-analysis/dlc/narrative-identity.md",
    "skills/interaction-risk-analysis/dlc/relationship-dynamics.md",
    "skills/interaction-risk-analysis/references/methodology-and-limitations.md",
    "skills/interaction-risk-analysis/references/interaction-decomposition.md",
    "skills/interaction-risk-analysis/references/attachment-styles.md",
    "skills/interaction-risk-analysis/references/axioms.md",
    "skills/interaction-risk-analysis/references/signal-mapping.md",
    "skills/interaction-risk-analysis/references/reasoning-with-the-user.md",
    "skills/interaction-risk-analysis/references/scams-and-social-engineering.md",
    "skills/interaction-risk-analysis/references/relationship-coercion.md",
    "skills/interaction-risk-analysis/references/workplace-and-social-bullying.md",
    "skills/interaction-risk-analysis/references/safety-and-agency.md",
    "skills/interaction-risk-analysis/references/fraud-and-coercive-control-support.md",
    "skills/interaction-risk-analysis/references/safety-boundaries.md",
    "skills/interaction-risk-analysis/references/perspectives/cbt-descriptive.md",
    "skills/interaction-risk-analysis/references/perspectives/dark-triad-behavioral-screening.md",
    "skills/interaction-risk-analysis/references/perspectives/developmental-psychology.md",
    "skills/interaction-risk-analysis/references/perspectives/forensic-evidence-boundaries.md",
    "skills/interaction-risk-analysis/references/perspectives/humanistic-and-needs.md",
    "skills/interaction-risk-analysis/references/perspectives/psychodynamic.md",
    "skills/interaction-risk-analysis/references/perspectives/steelman-report.md",
    "skills/person-deep-analysis/SKILL.md",
    "skills/person-deep-analysis/agents/openai.yaml",
    "skills/person-deep-analysis/modules/m1-needs-and-preferences.md",
    "skills/person-deep-analysis/modules/m2-self-cognition.md",
    "skills/person-deep-analysis/modules/m3-experience-and-development.md",
    "skills/person-deep-analysis/modules/m4-shadow-risk.md",
    "skills/person-deep-analysis/modules/m5-interaction-patterns.md",
    "skills/person-deep-analysis/dlc/fictional-character-analysis.md",
    "skills/person-deep-analysis/dlc/narrative-identity.md",
    "skills/person-deep-analysis/dlc/relationship-dynamics.md",
    "skills/person-deep-analysis/references/methodology-and-limitations.md",
    "skills/person-deep-analysis/references/attachment-styles.md",
    "skills/person-deep-analysis/references/axioms.md",
    "skills/person-deep-analysis/references/signal-mapping.md",
    "skills/person-deep-analysis/references/fraud-and-coercive-control-support.md",
    "skills/person-deep-analysis/references/safety-boundaries.md",
    "skills/person-deep-analysis/references/perspectives/cbt-descriptive.md",
    "skills/person-deep-analysis/references/perspectives/dark-triad-behavioral-screening.md",
    "skills/person-deep-analysis/references/perspectives/developmental-psychology.md",
    "skills/person-deep-analysis/references/perspectives/forensic-evidence-boundaries.md",
    "skills/person-deep-analysis/references/perspectives/humanistic-and-needs.md",
    "skills/person-deep-analysis/references/perspectives/psychodynamic.md",
    "skills/person-deep-analysis/references/perspectives/steelman-report.md",
    "docs/research/multilens-psychology-evidence.md",
    "docs/research/multilens-design-review.md",
    "docs/research/network-evaluation-sources.md",
    "docs/research/fraud-and-coercive-control-guidance.md",
    "docs/launch/blog-project-module.md",
    "docs/demos/README.md",
    "docs/demos/01-romance-investment.md",
    "docs/demos/02-task-deposit.md",
    "docs/demos/03-emotional-blackmail.md",
    "docs/demos/04-emotional-abuse-and-control.md",
    "docs/demos/05-peer-bullying.md",
    "docs/demos/06-workplace-bullying.md",
    "docs/demos/07-single-memory-conflict.md",
    "docs/demos/08-counterevidence-update.md",
    "README.md",
    "README.zh-CN.md",
    "shared/README.md",
    "shared/manifest.json",
    "CONTRIBUTING.md",
    "LICENSE",
    "docs/launch/README.md",
    "docs/launch/content-kit.md",
    "docs/research/github-comparable-projects.md",
    "docs/research/interaction-risk-skills-landscape.md",
    "docs/research/demo-scenario-sources.md",
    "evals/README.md",
    "evals/behavior-regression.md",
    "evals/safety-scenarios.json",
    "evals/safety-regression.md",
    "evals/interaction-risk-cases.json",
    "evals/interaction-risk-acceptance.md",
    "evals/results/2026-09-25-person-analysis-anti-fraud-acceptance.md",
    "evals/results/2026-09-25-decomposition-method-evaluation.md",
    "evals/results/2026-09-25-public-safety-skill-forward-test.md",
    "evals/results/2026-09-24-network-example-ab-pilot.md",
    "evals/results/2026-09-25-scope-expansion-smoke.md",
    "evals/results/2026-09-24-fraud-agency-forward-test.md",
    "evals/scenarios.json",
    "evals/cases/case-single-dating.md",
    "evals/cases/case-couple-conflict.md",
    ".github/workflows/validate.yml",
    "scripts/check_skill_discovery.py",
    "scripts/check_skill_installation.py",
    "scripts/validate_skill.py",
    "scripts/sync_shared_copies.py",
    "scripts/validate_safety_evals.py",
    "scripts/validate_interaction_risk_evals.py",
    "scripts/validate_evals.py",
)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
PACKAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|(?<!!)\[[^\]]*\]\(([^)]+)\)")
RUNTIME_REF_RE = re.compile(r"`((?:references|modules|dlc)/[^`\s]+)`")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
H2_RE = re.compile(r"^## ", re.MULTILINE)
CJK_RE = re.compile(r"[\u3400-\u9fff]")
NEIGHBORS = {
    "interaction-risk-analysis": "person-deep-analysis",
    "person-deep-analysis": "interaction-risk-analysis",
}


def check_frontmatter(skill_name: str, errors: list[str], root: Path = REPO_ROOT) -> None:
    skill_file = root / "skills" / skill_name / "SKILL.md"
    if not skill_file.is_file():
        return
    content = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        errors.append(f"skills/{skill_name}/SKILL.md: missing YAML frontmatter")
        return
    fields = match.group(1)
    name_match = re.search(
        r"""^name:[ \t]*(?:'([^'\n]+)'|"([^"\n]+)"|([^\s#]+))[ \t]*$""",
        fields,
        flags=re.MULTILINE,
    )
    for field in ("name", "description"):
        if not re.search(rf"^{field}:\s*\S", fields, flags=re.MULTILINE):
            errors.append(f"skills/{skill_name}/SKILL.md: frontmatter is missing a non-empty {field!r} field")
    if name_match:
        name = next(value for value in name_match.groups() if value is not None)
        if name != skill_name:
            errors.append(f"skills/{skill_name}/SKILL.md name {name!r} does not match directory {skill_name!r}")
    description_match = re.search(
        r"^description:\s*>-?\s*\n((?:[ \t].*\n?)+)", fields, flags=re.MULTILINE
    )
    if description_match and len(description_match.group(1).strip()) > 1024:
        errors.append(f"skills/{skill_name}/SKILL.md: frontmatter description exceeds 1024 characters")
    if description_match and not description_match.group(1).lstrip().startswith("Use when"):
        errors.append(f"skills/{skill_name}/SKILL.md: description should begin with a clear usage trigger ('Use when')")
    if not re.search(r"^license:\s*MIT\s*$", fields, flags=re.MULTILINE):
        errors.append(f"skills/{skill_name}/SKILL.md: frontmatter must include 'license: MIT'")
    neighbor = NEIGHBORS.get(skill_name)
    description_text = description_match.group(1) if description_match else ""
    if neighbor and not re.search(
        r"(?<![A-Za-z0-9-])" + re.escape(neighbor) + r"(?![A-Za-z0-9-])",
        description_text,
    ):
        errors.append(
            f"skills/{skill_name}/SKILL.md: description must name the neighboring skill {neighbor}"
        )


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (REPO_ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_no_root_skill(errors: list[str]) -> None:
    if (REPO_ROOT / "SKILL.md").exists():
        errors.append("repository root must not contain SKILL.md; installable skill belongs under skills/")


def check_installable_skills(errors: list[str]) -> None:
    found = {path.name for path in (REPO_ROOT / "skills").iterdir() if path.is_dir()}
    expected = set(SKILL_NAMES)
    if found != expected:
        errors.append(f"expected exactly these installable skills {sorted(expected)}, found {sorted(found)}")


def check_runtime_references(errors: list[str]) -> None:
    for skill_name in SKILL_NAMES:
        skill_root = (REPO_ROOT / "skills" / skill_name).resolve()
        if not skill_root.is_dir():
            continue
        for source in skill_root.rglob("*.md"):
            for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
                for match in RUNTIME_REF_RE.finditer(line):
                    reference = match.group(1)
                    target = (skill_root / reference).resolve()
                    location = f"skills/{skill_name}/{source.relative_to(skill_root)}:{line_number}"
                    if not target.is_relative_to(skill_root):
                        errors.append(f"{location}: runtime reference escapes skill directory: {reference}")
                    elif not target.is_file():
                        errors.append(f"{location}: runtime reference target not found: {reference}")


def check_markdown_links(errors: list[str]) -> None:
    for source in REPO_ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in source.relative_to(REPO_ROOT).parts):
            continue
        for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            for match in LINK_RE.finditer(line):
                target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("//") or target.startswith("#"):
                    continue
                path = unquote(parsed.path)
                if not path:
                    continue
                resolved = (source.parent / path).resolve()
                if not resolved.exists():
                    relative = source.relative_to(REPO_ROOT)
                    errors.append(f"{relative}:{line_number}: local link target not found: {path}")


def local_link_target(target: str) -> str | None:
    cleaned = target.strip().split(maxsplit=1)[0].strip("<>")
    parsed = urlparse(cleaned)
    if parsed.scheme or cleaned.startswith("//") or cleaned.startswith("#"):
        return None
    return unquote(parsed.path) or None


def check_package_links(errors: list[str], root: Path = REPO_ROOT) -> None:
    """Fail when a skill package links to a file outside its own directory."""
    for skill_name in SKILL_NAMES:
        skill_dir = (root / "skills" / skill_name).resolve()
        if not skill_dir.is_dir():
            continue
        for source in sorted(skill_dir.rglob("*")):
            if source.is_symlink():
                errors.append(
                    f"{source.relative_to(root)}: symlink is not allowed inside an installable skill package"
                )
                continue
            if source.suffix != ".md" or not source.is_file():
                continue
            relative = source.relative_to(root)
            for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
                for match in PACKAGE_LINK_RE.finditer(line):
                    local_path = local_link_target(match.group(1) or match.group(2))
                    if local_path is None:
                        continue
                    resolved = (source.parent / local_path).resolve()
                    try:
                        resolved.relative_to(skill_dir)
                    except ValueError:
                        errors.append(
                            f"{relative}:{line_number}: link points outside the skill package: {local_path}"
                        )


def check_readme_editions(errors: list[str], root: Path = REPO_ROOT) -> None:
    """Require an English default README and a Chinese twin with the same sections."""
    english = root / "README.md"
    chinese = root / "README.zh-CN.md"
    texts: dict[str, str] = {}
    for path in (english, chinese):
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(root)}")
            continue
        texts[path.name] = path.read_text(encoding="utf-8")
    if "README.md" in texts and not texts["README.md"].startswith("[Chinese](README.zh-CN.md)"):
        errors.append("README.md: first line must link to README.zh-CN.md")
    if "README.zh-CN.md" in texts and not texts["README.zh-CN.md"].startswith("[英文](README.md)"):
        errors.append("README.zh-CN.md: first line must link to README.md")
    if "README.md" in texts and CJK_RE.search(texts["README.md"]):
        errors.append("README.md: English edition must not contain Chinese characters")
    if "README.zh-CN.md" in texts and not CJK_RE.search(texts["README.zh-CN.md"]):
        errors.append("README.zh-CN.md: Chinese edition must contain Chinese characters")
    if len(texts) == 2:
        english_sections = len(H2_RE.findall(texts["README.md"]))
        chinese_sections = len(H2_RE.findall(texts["README.zh-CN.md"]))
        if english_sections != chinese_sections:
            errors.append(
                "README section count differs: "
                f"README.md has {english_sections} level-2 headings, "
                f"README.zh-CN.md has {chinese_sections}"
            )
        check_use_instead_column(errors, texts["README.md"], "Use instead", "README.md")
        check_use_instead_column(errors, texts["README.zh-CN.md"], "改用", "README.zh-CN.md")


def markdown_tables(text: str) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].startswith("|") and index + 1 < len(lines) and re.match(r"^\|\s*-+", lines[index + 1]):
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            tables.append(rows)
        else:
            index += 1
    return tables


def check_use_instead_column(errors: list[str], text: str, header_name: str, filename: str) -> None:
    matched = False
    for rows in markdown_tables(text):
        if not rows or header_name not in rows[0]:
            continue
        matched = True
        try:
            column = rows[0].index(header_name)
        except ValueError:
            errors.append(f"{filename}: {header_name} column is not a table header cell")
            continue
        for row in rows[2:]:
            if not row or column >= len(row):
                errors.append(f"{filename}: skill table row is missing the {header_name} column")
                continue
            present = [name for name in SKILL_NAMES if name in row[0]]
            if len(present) != 1:
                continue
            other = NEIGHBORS[present[0]]
            if other not in row[column]:
                errors.append(f"{filename}: {header_name} cell for {present[0]} must name {other}")
            if filename == "README.md" and CJK_RE.search(row[column]):
                errors.append(f"{filename}: {header_name} cell for {present[0]} must stay in English")
    if not matched:
        errors.append(f"{filename}: skill table must include a {header_name} column")


def check_shared_copies(errors: list[str], root: Path = REPO_ROOT) -> None:
    errors.extend(copy_errors(root))


def collect_errors(root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    if root == REPO_ROOT:
        check_required_files(errors)
        for skill_name in SKILL_NAMES:
            check_frontmatter(skill_name, errors)
        check_no_root_skill(errors)
        check_installable_skills(errors)
        check_runtime_references(errors)
        check_markdown_links(errors)
    check_package_links(errors, root)
    check_readme_editions(errors, root)
    check_shared_copies(errors, root)
    return errors


def main() -> int:
    errors = collect_errors()
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Repository validation passed "
        "(package files, frontmatter, neighboring skills, licenses, "
        "in-package links, shared copies, local Markdown links, "
        "English and Chinese READMEs)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
