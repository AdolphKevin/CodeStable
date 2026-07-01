# CodeStable Balanced Runtime v6

CodeStable Balanced Runtime is an engineering task-management Skill package for Codex / Claude Code. Principle: **reduce discoverable Skills without reducing engineering discipline; keep workflows debuggable instead of hiding old flows.**

## Core Idea

`cs-plan` / `cs-do` / `cs-review` are only the unified entries. The real orchestration target is the stable software-lifecycle entities: `requirements`, `architecture`, `roadmap`, `feature`, `issue`, `refactor`, `decision`, `learning`, and related project knowledge.

The three entries control when those entities are created, read, updated, or skipped: plan facts and boundaries first, execute the smallest ready change, then verify with evidence and write back only long-term project facts or reusable knowledge into `.codestable/`.

## Discoverable Skills

The runtime package contains only 5 discoverable `SKILL.md` files:

| Skill | Purpose |
|---|---|
| `cs-plan` | Planning: code-aware onboarding, project knowledge refresh, code exploration, feature/bug/refactor/roadmap routing |
| `cs-do` | Execution: implement ready feature / issue / refactor work |
| `cs-review` | Review and sync: verify results, Project Sync, closure, code-grounded doc-sweep, explicit long-term knowledge records |
| `git-commit` | Standalone utility: generate commits from staged diff |
| `business-flow-mapper` | Standalone utility: map business flows |

`git-commit` and `business-flow-mapper` are not part of the CodeStable lifecycle.

## Behind the entries: playbooks, not discoverable Skills

Shared engineering discipline lives in:

```text
codestable-core/playbooks/
├── onboard.md
├── explore.md
├── feature.md
├── issue.md
├── refactor.md
├── roadmap.md
├── project-sync.md
└── knowledge-sync.md
```

These files are not `SKILL.md` files and are not discoverable Skills. They are auditable playbooks: each route has one authoritative place for inputs, evidence, write ownership, and hard stops. The three entries emit:

```text
Route: ...
Playbook: codestable-core/playbooks/<name>.md#<section>
Evidence: ...
```

When behavior is not satisfactory, edit the relevant route section in the playbook.

## Common invocations

| Goal | Invocation |
|---|---|
| Initialize `.codestable/` for a project | `cs-plan: initialize CodeStable for this repo` |
| Rebuild project knowledge from current implementation | `cs-plan: refresh .codestable from current implementation` |
| Repair or check `.codestable/` | `cs-plan: check and repair CodeStable initialization` |
| Read-only code exploration | `cs-plan: explore the auth login flow without changing code` |
| Plan a feature / bug / refactor / roadmap | `cs-plan: <your request>` |
| Execute ready work | `cs-do: continue the current feature / issue / refactor` |
| Review changes and sync docs | `cs-review: review and run Project Sync` |
| Reduce documentation entropy | `cs-review: run doc-sweep for auth` |
| Record architecture facts | `cs-review: record architecture: <fact, boundary, evidence or code anchor>` |
| Record requirements/business rules | `cs-review: record requirements: <capability, success criteria, boundary>` |
| Record decisions | `cs-review: record decision: <decision, context, tradeoff, consequence>` |
| Record learning/trick/explore/attention | `cs-review: record learning/trick/explore/attention: <content and evidence>` |

## Code-aware onboarding

`cs-plan: initialize CodeStable` is not a skeleton-only operation. It should copy runtime assets, generate `reference/code-inventory.json` and `reference/code-inventory.md`, then create code-informed `INDEX.md`, `architecture/ARCHITECTURE.md`, `requirements/VISION.md`, and `attention.md` from README, manifests, entrypoints, routes, schemas, tests, and config. Unconfirmed product intent must be labeled `inferred` or `unknown`.

For existing projects use:

```text
cs-plan: refresh .codestable from current implementation
```

This refreshes the inventory and indexes without deleting user-maintained documents.

## Doc-sweep safety

Use:

```text
cs-review: run doc-sweep for <module/scope>
```

It routes to `project-sync.doc-sweep`, verifies old docs against current code and indexes, writes a sweep report by default, and does not delete files unless the user explicitly confirms a file-by-file deletion list with sufficient evidence.

## Runtime directory

```text
.codestable/
├── INDEX.md
├── attention.md
├── requirements/VISION.md
├── architecture/ARCHITECTURE.md
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/INDEX.md
├── tools/
└── reference/
    ├── project-knowledge-contract.md
    ├── code-inventory.json
    ├── code-inventory.md
    ├── shared-conventions.md
    ├── workflow-conventions.md
    └── system-overview.md
```

`.codestable/INDEX.md` is the project knowledge entry point for every plan/do/review run.
