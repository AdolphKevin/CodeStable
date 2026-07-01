# CodeStable Balanced Skill Consolidation Map

本包从原来的 32 个 CodeStable/utility Skill 压缩为 **5 个可发现 Skill**。目标是降低 Codex / Claude Code 的触发噪音，同时保留原来的工程纪律。

## Discoverable runtime Skills

| Skill | Role |
|---|---|
| `cs-plan` | Planning / routing / onboard / explore entry |
| `cs-do` | Execution entry |
| `cs-review` | Review / Project Sync / closure entry; explicit architecture/decision/knowledge record entry |
| `git-commit` | Independent utility, not part of CodeStable plan/do/review |
| `business-flow-mapper` | Independent utility, not part of CodeStable plan/do/review |

## Internal discipline preserved as references

| Runtime reference | Consolidated source discipline |
|---|---|
| `codestable-core/references/executors/onboard.md` | original onboarding skeleton, migration, tools, shared templates |
| `codestable-core/references/executors/feature.md` | feature entry, fastforward, design, implementation, acceptance, brainstorm |
| `codestable-core/references/executors/issue.md` | issue report, root-cause analysis, quickfix, standard fix, fix-note |
| `codestable-core/references/executors/refactor.md` | refactor entry, fastforward, standard scan-design-apply, equivalence verification |
| `codestable-core/references/executors/roadmap.md` | roadmap creation/update, item schema, interface contract discipline |
| `codestable-core/references/executors/project-sync.md` | architecture, requirements, roadmap status, manual sync, doc-sweep, audit discipline |
| `codestable-core/references/executors/knowledge-sync.md` | attention, decision, learning, trick, explore persistence, manual record, guide, libdoc discipline |
| `codestable-core/references/executors/explore.md` | direct code exploration route handled by `cs-plan` |

Historical source dumps are intentionally omitted from the runtime package so agents cannot accidentally read stale or conflicting rules. Keep historical material only in a separate development archive outside the runtime package.

## How removed stage commands are invoked now

| Old top-level concept | Runtime invocation |
|---|---|
| `cs-onboard` | `cs-plan：初始化 / 修复 / 检查 CodeStable` |
| `cs-explore` | `cs-plan：探索 <模块>，不改代码` |
| `cs-arch` / `cs-req` | `cs-review：记录 architecture / requirements：...` |
| `cs-decide` | `cs-review：记录 decision：...` |
| `cs-note` | 不保留泛化 `note` 入口；按内容归类为 `attention` / `learning` / `trick` / `decision` / `explore` 后用 `cs-review：记录 <type>：...` |
| `cs-learn` / `cs-trick` | `cs-review：记录 learning / trick：...` |

## Omitted from this runtime package

`browser-bridge` is not included. Package it separately as a browser automation utility when needed.

## Engineering discipline preservation

The package removes discoverable trigger surface, not process rules:

- public routing stays in `cs-plan` / `cs-do` / `cs-review`;
- detailed workflow rules stay once under package-level `codestable-core/`;
- project-level shared conventions are copied into `.codestable/reference/` during onboard;
- no runtime historical-source directory or stale source dump is included.
