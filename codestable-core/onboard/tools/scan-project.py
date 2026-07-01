#!/usr/bin/env python3
"""Create a lightweight CodeStable code inventory for onboarding and doc-sweep.

The scanner is intentionally conservative: it records observable files, manifests,
commands, directories, and anchor candidates. It does not try to fully understand
business behavior.
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".codestable", "node_modules", "dist", "build", "out",
    "coverage", ".next", ".nuxt", ".turbo", ".cache", ".venv", "venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "target", "vendor",
}
MANIFEST_NAMES = {
    "package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "bun.lockb",
    "pyproject.toml", "requirements.txt", "poetry.lock", "Pipfile", "go.mod", "go.sum",
    "Cargo.toml", "Cargo.lock", "pom.xml", "build.gradle", "settings.gradle", "composer.json",
    "Gemfile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml", "Makefile",
}
CONFIG_PATTERNS = (
    "tsconfig", "vite.config", "next.config", "nuxt.config", "webpack.config", "rollup.config",
    "eslint", "prettier", "jest", "vitest", "pytest", "ruff", "mypy", "tailwind", "prisma",
    "drizzle", "sequelize", "typeorm", "knex", "openapi", "swagger",
)
SOURCE_DIR_NAMES = {"src", "app", "pages", "components", "lib", "server", "api", "routes", "services", "core", "cmd", "internal", "pkg"}
TEST_DIR_HINTS = {"test", "tests", "__tests__", "e2e"}
TEST_FILE_MARKERS = (".test.", ".spec.", "_test.", "-test.")
TEST_FILE_PREFIXES = ("test_",)
ROUTE_HINTS = ("route", "routes", "router", "controller", "handler", "api", "endpoint")
SCHEMA_HINTS = ("schema", "model", "models", "migration", "migrations", "prisma", "drizzle")


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        dirnames[:] = [name for name in dirnames if name not in IGNORE_DIRS and not name.startswith(".") or name in {".github"}]
        for name in filenames:
            p = d / name
            if not should_ignore(p.relative_to(root)):
                yield p


def is_test_path(path: Path) -> bool:
    parts = [part.lower() for part in path.parts]
    lower = path.name.lower()
    if any(part in TEST_DIR_HINTS for part in parts):
        return True
    return lower.startswith(TEST_FILE_PREFIXES) or any(marker in lower for marker in TEST_FILE_MARKERS)


def file_kind(path: Path) -> str:
    name = path.name
    lower = name.lower()
    if name in MANIFEST_NAMES:
        return "manifest"
    if lower.startswith("readme") or lower in {"license", "changelog.md"}:
        return "project-doc"
    if any(x in lower for x in CONFIG_PATTERNS):
        return "config"
    if is_test_path(path):
        return "test"
    if any(x in part.lower() or x in lower for part in path.parts for x in ROUTE_HINTS):
        return "route-api"
    if any(x in part.lower() or x in lower for part in path.parts for x in SCHEMA_HINTS):
        return "schema-model"
    if path.suffix.lower() in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".go", ".rs", ".java", ".kt", ".php", ".rb", ".cs", ".swift"}:
        return "source"
    return "other"


def detect_commands(root: Path) -> List[Dict[str, str]]:
    commands: List[Dict[str, str]] = []
    package_json = root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            for name, cmd in sorted((data.get("scripts") or {}).items()):
                commands.append({"source": "package.json", "name": name, "command": str(cmd)})
        except Exception as exc:  # pragma: no cover - diagnostic only
            commands.append({"source": "package.json", "name": "parse-error", "command": str(exc)})
    makefile = root / "Makefile"
    if makefile.exists():
        for line in makefile.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line and not line.startswith("\t") and ":" in line and not line.startswith("."):
                target = line.split(":", 1)[0].strip()
                if target and all(c.isalnum() or c in "_-" for c in target):
                    commands.append({"source": "Makefile", "name": target, "command": f"make {target}"})
    if (root / "pyproject.toml").exists():
        commands.append({"source": "pyproject.toml", "name": "python-tests", "command": "pytest"})
    if (root / "go.mod").exists():
        commands.append({"source": "go.mod", "name": "go-tests", "command": "go test ./..."})
    if (root / "Cargo.toml").exists():
        commands.append({"source": "Cargo.toml", "name": "rust-tests", "command": "cargo test"})
    return commands


def detect_stack(files: List[Path], root: Path) -> List[str]:
    names = {p.name for p in files}
    stack = []
    checks = [
        ("package.json", "node/js-ts"), ("tsconfig.json", "typescript"), ("next.config.js", "nextjs"),
        ("next.config.mjs", "nextjs"), ("vite.config.ts", "vite"), ("vite.config.js", "vite"),
        ("pyproject.toml", "python"), ("requirements.txt", "python"), ("go.mod", "go"),
        ("Cargo.toml", "rust"), ("pom.xml", "java/maven"), ("build.gradle", "java/gradle"),
        ("Dockerfile", "docker"), ("docker-compose.yml", "docker-compose"),
    ]
    for filename, label in checks:
        if filename in names and label not in stack:
            stack.append(label)
    return stack


def top_modules(files: List[Path], root: Path) -> List[Dict[str, object]]:
    buckets: Dict[str, List[Path]] = defaultdict(list)
    for p in files:
        rp = p.relative_to(root)
        if len(rp.parts) == 1:
            key = "."
        elif rp.parts[0] in {"src", "app", "packages", "apps", "services", "cmd", "internal", "pkg"} and len(rp.parts) > 1:
            key = "/".join(rp.parts[:2])
        else:
            key = rp.parts[0]
        buckets[key].append(p)
    rows = []
    for key, vals in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:30]:
        kinds = Counter(file_kind(v) for v in vals)
        reps = [rel(v, root) for v in vals[:5]]
        rows.append({"path": key, "file_count": len(vals), "kinds": dict(kinds), "representative_files": reps})
    return rows


def build_inventory(root: Path) -> Dict[str, object]:
    files = sorted(iter_files(root), key=lambda p: rel(p, root))
    entries = []
    for p in files:
        if p.is_file():
            entries.append({"path": rel(p, root), "kind": file_kind(p), "suffix": p.suffix, "size": p.stat().st_size})
    by_kind = Counter(e["kind"] for e in entries)
    selected = lambda kind: [e["path"] for e in entries if e["kind"] == kind][:80]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root.resolve()),
        "summary": {"file_count": len(entries), "by_kind": dict(by_kind), "stack_hints": detect_stack(files, root)},
        "commands": detect_commands(root),
        "manifests": selected("manifest"),
        "project_docs": selected("project-doc"),
        "configs": selected("config"),
        "tests": selected("test"),
        "route_api_hints": selected("route-api"),
        "schema_model_hints": selected("schema-model"),
        "source_hints": selected("source"),
        "top_modules": top_modules(files, root),
    }


def to_markdown(inv: Dict[str, object]) -> str:
    lines = ["# Code Inventory", "", f"Generated at: `{inv['generated_at']}`", "", "## Summary", ""]
    summary = inv["summary"]
    lines.append(f"- Files scanned: {summary['file_count']}")
    lines.append(f"- Stack hints: {', '.join(summary.get('stack_hints') or ['unknown'])}")
    lines.append("- By kind: " + ", ".join(f"{k}={v}" for k, v in sorted(summary["by_kind"].items())))
    lines += ["", "## Commands", ""]
    for c in inv.get("commands", []):
        lines.append(f"- `{c['command']}` ({c['source']}:{c['name']})")
    if not inv.get("commands"):
        lines.append("- none detected")
    for title, key in [("Manifests", "manifests"), ("Project docs", "project_docs"), ("Configs", "configs"), ("Tests", "tests"), ("Route/API hints", "route_api_hints"), ("Schema/model hints", "schema_model_hints")]:
        lines += ["", f"## {title}", ""]
        items = inv.get(key, [])
        if items:
            for item in items[:40]:
                lines.append(f"- `{item}`")
        else:
            lines.append("- none detected")
    lines += ["", "## Top modules", ""]
    for m in inv.get("top_modules", []):
        lines.append(f"- `{m['path']}` — {m['file_count']} files; kinds={m['kinds']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", dest="json_path")
    ap.add_argument("--markdown", dest="markdown_path")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    inv = build_inventory(root)
    if args.json_path:
        p = Path(args.json_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_path:
        p = Path(args.markdown_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(to_markdown(inv), encoding="utf-8")
    if not args.json_path and not args.markdown_path:
        print(json.dumps(inv, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
