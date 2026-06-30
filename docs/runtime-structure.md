# CodeStable 运行时结构

`/cs-onboard` 跑完后，会在你的项目根下生成一个 `codestable/` 目录。这是 CodeStable 所有产物的聚合根，也是各个子技能在运行时唯一会读写的工作区。

```text
你的项目/
├── codestable/
│   ├── requirements/                     # 需求实体
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
│   │   └── YYYY-MM-DD-{doc_type}-{slug}.md
│   ├── tools/                            # 共享脚本
│   └── reference/                        # 共享参考文档
│       ├── shared-conventions.md
│       ├── workflow-conventions.md
│       ├── system-overview.md
│       └── ...
└── AGENTS.md
```

## 要点

- 所有产物都聚在 `codestable/` 下，让历史 feature、bug 和决策容易检索。
- `requirements/` 和 `architecture/` 是长效档案，只记现状。
- `roadmap/` 是规划层，用于大需求拆解和接口契约。
- `features/`、`issues/`、`refactors/` 用 `YYYY-MM-DD-{slug}/` 聚合单次工作。
- 收尾阶段只做轻量知识沉淀判断；有明确复用价值的候选才路由到对应执行器。
- `compound/` 保存可检索的归档文档，learning、trick、decision、explore 通过 `doc_type` 字段区分。
- `attention.md` 不属于 compound，它保存每次 CodeStable 技能启动都必须知道的短提醒。
- `reference/` 由 `cs-onboard` 从技能包复制；要改共享口径或流程规则，改 `cs-onboard/reference/` 模板。

## 硬约束

Skill 是独立安装单元，运行时每个 skill 只能看到自己包内的文件。A 技能的 `SKILL.md` 里写 `B-skill/reference/xxx.md` 这种引用在运行时不可达。

跨 skill 共享的参考文档必须走工作项目这一层：由 `cs-onboard` 从技能包复制到项目的 `codestable/reference/`，其他 skill 用项目相对路径读取。
