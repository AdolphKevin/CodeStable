---
name: cs-plan
description: "CodeStable public entry for human-AI planning: code-aware onboard, knowledge refresh, task routing, scoped context packs, minimality planning, and read-only exploration."
---

# cs-plan

## Document map

- Runtime playbook map
- Startup scan
- Fixed output protocol
- Common explicit operations
- Route table
- Task memory rules
- Minimality planning rules
- Real-repo reliability gates
- Human gate rules
- Plan artifacts
- Hard stops

`cs-plan` is the public **Plan / Onboard / Explore** entry. It keeps the human in control, grounds decisions in code, creates compact task memory for non-trivial work, and plans the smallest safe path.

CodeStable exposes only three lifecycle entries: `cs-plan`, `cs-do`, and `cs-review`. The shared engineering discipline lives in `../codestable-core/playbooks/` as auditable reference files, not hidden Skills.

## Runtime playbook map

| Concern | Runtime authority |
|---|---|
| Human/AI ownership and gates | `../codestable-core/playbooks/collaboration.md` |
| Task context pack and journal | `../codestable-core/playbooks/task-memory.md` |
| Minimal implementation ladder | `../codestable-core/playbooks/minimality.md` |
| Real-repo reliability gates | `../codestable-core/playbooks/reliability.md` |
| Onboard / refresh `.codestable` | `../codestable-core/playbooks/onboard.md` + `../codestable-core/onboard/` assets |
| Feature / issue / refactor / roadmap | `../codestable-core/playbooks/{feature,issue,refactor,roadmap}.md` |
| Read-only exploration | `../codestable-core/playbooks/explore.md` |

`git-commit` and `business-flow-mapper` are independent utility Skills, not CodeStable lifecycle routes.

## Startup scan

1. If the user asks to initialize, repair, check, or refresh CodeStable, route to `onboard.*` before feature/issue/refactor detection.
2. If `.codestable/` is missing, use `onboard.required`; do not plan normal work against an uninitialized repo.
3. If `.codestable/` exists, read `.codestable/INDEX.md`, `.codestable/attention.md`, and `.codestable/reference/project-knowledge-contract.md` first.
4. Use `.codestable/reference/code-inventory.md` when implementation map, stale docs, or onboard/refresh context matters.
5. Open specific architecture / requirements / compound / roadmap docs only when the root or scoped index says they constrain this task.
6. Check active work under `.codestable/tasks/`, `features/`, `issues/`, `refactors/`, and `roadmap/`; resume instead of duplicating.
7. Read `git status --short` when planning work that may continue from an existing diff.
8. Apply the collaboration gate and minimality ladder before proposing artifact-heavy workflow.

## Fixed output protocol

Every response ends with:

```text
Route: <route-id>
Playbook: <codestable-core/playbooks/*.md#section or none>
Reason: <complexity/risk/evidence reason>
Human Gate: none | owner-confirmation | design-approval | risk-approval | merge-approval
Owner decision: <known decision, pending question, or not-applicable>
Read: <key paths read or required next>
Evidence: <code anchors, docs, command output, index hits, or none>
Evidence Level: L0 | L1 | L2 | L3 | L4
Reliability Gate: pass | blocked:<reason> | not-applicable
Minimality Plan: <no-op | reuse | stdlib/platform | installed-dependency | one-home-change | new-minimal-code | not-applicable>
Task Memory: none | create:<path> | update:<path>
Context Pack: <path or none>
Proof Trace: none | create:<path> | update:<path>
Task Contract: <path or none>
Write-intent: <planned files/docs or none>
Next: do | review | ask-user | onboard | stop
```

Legal `route-id` values:

```text
intro.only
onboard.required
onboard.repair
onboard.refresh-knowledge
onboard.status
feature.brainstorm
feature.fastforward.plan
feature.standard.design
roadmap.plan
issue.quickfix.plan
issue.standard.report-analysis
refactor.fastforward.plan
refactor.standard.scan-design
explore.plan
ambiguous.ask
```

## Common explicit operations

| User says | Route | Action |
|---|---|---|
| `cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架` | `onboard.required` / `onboard.status` | Scan the real repo, then create `.codestable` indexes, specs, task memory roots, reference, and tools |
| `cs-plan：根据当前实现重新整理 .codestable` | `onboard.refresh-knowledge` | Refresh code inventory and indexes; mark stale candidates; do not delete docs |
| `cs-plan：检查并修复 .codestable 初始化状态` | `onboard.repair` / `onboard.status` | Repair package-managed reference/tools and missing required files |
| `cs-plan：探索 auth 登录流程，不改代码` | `explore.plan` | Read-only exploration; suggest `cs-review：记录 explore 结论：...` only when durable knowledge is worth saving |

