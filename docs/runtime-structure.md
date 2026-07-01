# CodeStable 运行时结构

首次通过 `cs-plan` onboard 后，项目根下会生成 `.codestable/`。它是 CodeStable 所有产物的聚合根，也是三个 CodeStable 入口在项目里读写长期知识的唯一工作区。

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
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/                         # 文档熵减报告
├── compound/
│   ├── INDEX.md
│   └── YYYY-MM-DD-{doc_type}-{slug}.md
├── tools/
│   ├── scan-project.py
│   ├── scan-codestable-docs.py
│   └── ...
└── reference/
    ├── project-knowledge-contract.md
    ├── code-inventory.json
    ├── code-inventory.md
    ├── shared-conventions.md
    ├── workflow-conventions.md
    ├── system-overview.md
    └── ...
```

## 知识新鲜度

- `INDEX.md`：只放摘要和链接，不写长事实。
- `code-inventory.*`：当前代码地图，onboard/refresh/doc-sweep 时刷新。
- `ARCHITECTURE.md`：当前结构事实，必须有代码锚点或已验收 diff。
- `VISION.md`：用户/系统能力索引，onboard 推断项要标 `inferred`。
- `compound/`：decision、learning、trick、explore 等可复用知识。
- `doc-sweeps/`：旧文档 lifecycle 报告，不默认删除。

## 维护入口归属

- 初始化、修复、刷新 `.codestable/`：`cs-plan` 的 `onboard.required` / `onboard.repair` / `onboard.refresh-knowledge`。
- 执行代码改动：`cs-do`，不顺手改长期事实。
- 长期事实、索引和文档熵减：`cs-review`。

## Runtime playbook

共享工程纪律只放在包级：

```text
codestable-core/playbooks/*.md
```

不要把同一规则复制到多个 Skill 目录；需要调试时看三入口输出的 `Playbook:` 字段。
