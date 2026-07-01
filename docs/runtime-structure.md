# CodeStable 运行时结构

首次通过 `cs-plan` 的 onboard 路由后，会在你的项目根下生成一个 `.codestable/` 目录。这是 CodeStable 所有产物的聚合根，也是三个 CodeStable 入口在项目里唯一会读写的工作区。初始化、修复和检查骨架都通过 `cs-plan` 执行，不需要单独的 onboard Skill。

```text
你的项目/
├── .codestable/
│   ├── INDEX.md                           # 项目知识总索引，三入口启动后先读
│   ├── requirements/                     # 需求实体
│   │   ├── VISION.md                       # 能力/需求索引
│   │   └── {slug}.md
│   ├── architecture/                     # 架构实体
│   │   ├── ARCHITECTURE.md
│   │   └── {type}-{slug}.md
│   ├── roadmap/                          # 大需求规划
│   │   └── {slug}/
│   │       ├── {slug}-roadmap.md
│   │       ├── {slug}-items.yaml
│   │       └── drafts/
│   ├── features/                         # 特性流程
│   │   └── YYYY-MM-DD-{slug}/
│   │       ├── {slug}-brainstorm.md
│   │       ├── {slug}-design.md
│   │       ├── {slug}-checklist.yaml
│   │       └── {slug}-acceptance.md
│   ├── issues/                           # 问题流程
│   │   └── YYYY-MM-DD-{slug}/
│   │       ├── {slug}-report.md
│   │       ├── {slug}-analysis.md
│   │       └── {slug}-fix-note.md
│   ├── refactors/                        # 重构流程
│   │   └── YYYY-MM-DD-{slug}/
│   │       ├── {slug}-scan.md
│   │       ├── {slug}-refactor-design.md
│   │       ├── {slug}-checklist.yaml
│   │       └── {slug}-apply-notes.md
│   ├── compound/                         # 可检索经验 / 长期规则 / 可复用处方
│   │   ├── INDEX.md                       # 长期知识索引
│   │   └── YYYY-MM-DD-{doc_type}-{slug}.md
│   ├── tools/                            # 共享脚本
│   └── reference/                        # 共享参考文档
│       ├── shared-conventions.md
│       ├── workflow-conventions.md
│       ├── system-overview.md
│       └── ...
```

## 显式记录入口

- 记录 architecture / requirements / roadmap 状态：使用 `cs-review：记录 architecture/requirements/roadmap：...`。
- 记录 decision / learning / trick / explore / attention：使用 `cs-review：记录 decision/learning/trick/explore/attention：...`；通用 note 必须先归类。
- 这些操作会进入 `project-sync.manual` 或 `knowledge-sync.manual`，仍需来源和证据，不会凭空写长期文档。

## 要点

- 所有产物都聚在 `.codestable/` 下，让历史 feature、bug 和决策容易检索。
- `requirements/` 和 `architecture/` 是长效档案，只记现状。
- `roadmap/` 是规划层，用于大需求拆解和接口契约。
- `features/`、`issues/`、`refactors/` 用 `YYYY-MM-DD-{slug}/` 聚合单次工作。
- `compound/` 保存可检索的归档文档，learning、trick、decision、explore 通过 `doc_type` 字段区分。
- `attention.md` 不属于 compound，它保存每次 CodeStable 技能启动都必须知道的短提醒。
- `.codestable/INDEX.md` 是每次 Plan/Do/Review 的项目知识总入口；索引只放摘要和链接，具体事实在 architecture / requirements / roadmap / compound 文档。
- `reference/` 和 `tools/` 由 `cs-plan` 的 onboard 路径从 `codestable-core/onboard/` 复制到项目。

## 硬约束

CodeStable runtime 把共享 executor reference 放在包级 `codestable-core/`，而不是复制到多个 Skill 目录。不要在一个 Skill 里依赖另一个 Skill 目录中的 reference；需要共享的规则只放 `codestable-core/` 一份。

跨入口共享项目事实必须走工作项目这一层：`cs-plan` onboard 释放 `.codestable/INDEX.md` 和 `.codestable/reference/`，之后三入口先读索引，再按需读具体文档。


## 维护入口归属

- `.codestable/` 初始化、修复和 reference/tools 刷新：通过 `cs-plan` 的 `onboard.required` / `onboard.repair` 完成。
- `.codestable/architecture/` 与 `.codestable/requirements/`：通过 `cs-review` 的 `project-sync.manual` 或验收后的 Project Sync 更新。
- `.codestable/compound/`、`.codestable/attention.md`、guide/libdoc：通过 `cs-review` 显式记录或验收后的长期知识同步更新。
- 普通 `cs-do` 不负责创建长期文档；它只记录执行证据并把收口交给 `cs-review`。
