# CodeStable Balanced Runtime

CodeStable Balanced Runtime is a repository-local engineering workflow Skill package for Codex / Claude Code. Its principle is: **simplify Skills, not engineering discipline**.

## Discoverable Skills

The runtime package contains only 5 discoverable `SKILL.md` files:

| Skill | Purpose |
|---|---|
| `cs-plan` | Plan: classify work type, scope, complexity, artifacts, and next step; also handles onboarding and code exploration |
| `cs-do` | Do: execute ready feature / issue / refactor work |
| `cs-review` | Review and sync: verify results, run Project Sync, close state; also handles explicit architecture / decision / knowledge records |
| `git-commit` | Independent utility: generate commits from staged diffs |
| `business-flow-mapper` | Independent utility: map business flows |

`git-commit` and `business-flow-mapper` are not part of the CodeStable plan/do/review lifecycle.

## How to invoke explicit operations

Internal executors are no longer separate Skills, but their operations are still available through the three public entries:

| Goal | Invocation |
|---|---|
| Initialize `.codestable/` in a new repo | `cs-plan: initialize CodeStable / onboard this repo` |
| Repair or inspect the `.codestable/` skeleton | `cs-plan: check and repair CodeStable onboarding` |
| Explore code without changing it | `cs-plan: explore the auth login flow without editing code` |
| Plan a feature / bug / refactor / roadmap | `cs-plan: <your request>` |
| Execute ready work | `cs-do: continue the current feature / issue / refactor` |
| Review changes and sync docs | `cs-review: review this change and run Project Sync` |
| Explicitly record architecture facts | `cs-review: record architecture: <fact, boundary, evidence, code anchors>` |
| Explicitly record requirements or business rules | `cs-review: record requirements: <capability, criteria, boundary>` |
| Explicitly record a technical decision | `cs-review: record decision: <decision, context, tradeoff, consequence>` |
| Explicitly record learning/trick/explore/attention | `cs-review: record learning/trick/explore/attention: <content and evidence>` |

See `docs/manual-operations.en.md` for details.

## Balanced runtime topology

CodeStable's internal engineering discipline is preserved as references, not top-level Skills:

```text
onboard executor reference
feature workflow reference
issue workflow reference
refactor workflow reference
roadmap workflow reference
project-sync workflow reference
knowledge-sync workflow reference
explore executor reference
```

These references are centralized under package-level `codestable-core/`. The three entries read the same authoritative executor files by relative path, so feature / issue / refactor / roadmap rules are not copied across Skill directories. Even if a host discovers skills solely by `SKILL.md` files, it cannot discover internal executors as Skills because they are not `SKILL.md` files.

## Runtime directory

CodeStable uses one project-local runtime root:

```text
.codestable/
├── INDEX.md
├── attention.md
├── requirements/
│   └── VISION.md
├── architecture/
│   └── ARCHITECTURE.md
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/
│   └── INDEX.md
├── tools/
└── reference/
    ├── project-knowledge-contract.md
    ├── shared-conventions.md
    ├── workflow-conventions.md
    ├── system-overview.md
    └── tools.md
```

`.codestable/reference/` and `.codestable/tools/` are released by the `cs-plan` onboarding route from `codestable-core/onboard/`, then shared by all three CodeStable entries at the project layer. `.codestable/INDEX.md` is the startup knowledge index for every CodeStable entry, and `cs-review` keeps indexes fresh when durable facts change.

## Common flows

```text
New repo:             cs-plan → onboard.required / onboard.repair / onboard.status
Code exploration:     cs-plan → explore.plan
Small feature:        cs-plan → feature.fastforward.plan → cs-do → cs-review
Standard feature:     cs-plan → feature.standard.design → cs-do → cs-review
Unknown-root bug:     cs-plan → issue.standard.report-analysis → cs-do → cs-review
Known-root bug:       cs-plan → issue.quickfix.plan → cs-do → cs-review
Small refactor:       cs-plan → refactor.fastforward.plan → cs-do → cs-review
Large initiative:     cs-plan → roadmap.plan → child features
Manual architecture:  cs-review: record architecture: ...
Manual decision:      cs-review: record decision: ...
```

## References

- `docs/manual-operations.en.md` — explicit onboarding, exploration, and manual record syntax through the three entries.
- `docs/three-command-mode.md` — three-command mode and runtime reference topology.
- `docs/skill-consolidation-map.md` — consolidation map from old Skills to runtime references.
- `docs/runtime-structure.md` — `.codestable/` runtime structure.
