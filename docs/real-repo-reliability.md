# Real-repo reliability

## Document map

- Why this reliability layer exists
- What counts as evidence
- How to debug poor outcomes
- Bug fix / refactor / audit-only / review gates

## Why this reliability layer exists

A correct Skill package is not enough. CodeStable should improve real work in real repositories: bug fixes should start from the failure, refactors should prove behavior equivalence, audit-only backend chains should produce a complete file-level ledger before fixes, and reviews/doc-sweeps should prefer current code over old documents.

CodeStable therefore uses three hard ideas:

1. **Evidence levels**: each route states whether it has user intent, docs, code anchors, executable checks, or before/after proof.
2. **Proof trace**: non-trivial work records a compact audit trail in task memory.
3. **Audit ledger**: high-risk backend prompt/schema/status/event chains enumerate modules, callers, consumers, risks, and exact `已审完/未审完` status before code.
4. **Fail closed**: when evidence is too weak, the entry returns `blocked:*` instead of guessing.

## What counts as evidence

- L0: user intent only.
- L1: current docs or `.codestable` index.
- L2: current code/manifests/config/tests anchors.
- L3: executable command output or reproduction path.
- L4: before/after proof.

Bug fix and refactor closure should aim for L4. Audit-only completion requires L2 anchors for every relevant module and prompt/schema path-field-caller-consumer mapping. Doc-sweep mutation requires claim mapping to current anchors plus user approval.

## How to debug poor outcomes

Look at the final protocol fields:

```text
Route:
Playbook:
Evidence Level:
Reliability Gate:
Proof Trace:
Audit Ledger / Audit Status:
Minimality / Overbuild:
Next:
```

If the result is bad, fix the first broken layer: route, evidence threshold, human gate, proof trace, then playbook wording.

## Gates

- Bug fix: reproduction or no-repro rationale before code.
- Refactor: equivalence proof path before code.
- Audit-only: file-level ledger and `Audit Status: 已审完` before `cs-do`; partial ledgers block execution.
- Review: checks/proof trace/writeback matrix before closure.
- Doc-sweep: claim matrix before mutation; delete/archive only after explicit path-by-path approval.
