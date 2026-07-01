# CodeStable Balanced 三命令模式

CodeStable Balanced 的目标是：**精简 Skill，而不是精简工程纪律**。

用户日常只需要记三条命令：

| Command | Purpose |
|---|---|
| `cs-plan` | 判断任务类型、复杂度、边界与下一步计划 |
| `cs-do` | 执行 ready 的 feature / issue / refactor 工作 |
| `cs-review` | 验证结果、Project Sync、状态收口 |

## Runtime guarantee

本包不依赖 frontmatter 可见性字段隐藏内部执行器。CodeStable runtime 里只有这 3 个可发现 CodeStable `SKILL.md`；内部执行器全部是包级 `codestable-core/` reference 文件，不是 Skill。

独立 utility Skill 保留为：

```text
git-commit
business-flow-mapper
```

## 显式操作层

只有 5 个可发现 Skill 并不意味着 onboard、architecture sync、decision record 消失。它们是三入口的显式 intent：

| 目标 | 用户说法 | Route |
|---|---|---|
| 初始化/修复/检查 `.codestable/` | `cs-plan：初始化 CodeStable` / `cs-plan：检查并修复 .codestable` | `onboard.required` / `onboard.repair` / `onboard.status` |
| 只读代码探索 | `cs-plan：探索 <模块>，不改代码` | `explore.plan` |
| 手动记录当前架构/需求/roadmap 状态 | `cs-review：记录 architecture/requirements/roadmap：...` | `project-sync.manual` |
| 手动记录决策/踩坑/技巧/注意事项 | `cs-review：记录 decision/learning/trick/attention：...` | `knowledge-sync.manual` |

详见 `docs/manual-operations.md`。

## Internal executor references

Route IDs are internal output labels, not user commands. User-facing follow-ups should say `cs-plan` / `cs-do` / `cs-review` with a concrete intent, not executor or sync route names.


| Public entry | Route family / sync target | Runtime reference |
|---|---|---|
| `cs-plan` | `onboard.*` | `../codestable-core/references/executors/onboard.md` + `../codestable-core/onboard/` |
| `cs-plan` | `explore.plan` | `../codestable-core/references/executors/explore.md` |
| `cs-plan` / `cs-do` / `cs-review` | `feature.*` | `../codestable-core/references/executors/feature.md` |
| `cs-plan` / `cs-do` / `cs-review` | `issue.*` | `../codestable-core/references/executors/issue.md` |
| `cs-plan` / `cs-do` / `cs-review` | `refactor.*` | `../codestable-core/references/executors/refactor.md` |
| `cs-plan` / `cs-review` | `roadmap.*` | `../codestable-core/references/executors/roadmap.md` |
| `cs-review` | project sync | `../codestable-core/references/executors/project-sync.md` |
| `cs-review` | knowledge sync | `../codestable-core/references/executors/knowledge-sync.md` |


## Stability rule

入口 Skill 必须自包含路由和固定输出协议，不能依赖读取其它 Skill 的 `SKILL.md` 才能决定下一步。跨入口 executor 口径走包级 `codestable-core/`，项目事实口径走项目层：`cs-plan` onboard 后释放 `.codestable/INDEX.md`、`.codestable/reference/` 和 `.codestable/tools/`，之后三个入口用项目索引定位具体知识。

## Project knowledge index rule

Every CodeStable entry starts from `.codestable/INDEX.md` and `.codestable/attention.md`. `cs-plan` uses index files to decide which architecture / requirement / compound / roadmap details to open; `cs-review` updates both detail files and indexes in the same closure step.

## Explore rule

`explore.plan` 由 `cs-plan` 直接执行定向代码探索；knowledge-sync 只负责在 `cs-review` 阶段把未来可复用的探索结论沉淀为 `.codestable/compound/*-explore-*.md`，不是探索执行器；`cs-plan` 的 `explore.plan` 不直接写 compound。

## Manual sync rule

`cs-review` 可以在没有当前代码 diff 的情况下记录架构、需求、决策或长期知识，但前提是用户明确要求，且有可追溯来源。manual sync 仍要输出 Writeback Matrix；证据不足时输出 `Next: ask-user`，不要编造长期事实。

## Roadmap writeback rule

Roadmap item 状态职责唯一化：

- `cs-do` 可在从 roadmap item 开始实现时标记 `in-progress`。
- `cs-review` Project Sync 在验收通过后统一标记 item 为 `done` 并同步主文档；阻塞或暂停写入 roadmap notes/status，不发明 schema 外的 item status。
- feature workflow 不直接关闭 roadmap。
