# CodeStable Balanced Runtime v6

CodeStable Balanced Runtime 是一个面向 Codex / Claude Code 的工程化开发任务管理 Skill 包。原则是：**精简 Skill，而不是精简工程纪律；把规则显式化并保持可调试性。**

## 中心思想

CodeStable 的 `cs-plan` / `cs-do` / `cs-review` 三命令只是统一入口；真正被建模和编排的是软件生命周期里的稳定实体：`requirements`、`architecture`、`roadmap`、`feature`、`issue`、`refactor`、`decision`、`learning` 等。

三入口负责控制这些实体什么时候被创建、读取、更新或跳过：先规划事实和边界，再执行 ready 的最小改动，最后用证据验收，并只把改变项目长期事实或未来会复用的知识写回 `.codestable/`。

## 可发现 Skill

Runtime 包只包含 5 个可发现 `SKILL.md`：

| Skill | 作用 |
|---|---|
| `cs-plan` | 规划：代码实况初始化、项目知识刷新、代码探索、功能/bug/重构/roadmap 路由 |
| `cs-do` | 执行：推进 ready 的 feature / issue / refactor 工作 |
| `cs-review` | 验收与同步：验证结果、Project Sync、状态收口、代码证据优先的文档熵减、显式记录长期知识 |
| `git-commit` | 独立 utility：基于 staged diff 生成提交 |
| `business-flow-mapper` | 独立 utility：梳理业务流程 |

`git-commit` 与 `business-flow-mapper` 不是 CodeStable 生命周期的一部分。

## 背后是可审计 playbook

三入口共享的工程纪律位于：

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

这些文件不是 `SKILL.md`，不会被宿主发现为技能。它们是可审计 playbook：每个 route 的输入、证据、写权限和禁止事项都集中在一个权威文件里。三入口输出会带：

```text
Route: ...
Playbook: codestable-core/playbooks/<name>.md#<section>
Evidence: ...
```

效果不满意时，直接修改对应 playbook 的 route 小节即可调试。

## 常用调用

| 你想做的事 | 调用方式 |
|---|---|
| 初始化新项目 `.codestable/` | `cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架` |
| 根据当前实现重新整理项目知识 | `cs-plan：根据当前实现重新整理 .codestable` |
| 修复或检查 `.codestable/` | `cs-plan：检查并修复 CodeStable 初始化状态` |
| 只摸代码、解释流程、不改代码 | `cs-plan：探索 auth 登录流程，不改代码` |
| 规划新功能 / bug / 重构 / roadmap | `cs-plan：<你的需求>` |
| 执行已经 ready 的任务 | `cs-do：继续执行当前 feature / issue / refactor` |
| 验收本次改动并同步文档 | `cs-review：验收并做 Project Sync` |
| 文档熵减 / 清理过时文档 | `cs-review：做文档熵减，范围是 auth 模块` |
| 显式记录架构事实 | `cs-review：记录 architecture：<事实、边界、证据或代码锚点>` |
| 显式记录需求/业务规则 | `cs-review：记录 requirements：<能力、成功标准、边界>` |
| 显式记录技术决策 | `cs-review：记录 decision：<决定、背景、取舍、后果>` |
| 显式记录踩坑/技巧/探索结论/注意事项 | `cs-review：记录 learning/trick/explore/attention：<内容和证据>` |

详细语法见 `docs/manual-operations.md`。

## 代码实况初始化

`cs-plan：初始化 CodeStable` 不再只是创建空目录。它应该：

1. 复制 `.codestable/reference/` 和 `.codestable/tools/`；
2. 运行或等价执行 `scan-project.py` 生成 `reference/code-inventory.json` 和 `reference/code-inventory.md`；
3. 根据 README、manifests、entrypoints、routes、schemas、tests、config 生成代码实况版 `INDEX.md`、`architecture/ARCHITECTURE.md`、`requirements/VISION.md` 和 `attention.md`；
4. 对无法确认的产品意图标记 `inferred` / `unknown`，不编造事实。

已有项目可以用：

```text
cs-plan：根据当前实现重新整理 .codestable
```

这会刷新代码库存和索引，但不会删除用户维护的文档。

## 文档熵减安全边界

文档熵减使用：

```text
cs-review：做文档熵减，范围是 <模块/目录/全项目>
```

它会进入 `project-sync.doc-sweep`，要求先用当前代码和索引核验旧文档。默认只写 sweep report 和 lifecycle 标记，不删除文件。删除需要用户明确确认、逐文件列出和充分 evidence。

## 运行时目录

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

`.codestable/INDEX.md` 是每次 plan/do/review 的项目知识入口；review 写回长期事实时同时维护索引。

## 参考文档

- `docs/manual-operations.md` — 三入口下的初始化、刷新、探索、手动记录、doc-sweep 语法。
- `docs/three-command-mode.md` — 三命令模式与 playbook 拓扑。
- `docs/runtime-structure.md` — `.codestable/` 运行时结构。
- `docs/debugging.md` — 如何根据 `Route / Playbook / Evidence` 调试 CodeStable 行为。
- `docs/doc-sweep-safety.md` — 文档熵减的代码证据优先规则。
