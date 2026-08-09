#!/usr/bin/env python3
"""Hash selected files beneath one Scenario artifact root.

This utility only produces deterministic evidence bindings. It does not decide
whether a Scenario run passed.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import sys
from pathlib import Path


class SelectionError(ValueError):
    """Raised when an artifact selection is unsafe or cannot be resolved."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reject_symlink_components(root: Path, candidate: Path) -> None:
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise SelectionError(f"artifact escapes the root: {candidate}") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise SelectionError(f"symlinks are not accepted: {current}")


def relative_file(root: Path, candidate: Path) -> tuple[str, Path]:
    reject_symlink_components(root, candidate)
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise SelectionError(f"artifact does not exist: {candidate}") from exc
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise SelectionError(f"artifact escapes the root: {candidate}") from exc
    if not resolved.is_file():
        raise SelectionError(f"artifact is not a regular file: {candidate}")
    return relative.as_posix(), resolved


def expand_selection(root: Path, selection: str) -> list[tuple[str, Path]]:
    raw = Path(selection)
    if raw.is_absolute() or ".." in raw.parts:
        raise SelectionError(f"selection must be a relative path without '..': {selection}")

    matches = [Path(value) for value in glob.glob(str(root / selection), recursive=True)]
    if not matches:
        raise SelectionError(f"selection matched no artifacts: {selection}")

    files: list[tuple[str, Path]] = []
    for match in matches:
        reject_symlink_components(root, match)
        if match.is_dir():
            descendants = sorted(match.rglob("*"), key=lambda path: path.as_posix())
            for descendant in descendants:
                reject_symlink_components(root, descendant)
                if descendant.is_file():
                    files.append(relative_file(root, descendant))
        elif match.is_file():
            files.append(relative_file(root, match))
        else:
            raise SelectionError(f"unsupported artifact type: {match}")
    return files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SHA-256 bindings for selected Scenario artifacts."
    )
    parser.add_argument("artifact_root", help="Frozen Scenario artifact directory")
    parser.add_argument(
        "selections",
        nargs="+",
        help="Relative file, directory, or glob under the artifact root",
    )
    parser.add_argument(
        "--format",
        choices=("mapping", "list"),
        default="mapping",
        help="Output a path-to-hash mapping or a list of path/hash objects",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = Path(args.artifact_root).resolve(strict=True)
        if not root.is_dir():
            raise SelectionError(f"artifact root is not a directory: {root}")

        selected: dict[str, Path] = {}
        for selection in args.selections:
            for relative, resolved in expand_selection(root, selection):
                selected[relative] = resolved
        if not selected:
            raise SelectionError("no regular files were selected")

        bindings = {
            relative: f"sha256:{sha256_file(selected[relative])}"
            for relative in sorted(selected)
        }
        if args.format == "list":
            output: object = [
                {"path": relative, "sha256": digest}
                for relative, digest in bindings.items()
            ]
        else:
            output = bindings
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=False))
        return 0
    except (OSError, SelectionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
