#!/usr/bin/env python3
"""Generate a CodeStable doc-sweep claim-matrix skeleton.

This tool does not semantically decide truth. It inventories candidate docs and creates a
claim matrix scaffold so cs-review can map durable claims to current code anchors.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from datetime import datetime

EXCLUDE_PARTS = {"tools", "reference"}

def iter_docs(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml"}:
            rel = p.relative_to(root)
            if any(part in EXCLUDE_PARTS for part in rel.parts):
                continue
            yield p

def extract_headings(text: str):
    out = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if m:
            out.append(m.group(2).strip())
    return out[:12]

def md_cell(value: str) -> str:
    return value.replace("|", r"\|")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".codestable")
    ap.add_argument("--out", default=".codestable/doc-sweeps/claim-matrix.md")
    args = ap.parse_args()
    root = Path(args.root)
    rows = []
    for p in sorted(iter_docs(root)):
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(root).as_posix()
        headings = extract_headings(text)
        rows.append({"document": rel, "candidate_claims": headings})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Doc-sweep Claim Matrix",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "This is a scaffold. Fill Current anchor / Classification before mutating docs.",
        "",
        "| Document | Claim | Claimed status/date | Current anchor | Anchor type | Classification | Recommended action |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        claims = row["candidate_claims"] or ["TODO extract durable claim"]
        for claim in claims:
            lines.append(f"| `{md_cell(row['document'])}` | {md_cell(claim)} | TODO status/date | TODO | TODO | unverified | TODO |")
    out.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({"documents": len(rows), "out": str(out)}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
