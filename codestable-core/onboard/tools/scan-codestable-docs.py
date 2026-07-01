#!/usr/bin/env python3
"""Inventory .codestable documents for code-grounded doc-sweep."""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

EXCLUDE_PARTS = {"tools", "reference"}
DOC_SUFFIXES = {".md", ".yaml", ".yml"}
CODE_ANCHOR_RE = re.compile(r"`([^`]+\.(?:ts|tsx|js|jsx|py|go|rs|java|kt|php|rb|cs|sql|json|yaml|yml|toml|md)(?::\d+)?)`")
STATUS_RE = re.compile(r"(?:status|状态)\s*[:：]\s*([^\n]+)", re.IGNORECASE)


def rel(p: Path, root: Path) -> str:
    return p.relative_to(root).as_posix()


def should_include(path: Path, cs_root: Path) -> bool:
    rp = path.relative_to(cs_root)
    if any(part in EXCLUDE_PARTS for part in rp.parts):
        return False
    return path.suffix.lower() in DOC_SUFFIXES


def classify_doc(path: Path, text: str) -> dict:
    anchors = sorted(set(CODE_ANCHOR_RE.findall(text)))[:30]
    status_match = STATUS_RE.search(text[:1000])
    headings = [line.strip("# ") for line in text.splitlines() if line.startswith("#")][:10]
    return {
        "path": path.as_posix(),
        "status_hint": status_match.group(1).strip() if status_match else "unknown",
        "headings": headings,
        "code_anchors": anchors,
        "bytes": len(text.encode("utf-8")),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".codestable")
    ap.add_argument("--json", dest="json_path")
    args = ap.parse_args()
    cs_root = Path(args.root).resolve()
    docs = []
    if cs_root.exists():
        for dirpath, dirnames, filenames in os.walk(cs_root):
            d = Path(dirpath)
            dirnames[:] = [name for name in dirnames if name not in EXCLUDE_PARTS]
            for name in filenames:
                p = d / name
                if should_include(p, cs_root):
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    item = classify_doc(Path(rel(p, cs_root)), text)
                    docs.append(item)
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "root": str(cs_root), "documents": docs}
    if args.json_path:
        out = Path(args.json_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
