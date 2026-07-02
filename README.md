# CodeStable

CodeStable 是面向 Codex / Claude Code 的工程化开发任务管理 Skill 包。它把一次软件开发工作拆成三个公开入口：先规划和收集证据，再执行最小可验证改动，最后验收并把长期事实写回项目知识库。

它解决的不是“多加几个 Agent”，而是几个真实仓库里常见的问题：

- 任务跨会话后上下文丢失；
- AI 直接实现但没有复现、验证或等价证据；
- 小需求被做成大框架；
- README、架构文档、需求文档和当前代码逐渐失真；
- 文档清理缺少代码锚点，容易误删有效知识。

## 安装

```bash
npx skills add https://github.com/AdolphKevin/CodeStable
```

命令进入交互选择界面后，按 `a` 全选仓库内所有 skills，再按提示确认安装。

## 核心设计

CodeStable 只暴露三个生命周期入口：

| 入口 | 用途 |
|---|---|
| `cs-plan` | 初始化 / 刷新项目知识、探索代码、规划 feature / issue / refactor / roadmap，并生成必要的上下文包 |
| `cs-do` | 执行已经 ready 的工作，复用现有实现，应用最小实现规则，记录验证证据 |
| `cs-review` | 验收改动、检查过度设计、收口任务记忆、同步长期文档、执行代码证据优先的 doc-sweep |

另有两个独立工具 Skill：

| Skill | 用途 |
|---|---|
| `git-commit` | 基于 staged diff 生成规范提交 |
| `business-flow-mapper` | 从代码、文档或测试梳理业务流程图 |

## 工作方式

CodeStable 的项目知识默认进入目标仓库的 `.codestable/`：

- `requirements/`：用户可见能力、业务规则和成功标准；
- `architecture/`：当前架构事实、模块边界和代码锚点；
- `specs/`：测试命令、工程规范、API/UI/data/security 约定；
- `tasks/`：跨会话 task capsule、context pack、journal 和 proof trace；
- `features/`、`issues/`、`refactors/`、`roadmap/`：生命周期产物；
- `compound/`：decision、learning、trick、explore 等可复用知识；
- `reference/code-inventory.*`：当前代码实况库存；
- `doc-sweeps/`：文档熵减报告，默认不删除文件。

共享工程纪律放在本仓库的 `codestable-core/playbooks/`。这些文件不是可发现 Skill，而是三入口共同引用的可审计规则：

```text
codestable-core/playbooks/
├── collaboration.md     # human gate 和 owner 决策边界
├── task-memory.md       # task capsule / context pack / journal / proof trace
├── minimality.md        # 最小实现 ladder / overbuild review
├── reliability.md       # evidence level / bug-refactor-review 可靠性门槛
├── onboard.md
├── explore.md
├── feature.md
├── issue.md
├── refactor.md
├── roadmap.md
├── project-sync.md
└── knowledge-sync.md
```

## 常用调用

| 你想做的事 | 调用方式 |
|---|---|
| 初始化项目知识库 | `cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架` |
| 根据当前实现刷新知识 | `cs-plan：根据当前实现重新整理 .codestable` |
| 只读探索代码流程 | `cs-plan：探索 auth 登录流程，不改代码` |
| 规划新功能 / bug / 重构 | `cs-plan：<你的需求>` |
| 执行 ready 工作 | `cs-do：继续执行当前 feature / issue / refactor` |
| 验收改动并同步文档 | `cs-review：验收并做 Project Sync` |
| 清理过时文档 | `cs-review：做文档熵减，范围是 auth 模块` |
| 记录架构事实 | `cs-review：记录 architecture：<事实、边界、证据或代码锚点>` |
| 记录需求或业务规则 | `cs-review：记录 requirements：<能力、成功标准、边界>` |
| 记录技术决策 | `cs-review：记录 decision：<决定、背景、取舍、后果>` |
| 提交 staged 改动 | `git-commit` |

## 可靠性约束

每个入口都会输出可调试字段，例如：

```text
Route: ...
Playbook: ...
Human Gate: ...
Evidence Level: ...
Reliability Gate: ...
Minimality Plan / Minimality / Overbuild Check: ...
Task Memory: ...
Next: ...
```

这些字段用于判断：路由是否正确、证据是否足够、是否需要用户拍板、实现是否过度、任务是否可以继续或收口。

几个硬规则：

- bug fix 要从失败信号、复现路径或 no-repro 理由开始；
- refactor 要先说明行为边界和等价验证方式；
- 非平凡任务要留下 proof trace；
- doc-sweep 先做 claim matrix，删除 / 归档必须逐文件确认；
- minimality 不允许裁掉验证、安全、权限、数据安全或可访问性。

## 仓库结构

```text
.
├── cs-plan/                 # 规划入口 Skill
├── cs-do/                   # 执行入口 Skill
├── cs-review/               # 验收与同步入口 Skill
├── git-commit/              # 独立提交工具 Skill
├── business-flow-mapper/    # 独立业务流程梳理 Skill
├── codestable-core/
│   ├── playbooks/           # 三入口共享规则
│   └── onboard/             # 初始化模板和工具
└── docs/                    # 使用说明和设计说明
```

## 参考文档

- `docs/manual-operations.md`：三入口常用操作。
- `docs/three-command-mode.md`：三命令模式和职责边界。
- `docs/runtime-structure.md`：`.codestable/` 运行时结构。
- `docs/real-repo-reliability.md`：真实仓库证据等级和可靠性门槛。
- `docs/doc-sweep-safety.md`：文档熵减安全规则。
- `docs/debugging.md`：如何根据输出字段调试 CodeStable 行为。
- `docs/design-synthesis.md`：CodeStable / Trellis / Ponytail 的设计融合说明。
