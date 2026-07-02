# CodeStable

CodeStable is a Skill package for Codex / Claude Code that keeps software work grounded in the current repository. It gives the agent three public lifecycle entries: plan with evidence, execute the smallest ready change, then review and sync durable project knowledge.

It is meant to prevent common real-repo failures:

- lost context across sessions;
- fixes without reproduction or verification evidence;
- small requests turning into unnecessary frameworks;
- stale requirements, architecture, and README docs;
- unsafe document cleanup without current code anchors.

## Public Entries

| Entry | Purpose |
|---|---|
| `cs-plan` | Initialize or refresh project knowledge, explore code, route work, and create compact context packs |
| `cs-do` | Execute ready work, reuse existing code, apply the minimality ladder, and record evidence |
| `cs-review` | Verify changes, check overbuild, finish task memory, sync durable docs, and run code-grounded doc-sweeps |

Standalone utility Skills:

| Skill | Purpose |
|---|---|
| `git-commit` | Create a clean commit from staged changes |
| `business-flow-mapper` | Map a business process from code, docs, traces, or tests |

## Runtime Model

CodeStable stores project memory in the target repository under `.codestable/`:

- `requirements/`: capabilities, business rules, and success criteria;
- `architecture/`: current structure, boundaries, and code anchors;
- `specs/`: scoped engineering standards;
- `tasks/`: resumable context packs, journals, and proof traces;
- `features/`, `issues/`, `refactors/`, `roadmap/`: lifecycle artifacts;
- `compound/`: decisions, learnings, tricks, and explorations;
- `reference/code-inventory.*`: current implementation inventory;
- `doc-sweeps/`: audit reports for stale documentation.

Shared rules live in `codestable-core/playbooks/`. They are auditable references, not discoverable Skills.

## Common Commands

| Goal | Invocation |
|---|---|
| Initialize CodeStable for a repo | `cs-plan: initialize CodeStable for this repo` |
| Refresh knowledge from current code | `cs-plan: refresh .codestable from current implementation` |
| Explore code without editing | `cs-plan: explore the auth login flow without changing code` |
| Plan feature / bug / refactor work | `cs-plan: <your request>` |
| Execute ready work | `cs-do: continue the current feature / issue / refactor` |
| Review and sync docs | `cs-review: review and run Project Sync` |
| Run doc-sweep | `cs-review: run doc-sweep for auth` |
| Commit staged changes | `git-commit` |

## Reliability Rules

Public entries expose route, playbook, human gate, evidence level, reliability gate, minimality, task memory, and next step fields. Those fields make behavior debuggable.

Hard rules:

- bug fixes start from a failure signal, reproduction path, or no-repro rationale;
- refactors need a behavior boundary and equivalence proof path;
- non-trivial work leaves a proof trace;
- doc-sweep audits before mutation and never deletes without explicit path-by-path approval;
- minimality must not remove validation, permissions, security, data safety, or accessibility.

## Repository Layout

```text
.
├── cs-plan/
├── cs-do/
├── cs-review/
├── git-commit/
├── business-flow-mapper/
├── codestable-core/
│   ├── playbooks/
│   └── onboard/
└── docs/
```

See `docs/manual-operations.md`, `docs/runtime-structure.md`, and `docs/debugging.md` for operational details.
