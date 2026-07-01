# CodeStable Balanced Runtime

CodeStable Balanced Runtime 是一个面向 Codex / Claude Code 的工程化开发任务管理 Skill 包。它的原则是：**精简 Skill，而不是精简工程纪律**。

## 可发现 Skill

Runtime 包只包含 5 个可发现 `SKILL.md`：

| Skill | 作用 |
|---|---|
| `cs-plan` | 规划：判断任务类型、边界、复杂度、产物和下一步；也承接初始化与代码探索 |
| `cs-do` | 执行：推进 ready 的 feature / issue / refactor 工作 |
| `cs-review` | 验收与同步：验证结果、Project Sync、状态收口；也承接显式记录架构/决策/经验 |
| `git-commit` | 独立 utility：基于 staged diff 生成提交 |
| `business-flow-mapper` | 独立 utility：梳理业务流程 |

`git-commit` 与 `business-flow-mapper` 不是 CodeStable 生命周期的一部分，不参与 `cs-plan` / `cs-do` / `cs-review` 路由。

## 显式操作怎么调用

内部执行器不再是独立 Skill，但操作没有消失。请通过三入口表达意图：

| 你想做的事 | 调用方式 |
|---|---|
| 初始化新项目 `.codestable/` | `cs-plan：初始化 CodeStable / onboard this repo` |
| 修复或检查 `.codestable/` 骨架 | `cs-plan：检查并修复 CodeStable 初始化状态` |
| 只摸代码、解释流程、不改代码 | `cs-plan：探索 auth 登录流程，不改代码` |
| 规划新功能 / bug / 重构 / roadmap | `cs-plan：<你的需求>` |
| 执行已经 ready 的任务 | `cs-do：继续执行当前 feature / issue / refactor` |
| 验收本次改动并同步文档 | `cs-review：验收并做 Project Sync` |
| 显式记录当前架构事实 | `cs-review：记录 architecture：<事实、边界、证据或代码锚点>` |
| 显式记录需求/业务规则 | `cs-review：记录 requirements：<能力、成功标准、边界>` |
| 显式记录技术决策 | `cs-review：记录 decision：<决定、背景、取舍、后果>` |
| 显式记录踩坑/技巧/探索结论/注意事项 | `cs-review：记录 learning/trick/explore/attention：<内容和证据>` |

详细语法见 `docs/manual-operations.md`。

## Balanced runtime 拓扑

CodeStable 的内部工程纪律保留为 reference，而不是顶层 Skill：

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

这些 reference 集中在包级 `codestable-core/` 下，三入口只通过相对路径读取同一份权威规则，不再复制 feature / issue / refactor / roadmap executor。即使宿主只按 `SKILL.md` 文件发现技能，也不会把内部执行器作为 Skill 发现或触发。

## 运行时目录

CodeStable 在项目里使用统一目录：

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

`.codestable/reference/` 和 `.codestable/tools/` 由 `cs-plan` 的 onboard 路径从 `codestable-core/onboard/` 释放到项目，供三个 CodeStable 入口在项目层共享。`.codestable/INDEX.md` 是每次 plan/do/review 的项目知识入口；review 写回长期事实时同时维护索引。

## 常见流程

```text
新项目：       cs-plan → onboard.required / onboard.repair / onboard.status
代码探索：     cs-plan → explore.plan
小功能：       cs-plan → feature.fastforward.plan → cs-do → cs-review
标准功能：     cs-plan → feature.standard.design → cs-do → cs-review
不明 bug：     cs-plan → issue.standard.report-analysis → cs-do → cs-review
明确 bug：     cs-plan → issue.quickfix.plan → cs-do → cs-review
小重构：       cs-plan → refactor.fastforward.plan → cs-do → cs-review
大需求：       cs-plan → roadmap.plan → 子 feature 逐个执行
手动架构记录： cs-review：记录 architecture：...
手动决策记录： cs-review：记录 decision：...
```

## 参考文档

- `docs/manual-operations.md` — 三入口下的显式初始化、探索、手动记录语法。
- `docs/three-command-mode.md` — 三命令模式与 runtime reference 拓扑。
- `docs/skill-consolidation-map.md` — 旧 Skill 到 runtime reference 的合并映射。
- `docs/runtime-structure.md` — `.codestable/` 运行时结构。
