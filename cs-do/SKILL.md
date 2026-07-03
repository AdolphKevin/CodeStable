---
name: cs-do
description: "CodeStable public entry for execution: read task context and completed audit ledgers when required, implement only ready work, apply the minimality ladder, reuse existing code, record evidence, and stop on missing approval."
---

# cs-do

## Document map

- Runtime playbook map
- Startup scan
- Fixed output protocol
- Execution route table
- Minimality execution rules
- Task memory rules
- Product boundary
- Completion standard

`cs-do` is the public **Execution** entry. It executes ready work only, keeps implementation scoped to the approved or fastforward boundary, and records evidence so `cs-review` can close the loop.

The shared rules live in `../codestable-core/playbooks/`; they are auditable references, not hidden Skills.

## Runtime playbook map

| Concern | Runtime authority |
|---|---|
| Human gates | `../codestable-core/playbooks/collaboration.md` |
| Task memory / journal | `../codestable-core/playbooks/task-memory.md` |
| Minimality ladder | `../codestable-core/playbooks/minimality.md` |
| Real-repo reliability gates | `../codestable-core/playbooks/reliability.md` |
| Feature / issue / refactor execution | `../codestable-core/playbooks/{feature,issue,refactor}.md` |
| Audit-only execution block / handoff | `../codestable-core/playbooks/audit-only.md` |

`cs-do` does not onboard, create roadmap strategy, or write durable project knowledge. Missing skeleton or missing ready plan returns to `cs-plan`.

## Startup scan

1. Ensure `.codestable/INDEX.md` exists. If not, `Route: onboard.required`, `Next: plan`.
2. Read `.codestable/INDEX.md`, `.codestable/attention.md`, and `.codestable/reference/project-knowledge-contract.md`.
3. If a `.codestable/tasks/*/context-pack.md` exists for this work, read it before code.
4. Read the current lifecycle artifact: feature design/checklist, issue report/analysis, refactor design/checklist, audit ledger, or fastforward plan.
5. If the plan/context says audit-only is required, or the requested execution scope is a cross-module backend prompt/schema/status/event chain, read the completed audit ledger before touching code; if it is missing, partial, or lacks `Audit Status: 已审完`, stop with `blocked.missing-audit-ledger`.
6. Check `git status --short`; exclude unrelated dirty files.
7. Read touched code, tests, existing helpers/types/components/services, relevant scoped specs, and the task proof trace if present before editing.
8. Apply the minimality ladder; stop at the first rung that works without cutting safety.

## Fixed output protocol

Every response ends with:

```text
Route: <route-id>
Playbook: <codestable-core/playbooks/*.md#section or none>
Reason: <why execution is allowed or blocked>
Human Gate: none | owner-confirmation | design-approval | risk-approval | merge-approval
Owner decision: <known decision, pending question, or not-applicable>
Read: <plan/artifact/context/code/test/doc paths>
Evidence: <completed steps, diff scope, reuse proof, validation proof>
Evidence Level: L0 | L1 | L2 | L3 | L4
Reliability Gate: pass | blocked:<reason> | not-applicable
Minimality: rung=<rung>; reuse=<paths or none>; added-abstraction=<none/path+reason>
Task Memory: none | update:<path>
Proof Trace: none | update:<path>
Audit Ledger: not-applicable | missing | inline | create:<path> | update:<path> | read:<path> | complete:<path> | partial:<path>
Audit Status: not-applicable | 已审完 | 未审完
Journal: <path or none>
Write-intent: <actual changed scope or planned scope>
Checks: <commands/manual paths; if not run, why>
Next: review | plan | ask-user | stop
```

Legal `route-id` values:

```text
onboard.required
feature.fastforward.do
feature.standard.implement
issue.quickfix.do
issue.standard.fix
refactor.fastforward.do
refactor.standard.apply
blocked.need-plan
blocked.need-user-decision
blocked.dirty-worktree
blocked.missing-context-pack
blocked.missing-audit-ledger
blocked.missing-reproduction
blocked.missing-equivalence-proof
```

