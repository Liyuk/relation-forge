#!/usr/bin/env python3
"""Copy canonical shared files into skill packages.

``shared/manifest.json`` is the list of sources. Each destination is a real
file inside a skill package, so the package can be installed without links
outside its own directory.

Edit the canonical file, then run this script. Do not edit the copies by hand.
``--check`` fails when a copy is missing or different, or when both skill
packages contain the same relative path with identical bytes and that path is
not listed in the manifest.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


MANIFEST_RELATIVE = Path("shared/manifest.json")
SKILL_NAMES = ("interaction-risk-analysis", "person-deep-analysis")


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_RELATIVE


def _load_manifest(root: Path) -> tuple[dict | None, list[str]]:
    path = manifest_path(root)
    if not path.is_file():
        if (root / "shared").exists():
            return None, [f"{MANIFEST_RELATIVE.as_posix()}: missing shared-copy manifest"]
        return None, []
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return None, [f"{MANIFEST_RELATIVE.as_posix()}: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{MANIFEST_RELATIVE.as_posix()}: manifest must be an object"]
    return data, []


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _safe_path(root: Path, raw: str) -> Path | None:
    if not isinstance(raw, str) or not raw or raw.startswith("/") or "\\" in raw:
        return None
    parts = Path(raw).parts
    if any(part in ("", ".", "..") for part in parts):
        return None
    path = (root / raw).resolve()
    if not path.is_relative_to(root.resolve()):
        return None
    return path


def planned_copies(root: Path, data: dict) -> tuple[list[tuple[Path, Path]], list[str]]:
    """Return (source, destination) pairs and manifest errors."""
    errors = []
    pairs: list[tuple[Path, Path]] = []
    files = data.get("files", [])
    trees = data.get("trees", [])
    if not isinstance(files, list) or not isinstance(trees, list):
        return [], [f"{MANIFEST_RELATIVE.as_posix()}: files and trees must be lists"]
    for entry in files:
        if not isinstance(entry, dict):
            errors.append(f"{MANIFEST_RELATIVE.as_posix()}: file entry must be an object")
            continue
        source = _safe_path(root, entry.get("source"))
        destinations = entry.get("destinations")
        if source is None or not isinstance(destinations, list) or not destinations:
            errors.append(f"{MANIFEST_RELATIVE.as_posix()}: invalid file copy entry")
            continue
        for raw in destinations:
            dest = _safe_path(root, raw)
            if dest is None or "skills" not in dest.parts:
                errors.append(
                    f"{MANIFEST_RELATIVE.as_posix()}: destination must stay inside a skill package: {raw}"
                )
                continue
            pairs.append((source, dest))
    for entry in trees:
        if not isinstance(entry, dict):
            errors.append(f"{MANIFEST_RELATIVE.as_posix()}: tree entry must be an object")
            continue
        source = _safe_path(root, entry.get("source"))
        destinations = entry.get("destinations")
        if source is None or not isinstance(destinations, list) or not destinations:
            errors.append(f"{MANIFEST_RELATIVE.as_posix()}: invalid tree copy entry")
            continue
        if not source.is_dir():
            errors.append(f"{_relative(root, source)}: shared tree is missing")
            continue
        relative_files = sorted(p.relative_to(source) for p in source.rglob("*") if p.is_file())
        if not relative_files:
            errors.append(f"{_relative(root, source)}: shared tree has no files")
            continue
        for raw in destinations:
            if not isinstance(raw, str) or Path(raw).parts[:1] != ("skills",) or len(Path(raw).parts) != 2:
                errors.append(f"{MANIFEST_RELATIVE.as_posix()}: tree destination must be skills/<name>: {raw}")
                continue
            dest_root = _safe_path(root, raw)
            if dest_root is None:
                errors.append(
                    f"{MANIFEST_RELATIVE.as_posix()}: tree destination must stay inside a skill package: {raw}"
                )
                continue
            for relative in relative_files:
                pairs.append((source / relative, dest_root / relative))
    return pairs, errors


def identical_unlisted_errors(root: Path, expected: set[str]) -> list[str]:
    """Fail when both packages contain the same bytes at a path the manifest omits."""
    packages = [root / "skills" / name for name in SKILL_NAMES]
    if any(not package.is_dir() for package in packages):
        return []
    errors = []
    first, second = packages
    for path in sorted(p for p in first.rglob("*") if p.is_file()):
        relative = path.relative_to(first).as_posix()
        twin = second / relative
        if not twin.is_file() or path.read_bytes() != twin.read_bytes():
            continue
        destinations = {f"skills/{name}/{relative}" for name in SKILL_NAMES}
        if not destinations <= expected:
            errors.append(
                f"{relative}: identical in both skill packages but not listed in {MANIFEST_RELATIVE.as_posix()}"
            )
    return errors


def copy_errors(root: Path) -> list[str]:
    root = root.resolve()
    data, errors = _load_manifest(root)
    if data is None:
        return errors
    pairs, manifest_errors = planned_copies(root, data)
    errors.extend(manifest_errors)
    expected: set[str] = set()
    for source, dest in pairs:
        source_rel = _relative(root, source) if source.is_relative_to(root.resolve()) else str(source)
        dest_rel = _relative(root, dest)
        expected.add(dest_rel)
        if not source.is_file():
            errors.append(f"{source_rel}: canonical shared file is missing")
            continue
        if not dest.is_file():
            errors.append(f"{dest_rel}: missing synced copy; run python3 scripts/sync_shared_copies.py --write")
            continue
        if source.read_bytes() != dest.read_bytes():
            errors.append(
                f"{dest_rel}: differs from {source_rel}; run python3 scripts/sync_shared_copies.py --write"
            )
    errors.extend(identical_unlisted_errors(root, expected))
    return errors


def write_copies(root: Path) -> list[str]:
    root = root.resolve()
    data, errors = _load_manifest(root)
    if data is None:
        raise ValueError("; ".join(errors) or "missing shared-copy manifest")
    pairs, manifest_errors = planned_copies(root, data)
    if manifest_errors:
        raise ValueError("; ".join(manifest_errors))
    written = []
    for source, dest in pairs:
        if not source.is_file():
            raise ValueError(f"{_relative(root, source)}: canonical shared file is missing")
        dest.parent.mkdir(parents=True, exist_ok=True)
        payload = source.read_bytes()
        if not dest.is_file() or dest.read_bytes() != payload:
            dest.write_bytes(payload)
            written.append(_relative(root, dest))
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        if args.check:
            errors = copy_errors(args.root)
            if errors:
                print("Shared copies are out of sync:")
                for error in errors:
                    print("- " + error)
                return 1
            print("Shared copies match shared/manifest.json.")
            return 0
        written = write_copies(args.root)
        if written:
            print("Updated shared copies:")
            for path in written:
                print("- " + path)
        else:
            print("Shared copies already match shared/manifest.json.")
        return 0
    except (OSError, ValueError) as exc:
        print("ERROR:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
