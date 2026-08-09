#!/usr/bin/env python3
"""Verify SHA-256 evidence bindings recorded by a Scenario review.

The verifier deliberately checks integrity only. It does not validate review
semantics, verdict consistency, or a repository-specific review schema.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA256_PATTERN = re.compile(r"^(?:sha256:)?([0-9a-fA-F]{64})$")


class ReviewError(ValueError):
    """Raised when a review or binding is structurally unsafe."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_hash(value: Any, location: str) -> str:
    if not isinstance(value, str):
        raise ReviewError(f"{location} must be a SHA-256 string")
    match = SHA256_PATTERN.fullmatch(value)
    if match is None:
        raise ReviewError(f"{location} is not a valid SHA-256 value")
    return match.group(1).lower()


def add_binding(
    bindings: dict[str, str], path_value: Any, hash_value: Any, location: str
) -> None:
    if not isinstance(path_value, str) or not path_value:
        raise ReviewError(f"{location}.path must be a non-empty string")
    normalized = normalize_hash(hash_value, f"{location}.sha256")
    existing = bindings.get(path_value)
    if existing is not None and existing != normalized:
        raise ReviewError(f"conflicting hashes recorded for {path_value}")
    bindings[path_value] = normalized


def collect_recursive_pairs(value: Any, bindings: dict[str, str], location: str) -> None:
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            add_binding(bindings, value["path"], value["sha256"], location)
        for key, child in value.items():
            collect_recursive_pairs(child, bindings, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_recursive_pairs(child, bindings, f"{location}[{index}]")


def collect_bindings(review: Any) -> dict[str, str]:
    if not isinstance(review, dict):
        raise ReviewError("review root must be a JSON object")

    bindings: dict[str, str] = {}
    reviewed = review.get("reviewed_artifacts")
    if isinstance(reviewed, dict):
        for path_value, hash_value in reviewed.items():
            add_binding(
                bindings,
                path_value,
                hash_value,
                f"reviewed_artifacts[{path_value!r}]",
            )
    elif reviewed is not None and not isinstance(reviewed, list):
        raise ReviewError("reviewed_artifacts must be a mapping or list")

    collect_recursive_pairs(review, bindings, "review")

    if "manifest_sha256" in review:
        add_binding(
            bindings,
            "manifest.json",
            review["manifest_sha256"],
            "manifest_sha256",
        )
    return bindings


def resolve_artifact(root: Path, path_value: str) -> tuple[str, Path]:
    raw = Path(path_value)
    if raw.is_absolute() or ".." in raw.parts:
        raise ReviewError(
            f"binding path must be relative and must not contain '..': {path_value}"
        )
    candidate = root / raw
    current = root
    for part in raw.parts:
        current = current / part
        if current.is_symlink():
            raise ReviewError(f"binding path contains a symlink: {path_value}")
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ReviewError(f"bound artifact does not exist: {path_value}") from exc
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ReviewError(f"binding path escapes artifact root: {path_value}") from exc
    if not resolved.is_file():
        raise ReviewError(f"bound artifact is not a regular file: {path_value}")
    return relative, resolved


def load_review(review_path: str) -> Any:
    if review_path == "-":
        return json.load(sys.stdin)
    with Path(review_path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify artifact hashes referenced by a Scenario review."
    )
    parser.add_argument("--artifact-root", required=True, help="Frozen artifact directory")
    parser.add_argument(
        "--review",
        required=True,
        help="Review JSON path, or '-' to read JSON from standard input",
    )
    parser.add_argument(
        "--allow-no-bindings",
        action="store_true",
        help="Allow a review with no directly discoverable path/SHA-256 bindings",
    )
    return parser.parse_args()


def emit(
    status: str,
    binding_count: int,
    verified: dict[str, str],
    errors: list[str],
) -> None:
    result: dict[str, Any] = {
        "status": status,
        "binding_count": binding_count,
        "verified_count": len(verified),
        "verified_paths": sorted(verified),
    }
    if errors:
        result["errors"] = errors
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    try:
        root = Path(args.artifact_root).resolve(strict=True)
        if not root.is_dir():
            raise ReviewError(f"artifact root is not a directory: {root}")
        review = load_review(args.review)
        bindings = collect_bindings(review)
        if not bindings:
            if args.allow_no_bindings:
                emit("PASS", 0, {}, [])
                return 0
            raise ReviewError("review contains no discoverable artifact bindings")

        errors: list[str] = []
        verified: dict[str, str] = {}
        for path_value, expected_hash in sorted(bindings.items()):
            try:
                relative, artifact = resolve_artifact(root, path_value)
                actual_hash = sha256_file(artifact)
                if actual_hash != expected_hash:
                    errors.append(
                        f"hash mismatch for {path_value}: expected {expected_hash}, "
                        f"actual {actual_hash}"
                    )
                else:
                    verified[relative] = expected_hash
            except (OSError, ReviewError) as exc:
                errors.append(str(exc))

        if errors:
            emit("FAIL", len(bindings), verified, errors)
            return 2
        emit("PASS", len(bindings), verified, [])
        return 0
    except (OSError, json.JSONDecodeError, ReviewError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
