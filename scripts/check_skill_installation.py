#!/usr/bin/env python3
"""Install from this repository into temporary Codex and Claude Code projects."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_SOURCE = REPO_ROOT
SKILLS_CLI_VERSION = "1.7.0"
TIMEOUT_SECONDS = 120
REQUIRED_RUNTIME_FILES = {
    "interaction-risk-analysis": (
        "SKILL.md",
        "LICENSE",
        "agents/openai.yaml",
        "modules/m1-needs-and-preferences.md",
        "modules/m2-self-cognition.md",
        "modules/m3-experience-and-development.md",
        "modules/m4-shadow-risk.md",
        "modules/m5-interaction-patterns.md",
        "dlc/fictional-character-analysis.md",
        "dlc/narrative-identity.md",
        "dlc/relationship-dynamics.md",
        "references/interaction-decomposition.md",
        "references/methodology-and-limitations.md",
        "references/attachment-styles.md",
        "references/axioms.md",
        "references/signal-mapping.md",
        "references/reasoning-with-the-user.md",
        "references/scams-and-social-engineering.md",
        "references/relationship-coercion.md",
        "references/workplace-and-social-bullying.md",
        "references/safety-and-agency.md",
        "references/fraud-and-coercive-control-support.md",
        "references/safety-boundaries.md",
        "references/perspectives/cbt-descriptive.md",
        "references/perspectives/dark-triad-behavioral-screening.md",
        "references/perspectives/developmental-psychology.md",
        "references/perspectives/forensic-evidence-boundaries.md",
        "references/perspectives/humanistic-and-needs.md",
        "references/perspectives/psychodynamic.md",
        "references/perspectives/steelman-report.md",
    ),
    "person-deep-analysis": (
        "SKILL.md",
        "LICENSE",
        "agents/openai.yaml",
        "modules/m1-needs-and-preferences.md",
        "modules/m2-self-cognition.md",
        "modules/m3-experience-and-development.md",
        "modules/m4-shadow-risk.md",
        "modules/m5-interaction-patterns.md",
        "references/methodology-and-limitations.md",
        "references/axioms.md",
        "references/signal-mapping.md",
        "references/fraud-and-coercive-control-support.md",
        "references/safety-boundaries.md",
        "references/attachment-styles.md",
        "references/perspectives/cbt-descriptive.md",
        "references/perspectives/dark-triad-behavioral-screening.md",
        "references/perspectives/developmental-psychology.md",
        "references/perspectives/forensic-evidence-boundaries.md",
        "references/perspectives/humanistic-and-needs.md",
        "references/perspectives/psychodynamic.md",
        "references/perspectives/steelman-report.md",
        "dlc/fictional-character-analysis.md",
        "dlc/narrative-identity.md",
        "dlc/relationship-dynamics.md",
    ),
}
REPOSITORY_ONLY_ENTRIES = (
    "archive", "docs", "evals", "scripts", "shared", "tests", ".github", "README.md",
    "README.zh-CN.md", "CONTRIBUTING.md",
)


def main() -> int:
    for skill_name, required_files in REQUIRED_RUNTIME_FILES.items():
        with TemporaryDirectory(prefix=f"{skill_name}-install-") as temp_dir:
            status = check_installation(skill_name, required_files, Path(temp_dir))
            if status:
                return status
    print("Sandboxed installs passed for both skills in Codex and Claude Code; runtime files are complete and repository-only content is excluded.")
    return 0


def check_installation(skill_name: str, required_files: tuple[str, ...], temp_dir: Path) -> int:
    try:
        result = subprocess.run(
            [
                "npx",
                "--yes",
                f"skills@{SKILLS_CLI_VERSION}",
                "add",
                str(SKILL_SOURCE),
                "--skill",
                skill_name,
                "--agent",
                "codex",
                "claude-code",
                "--yes",
                "--copy",
            ],
            cwd=temp_dir,
            check=False,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"Skills CLI installation of {skill_name} timed out after {TIMEOUT_SECONDS}s", file=sys.stderr)
        return 1
    output = result.stdout + result.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    if result.returncode:
        print(f"Skills CLI exited with status {result.returncode} while installing {skill_name}", file=sys.stderr)
        return result.returncode
    installed_entries = {
        "Codex": temp_dir / ".agents" / "skills" / skill_name,
        "Claude Code": temp_dir / ".claude" / "skills" / skill_name,
    }
    for agent, installed_entry in installed_entries.items():
        missing = [name for name in required_files if not (installed_entry / name).is_file()]
        if missing:
            print(
                f"{skill_name} {agent}-target install is missing runtime files: {', '.join(missing)}",
                file=sys.stderr,
            )
            return 1
        unexpected = [
            name for name in REQUIRED_RUNTIME_FILES
            if name != skill_name and (installed_entry.parent / name).exists()
        ]
        if unexpected:
            print(f"Unexpected skills installed with {skill_name} for {agent}: {', '.join(unexpected)}", file=sys.stderr)
            return 1
        leaked = [name for name in REPOSITORY_ONLY_ENTRIES if (installed_entry / name).exists()]
        if leaked:
            print(f"Repository-only content leaked into {skill_name} {agent} install: {', '.join(leaked)}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
