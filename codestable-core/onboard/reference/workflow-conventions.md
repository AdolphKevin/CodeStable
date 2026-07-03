# CodeStable Workflow Conventions
## Document map

- Entry model
- Before code
- Minimality
- Quality checks
- Project Sync
- Scoped commit
- History integrity

## Entry model

Use `cs-plan` for planning/onboard/explore/audit-only ledgers, `cs-do` for scoped execution, and `cs-review` for verification/sync/closure. Do not call internal historical Skill names.

## Before code

Before implementation, read:

1. current lifecycle artifact or fastforward plan;
2. `.codestable/INDEX.md`;
3. `.codestable/attention.md`;
4. task context pack when present;
5. scoped specs relevant to the touched area;
6. completed audit ledger when audit-only was required;
7. specific architecture/requirements/compound docs only when the indexes point to them.

## Minimality

Apply the ladder from `reference/minimality-ladder.md`: no-op, reuse existing code, platform/stdlib, existing dependency, one-home change, then new minimal code. Never cut validation, security, accessibility, data safety, or verification.

## Quality checks

Use project-native commands from README, package scripts, Makefile, CI, or existing tests. If full checks are too expensive or unavailable, run the smallest meaningful check and state what was not covered.

Separate dirty files into current scope, CodeStable artifacts, and unrelated work. Do not include unrelated dirty files in conclusions. If audit-only was required, do not implement from a missing or partial ledger.

## Project Sync

`cs-review` owns durable knowledge freshness. Sync only current facts:

| Signal | Sync target |
|---|---|
| module boundary, API, data/state ownership, config shape, main flow changed | architecture |
| user-visible capability, business rule, success/failure contract changed | requirements |
| roadmap item status, blocker, dependency changed | roadmap |
| confirmed coding convention or test command changed | specs |
| reusable decision, learning, trick, explore result | compound |
| short always-read project warning | attention |

No signal means `Project Sync: no-sync`.

## Scoped commit

Do not commit unless the user asks or approves. A commit contains only current task code, current task `.codestable` artifacts, and docs actually synced for this task.

## History integrity

Approved design/report/analysis/checklists are historical records. Do not rewrite them to make the final result look planned. Record accepted divergence in acceptance, fix-note, apply-notes, journal, or a dated addendum.
