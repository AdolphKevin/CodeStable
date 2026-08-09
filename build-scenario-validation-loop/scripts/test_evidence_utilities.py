#!/usr/bin/env python3
"""Regression tests for the bundled Scenario evidence utilities."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parent
HASH_ARTIFACTS = SCRIPT_ROOT / "hash_artifacts.py"
VERIFY_BINDINGS = SCRIPT_ROOT / "verify_review_bindings.py"


class EvidenceUtilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(
            prefix="scenario-evidence-tests-"
        )
        self.artifact_root = Path(self.temporary_directory.name)
        (self.artifact_root / "nested").mkdir()
        (self.artifact_root / "manifest.json").write_text(
            '{"run_id":"run-1"}\n', encoding="utf-8"
        )
        (self.artifact_root / "nested" / "report.md").write_text(
            "complete\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_script(
        self,
        script: Path,
        *arguments: object,
        expected_status: int = 0,
        stdin: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        process = subprocess.run(
            [sys.executable, str(script), *(str(argument) for argument in arguments)],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            expected_status,
            process.returncode,
            msg=(
                f"unexpected status for {script.name}: {process.returncode}\n"
                f"stdout:\n{process.stdout}\nstderr:\n{process.stderr}"
            ),
        )
        return process

    def hash_artifacts(self) -> dict[str, str]:
        process = self.run_script(
            HASH_ARTIFACTS,
            self.artifact_root,
            "manifest.json",
            "nested",
        )
        return json.loads(process.stdout)

    def write_review(self, value: Any, name: str = "codex-review.json") -> Path:
        path = self.artifact_root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_hash_outputs_are_sorted_and_support_both_formats(self) -> None:
        mapping = self.hash_artifacts()
        self.assertEqual(["manifest.json", "nested/report.md"], list(mapping))
        self.assertRegex(mapping["manifest.json"], r"^sha256:[0-9a-f]{64}$")

        process = self.run_script(
            HASH_ARTIFACTS,
            self.artifact_root,
            "manifest.json",
            "--format",
            "list",
        )
        self.assertEqual(
            [
                {
                    "path": "manifest.json",
                    "sha256": mapping["manifest.json"],
                }
            ],
            json.loads(process.stdout),
        )

    def test_hash_rejects_traversal_missing_files_and_symlinks(self) -> None:
        for selection in ("../outside.json", "missing.json"):
            with self.subTest(selection=selection):
                self.run_script(
                    HASH_ARTIFACTS,
                    self.artifact_root,
                    selection,
                    expected_status=2,
                )

        outside = self.artifact_root.parent / f"{self.artifact_root.name}-outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        link = self.artifact_root / "outside-link"
        try:
            link.symlink_to(outside)
        except OSError as error:
            outside.unlink(missing_ok=True)
            self.skipTest(f"symlinks are unavailable: {error}")
        try:
            self.run_script(
                HASH_ARTIFACTS,
                self.artifact_root,
                "outside-link",
                expected_status=2,
            )
        finally:
            outside.unlink(missing_ok=True)

    def test_verify_accepts_exact_list_bindings(self) -> None:
        mapping = self.hash_artifacts()
        review = {
            "reviewed_artifacts": [
                {"path": path, "sha256": digest}
                for path, digest in mapping.items()
            ]
        }
        review_path = self.write_review(review)
        process = self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            review_path,
        )
        result = json.loads(process.stdout)
        self.assertEqual("PASS", result["status"])
        self.assertEqual(2, result["binding_count"])
        self.assertEqual(2, result["verified_count"])

    def test_verify_supports_mapping_stdin_and_legacy_manifest_hash(self) -> None:
        mapping = self.hash_artifacts()
        mapping_review = json.dumps(
            {"reviewed_artifacts": {"nested/report.md": mapping["nested/report.md"]}}
        )
        process = self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            "-",
            stdin=mapping_review,
        )
        self.assertEqual("PASS", json.loads(process.stdout)["status"])

        legacy_path = self.write_review(
            {"manifest_sha256": mapping["manifest.json"]},
            name="legacy-review.json",
        )
        process = self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            legacy_path,
        )
        self.assertEqual("PASS", json.loads(process.stdout)["status"])

    def test_verify_reports_tampering_and_unsafe_paths(self) -> None:
        mapping = self.hash_artifacts()
        review_path = self.write_review(
            {"reviewed_artifacts": {"nested/report.md": mapping["nested/report.md"]}}
        )
        (self.artifact_root / "nested" / "report.md").write_text(
            "tampered\n", encoding="utf-8"
        )
        process = self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            review_path,
            expected_status=2,
        )
        result = json.loads(process.stdout)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("hash mismatch", result["errors"][0])

        traversal_path = self.write_review(
            {"reviewed_artifacts": {"../outside.json": "0" * 64}},
            name="traversal-review.json",
        )
        process = self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            traversal_path,
            expected_status=2,
        )
        self.assertIn("must not contain '..'", process.stdout)

        outside = self.artifact_root.parent / f"{self.artifact_root.name}-bound.txt"
        outside.write_text("outside\n", encoding="utf-8")
        link = self.artifact_root / "bound-link"
        try:
            link.symlink_to(outside)
        except OSError as error:
            outside.unlink(missing_ok=True)
            self.skipTest(f"symlinks are unavailable: {error}")
        try:
            symlink_review = self.write_review(
                {"reviewed_artifacts": {"bound-link": "0" * 64}},
                name="symlink-review.json",
            )
            process = self.run_script(
                VERIFY_BINDINGS,
                "--artifact-root",
                self.artifact_root,
                "--review",
                symlink_review,
                expected_status=2,
            )
            self.assertIn("contains a symlink", process.stdout)
        finally:
            outside.unlink(missing_ok=True)

    def test_verify_rejects_conflicts_and_requires_explicit_empty_opt_in(self) -> None:
        mapping = self.hash_artifacts()
        conflict_path = self.write_review(
            {
                "reviewed_artifacts": {
                    "manifest.json": mapping["manifest.json"]
                },
                "manifest_sha256": "0" * 64,
            },
            name="conflicting-review.json",
        )
        self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            conflict_path,
            expected_status=3,
        )

        empty_path = self.write_review({}, name="empty-review.json")
        self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            empty_path,
            expected_status=3,
        )
        process = self.run_script(
            VERIFY_BINDINGS,
            "--artifact-root",
            self.artifact_root,
            "--review",
            empty_path,
            "--allow-no-bindings",
        )
        result = json.loads(process.stdout)
        self.assertEqual("PASS", result["status"])
        self.assertEqual(0, result["binding_count"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
