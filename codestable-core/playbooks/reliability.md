# Real-repo reliability playbook
## Document map

Use this map first, then open only the section needed:

- Purpose
- Evidence levels
- Proof trace
- Bug-fix reliability
- Refactor reliability
- Review and doc freshness reliability
- Debuggability
- Output fields
- Hard stops

## Purpose

This playbook turns CodeStable from a process wrapper into a real-repository reliability harness. A route is not considered ready just because a plan exists; it is ready only when the current repository provides enough evidence to execute or review safely.

Owned by: `cs-plan`, `cs-do`, and `cs-review`.

## Evidence levels

Use the strongest available evidence and fail closed when the level is too weak for the requested mutation.

| Level | Evidence | Good for |
|---|---|---|
| L0 | user intent only | brainstorming, owner decisions, manual sync draft |
| L1 | current docs or `.codestable` index | navigation and candidate constraints |
| L2 | current code/manifests/config/tests anchors | planning, doc-sweep classification, implementation boundary |
| L3 | executable command output or reproduction path | bug fix, refactor equivalence, acceptance |
| L4 | before/after proof: failing-before/passing-after test, golden diff, or validated manual path | closure and durable writeback |

Rules:

- For `cs-do` bug fixes, require L2 plus either L3 reproduction or an explicit explanation why reproduction is unavailable.
- For refactors, require an equivalence proof path before editing.
- For doc-sweep mutation, require L2 claim mapping plus user approval for archive/delete/rewrite.
- For review closure, prefer L4; if unavailable, state the highest level achieved and what remains unproven.

## Proof trace

Every non-trivial task should have a proof trace. Task memory may store it at:

```text
.codestable/tasks/YYYY-MM-DD-{slug}/proof.md
```

Minimum sections:

```markdown
# Proof Trace: {task}

## Contract
- Route:
- Success criteria:
- Non-goals:
- Human gate / owner decision:
- Minimality rung expected:

## Evidence before change
- Code anchors:
- Reproduction or baseline check:
- Existing reusable paths:

## Change evidence
- Diff summary:
- Files touched:
- Added abstractions / dependencies:
- Why earlier minimality rungs did not apply:

## Validation evidence
- Commands run:
- Manual paths:
- Before/after result:
- Uncovered risk:

## Knowledge freshness
- Writeback Matrix:
- Index Sync:
- Doc-sweep claim matrix, if any:
```

A proof trace is not a verbose diary. It is the compact audit trail that allows a later human or agent to decide whether the work was actually safe.

## Bug-fix reliability

Bug fixes are more reliable when they start from the failure, not from an implementation guess.

Required before editing:

1. Symptom and affected entrypoint.
2. Current code path or config path suspected.
3. Reproduction command, failing test, log/request ID, or a reason reproduction is impossible.
4. Expected verification command or manual path.
5. Minimal fix boundary and forbidden scope.

If the root cause is uncertain, route to `issue.standard.report-analysis`. If a quickfix fails once, stop stacking patches and return to analysis.

## Refactor reliability

Refactor means behavior preservation. Required before editing:

1. Behavior contract: what must not change.
2. Equivalence proof path: existing tests, characterization test, snapshot/golden output, public API comparison, manual path, or explicit uncovered risk.
3. Scope limit: files/modules allowed and forbidden.
4. Churn budget: expected changed files and why.

If the task includes behavior change, reroute to feature or issue.

## Review and doc freshness reliability

Review is not complete until code, docs, and task memory agree at the right level.

For ordinary review:

- compare diff against route/contract;
- run or inspect checks;
- run overbuild review;
- finish task status/proof trace;
- promote only durable facts.

For doc-sweep:

- current code/manifests/tests/config outrank old docs;
- old docs are claims, not proof;
- every stale finding needs a current anchor or superseding source;
- no anchor means `unverified`, not `stale`;
- deletion/archive/rewrite requires explicit user approval and rollback note.

## Debuggability

Every public entry exposes enough fields to debug route quality without reading hidden instructions:

```text
Route:
Playbook:
Reliability Gate:
Evidence Level:
Proof Trace:
Minimality / Overbuild:
Next:
```

When an outcome is poor, debug in this order:

1. Was the route wrong?
2. Was the evidence level too weak for the mutation?
3. Was the human gate skipped?
4. Was task context/proof trace missing?
5. Was the playbook rule too vague?

## Output fields

Use these fields in addition to each public entry's normal protocol:

```text
Reliability Gate: pass | blocked:<reason> | not-applicable
Evidence Level: L0 | L1 | L2 | L3 | L4
Proof Trace: none | create:<path> | update:<path> | finish:<path>
```

## Hard stops

- Implementing a non-trivial bug fix without reproduction evidence or an explicit no-repro rationale.
- Refactoring without an equivalence proof path.
- Treating stale docs as proof against current code.
- Marking review complete when checks, proof trace, or owner gate are missing.
- Hiding weak evidence behind confident wording.