## Execution route table

| State / user request | Route | Action |
|---|---|---|
| No `.codestable/` | `onboard.required` | Stop; ask for `cs-plan：初始化 CodeStable` |
| Clear small feature or approved fastforward plan | `feature.fastforward.do` | Minimal scoped implementation and checks |
| Approved feature design/checklist | `feature.standard.implement` | Execute current checklist step and append evidence/journal |
| Clear root-cause bug with reproduction or no-repro rationale | `issue.quickfix.do` | Targeted fix and reproduction proof |
| Confirmed issue analysis / approved fix plan | `issue.standard.fix` | Implement only the chosen fix |
| Local behavior-preserving refactor with equivalence path | `refactor.fastforward.do` | Small equivalence-preserving change |
| Approved refactor design/checklist | `refactor.standard.apply` | Apply one verifiable slice at a time |
| No approved plan or safe fastforward boundary | `blocked.need-plan` | Return to `cs-plan` |
| New product/architecture/risk choice appears | `blocked.need-user-decision` | Stop and ask; do not guess |
| Unrelated dirty files obscure scope | `blocked.dirty-worktree` | Report and ask for scoping |
| Standard task has no context pack where one is expected | `blocked.missing-context-pack` | Return to `cs-plan` to create/update task memory |
| Audit-only was required but no completed file-level ledger is present | `blocked.missing-audit-ledger` | Return to `cs-plan` with `audit-only.backend-ledger`; do not edit source |
| Bug fix lacks reproduction, failing signal, or no-repro rationale | `blocked.missing-reproduction` | Return to `cs-plan` / issue analysis for failure evidence |
| Refactor lacks an equivalence proof path | `blocked.missing-equivalence-proof` | Return to `cs-plan` for characterization or verification plan |

## Real-repo execution gates

Before editing, confirm the task is executable in the current repository:

- Bug fix: reproduction path, failing test/log/user evidence, or explicit no-repro rationale exists.
- Refactor: equivalence proof path exists and behavior boundaries are named.
- Feature: success criteria, non-goals, code anchors, and validation path are known.
- Audit-required backend chain: a file-level audit ledger exists, all relevant rows are `done`, `Audit Status: 已审完` is present, prompt/schema path-field-caller-consumer mappings are complete, and the first fix is bounded.
- Any task: unrelated dirty files are excluded; task context/proof trace is read when present.

If the gate fails, return `blocked.*` and do not patch code. In particular, never patch audit-required work from a provisional or partial ledger.

## Minimality execution rules

Before new code, prove reuse was considered:

- search existing helpers/types/components/services/tests;
- prefer platform/stdlib/framework capability;
- do not add dependencies unless explicitly approved or already planned;
- do not create generic abstractions without real callers;
- fix shared root causes instead of patching every caller.

Small code is not enough: keep validation, security, accessibility, and data-safety checks.

## Task memory rules

For any task with `.codestable/tasks/*/journal.md`, append a short entry after meaningful progress:

```text
Did / Evidence / Checks / Blockers / Next route
```

Do not rewrite earlier entries. Ephemeral debugging stays in the journal; durable facts wait for `cs-review`.

## Product boundary

Implementation does not rewrite architecture, requirements, compound knowledge, or roadmap closure. It may mark a roadmap item `in-progress` when starting from an approved roadmap item; `done` and durable sync belong to `cs-review`.

## Completion standard

- Diff scope matches route and plan.
- Audit-required work references a completed audit ledger and implements only a bounded fix item from it.
- Checks or manual verification cover the changed behavior.
- Proof trace records before/after evidence for non-trivial tasks.
- Task journal/checklist/fix evidence is updated when relevant.
- Output `Next: review`, or clearly state why execution is blocked.