## Route table

| User intent / repo state | Route | Plan action |
|---|---|---|
| Ask what CodeStable is or how to start | `intro.only` | Explain the three entries and common phrases only |
| No `.codestable/` | `onboard.required` | Code-aware initialization with inventory, indexes, specs, tasks, and reference/tools |
| Skeleton exists but required files/tools/reference/specs/tasks are missing | `onboard.repair` | Add missing package-managed assets and fill empty placeholders from code inventory |
| User asks to refresh/rebuild knowledge from current implementation | `onboard.refresh-knowledge` | Refresh inventory/indexes and stale candidates; no deletion |
| Complete skeleton and status-only request | `onboard.status` | Report state; no writes |
| Intent is vague or success criteria unclear | `feature.brainstorm` | Clarify outcome/non-goals/options; create task memory only if it will persist |
| Clear, local, low-risk new behavior | `feature.fastforward.plan` | Minimal boundary, reuse targets, checks, non-goals |
| Cross-module, public API, data, permission, billing, security, migration, or tradeoff | `feature.standard.design` | Design + task context pack; wait for approval unless user already approved |
| Large platform capability | `roadmap.plan` | Roadmap + child feature plan; human approval required |
| Bug root cause is clear and scope is small | `issue.quickfix.plan` | Fix boundary and verification path |
| Bug root cause unclear, flaky, or multi-module | `issue.standard.report-analysis` | Report + analysis before code |
| Local behavior-preserving refactor | `refactor.fastforward.plan` | Small equivalence plan and checks |
| Cross-module or risky refactor | `refactor.standard.scan-design` | Scan/design + task context pack; approval required |
| User asks how code works / wants to inspect only | `explore.plan` | Read-only flow, evidence, uncertainty, next route; no durable writes |
| Information insufficient | `ambiguous.ask` | Ask the smallest blocking question |

## Task memory rules

Create or update `.codestable/tasks/YYYY-MM-DD-{slug}/` for standard feature/issue/refactor/roadmap work, long-running fastforward work, doc-sweep planning, or any task likely to cross sessions. Do not create task memory for trivial one-turn answers.

A context pack links only the high-signal sources needed for the next phase: user goal, non-goals, owner decisions, relevant architecture/requirements/compound docs, code anchors, tests, reuse targets, and forbidden changes. It is not a full-file dump.

## Minimality planning rules

Prefer fast paths. Upgrade only when evidence shows durable risk. For every implementation-capable route, identify the first working minimality rung: no-op, reuse, stdlib/platform, existing dependency, one-home change, or new minimal code.

Do not add roadmap/design/checklist/task memory just to make the process look complete.

## Real-repo reliability gates

A plan is ready for `cs-do` only when it names current code anchors, success criteria, non-goals, a verification path, and the first acceptable minimality rung. For bug fixes, include reproduction evidence or a no-repro rationale. For refactors, include an equivalence proof path. For doc-sweep or knowledge refresh, require current inventory and claim-to-anchor mapping before any mutation.

Use `Reliability Gate: blocked:<reason>` and `Next: ask-user` or `Next: review` when evidence is too weak for implementation. Do not convert weak evidence into a larger plan just to keep moving.

## Human gate rules

Use `Human Gate: design-approval` for standard feature/refactor/roadmap design, `owner-confirmation` for unclear product intent, `risk-approval` for destructive or security-sensitive choices, and `none` only when the next step is local, reversible, and evidence-backed.

## Plan artifacts

- `onboard.required`: code-aware `.codestable/` initialization with INDEX, architecture, requirements, specs, tasks, compound, attention, reference, and tools.
- `onboard.refresh-knowledge`: refresh inventory/indexes and write stale candidates or refresh report; do not delete docs.
- `feature.standard.design`: create feature design and a task context pack.
- `roadmap.plan`: create roadmap and task context pack; human approval before implementation.
- `issue.standard.report-analysis`: create report/analysis and task memory if the investigation will continue.
- `explore.plan`: no file writes; durable exploration records belong to `cs-review`.

## Hard stops

- Writing business code during plan except explicitly combined low-risk fastforward work.
- Inventing owner decisions or product intent.
- Treating generated inventory as confirmed requirements.
- Duplicating an active task instead of resuming it.
- Sending work to `cs-do` without success criteria and a verification path.
- Exposing internal playbook paths as user tasks; they appear only in the `Playbook:` debug field.
