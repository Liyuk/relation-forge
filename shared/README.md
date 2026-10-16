# Shared skill files

These files are the only editable copies of content that both skill packages need.

`manifest.json` lists each canonical file and the skill-package paths that must stay identical to it. `scripts/sync_shared_copies.py --write` copies them into those packages. `scripts/sync_shared_copies.py --check` fails when a copy is missing or different, and when the same relative path is byte-identical in both packages but is not listed here.

Skill packages do not link here. A copied skill directory remains installable on its own. Edit the canonical file, then run the sync script. Do not edit the copies by hand.

`shared/common/` holds the reference files that are the same in `interaction-risk-analysis` and `person-deep-analysis`. The repository root `LICENSE` is the canonical license text; the script copies it into each package. Files that differ between the packages stay in those packages and are not listed here.

[Liyuk/skills](https://github.com/Liyuk/skills) vendors these two skills and keeps its own `shared/relation-forge` tree. Editing this directory does not update that repository.
