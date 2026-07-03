# CodeStable 运行时结构

首次通过 `cs-plan` onboard 后，项目根下会生成 `.codestable/`。它是人与 AI 共同维护的软件生命周期知识库。

```text
.codestable/
├── INDEX.md                           # 项目知识总索引，三入口先读
├── attention.md                       # 每次启动必读短提醒
├── requirements/
│   ├── VISION.md                       # 能力/需求索引
│   └── {slug}.md
├── architecture/
│   ├── ARCHITECTURE.md                 # 架构索引
│   └── {type}-{slug}.md
├── specs/
│   ├── INDEX.md                        # scoped engineering standards
│   └── {scope}.md
├── tasks/
│   ├── INDEX.md                        # task capsule 总索引
│   └── YYYY-MM-DD-{slug}/
│       ├── task.md
│       ├── context-pack.md
│       ├── audit-ledger.md              # 可选：audit-only 文件级审计 ledger
│       ├── journal.md
│       ├── proof.md
│       └── status.yaml
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/
│   ├── INDEX.md
│   └── YYYY-MM-DD-{doc_type}-{slug}.md
├── tools/
│   ├── scan-project.py
│   ├── scan-codestable-docs.py
│   └── ...
└── reference/
    ├── project-knowledge-contract.md
    ├── human-ai-collaboration.md
    ├── task-memory-contract.md
    ├── minimality-ladder.md
    ├── specs-contract.md
    ├── code-inventory.json
    ├── code-inventory.md
    ├── workflow-conventions.md
    └── ...
```

## 知识层职责

- `INDEX.md`：只放摘要和链接，不写长事实。
- `attention.md`：短到每次都能读完的硬约束。
- `specs/`：Trellis 式 scoped specs，保存工程标准、测试命令、API/UI/data/security 约定。
- `tasks/`：Trellis 式 task memory，保存 context pack、audit ledger、journal 和 proof trace，让跨会话工作可恢复且可验证。
- `reference/code-inventory.*`：当前代码地图，onboard/refresh/doc-sweep 时刷新。
- `architecture/`：当前结构事实，必须有代码锚点或已验收 diff。
- `requirements/`：用户/系统能力事实；onboard 推断项要标 `inferred`。
- `compound/`：decision、learning、trick、explore 等可复用知识。
- `doc-sweeps/`：旧文档 lifecycle 报告，不默认删除。

## 维护入口归属

- 初始化、修复、刷新 `.codestable/`，以及 audit-only 后端链路 ledger：`cs-plan`。
- 执行代码改动：`cs-do`，不顺手改长期事实。
- 长期事实、索引、task finish、doc-sweep：`cs-review`。

## Runtime playbook

共享工程纪律只放在包级：

```text
codestable-core/playbooks/*.md
```

这些文件不是 Skill。需要调试时看三入口输出的 `Route / Playbook / Human Gate / Evidence / Audit Ledger / Task Memory / Minimality` 字段。
