#!/usr/bin/env python3
"""Create or update a compact CodeStable task proof trace template."""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime

TEMPLATE = """# Proof Trace: {title}

## Contract
- Route: {route}
- Success criteria: TODO
- Non-goals: TODO
- Human gate / owner decision: TODO
- Minimality rung expected: TODO

## Evidence before change
- Code anchors: TODO
- Reproduction or baseline check: TODO
- Existing reusable paths: TODO

## Change evidence
- Diff summary: TODO
- Files touched: TODO
- Added abstractions / dependencies: TODO
- Why earlier minimality rungs did not apply: TODO

## Validation evidence
- Commands run: TODO
- Manual paths: TODO
- Before/after result: TODO
- Uncovered risk: TODO

## Knowledge freshness
- Writeback Matrix: TODO
- Index Sync: TODO
- Doc-sweep claim matrix, if any: TODO

---
Created: {created}
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Path to proof.md")
    ap.add_argument("--title", default="task")
    ap.add_argument("--route", default="unknown")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    path = Path(args.path)
    if path.exists() and not args.force:
        print(f"exists: {path}")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(title=args.title, route=args.route, created=datetime.now().isoformat(timespec='seconds')), encoding="utf-8")
    print(f"wrote: {path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
