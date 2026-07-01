# onboard 参考模板

本文件提供 the onboard executor reference 使用的骨架模板。

## Document map

Use this map first, then open only the template needed:

- `.codestable/INDEX.md` 项目知识总索引模板
- `.codestable/architecture/ARCHITECTURE.md` 占位模板
- `.codestable/requirements/VISION.md` 能力索引模板
- `.codestable/compound/INDEX.md` 长期知识索引模板
- `.codestable/attention.md` 最小模板


## 0. `.codestable/INDEX.md` 项目知识总索引模板

```markdown
# CodeStable Project Index

> 状态：骨架（待填充）
> 创建日期：YYYY-MM-DD
> 维护规则：索引只放摘要和链接；具体事实写入对应 architecture / requirements / roadmap / compound 文档。

## 启动必读

- Attention: `attention.md`
- Knowledge contract: `reference/project-knowledge-contract.md`
- System overview: `reference/system-overview.md`
- Workflow conventions: `reference/workflow-conventions.md`

## 当前项目概览

- 项目简介：待补充
- 主要技术栈：待补充
- 关键入口：待补充

## 知识索引

| 类别 | 索引入口 | 何时打开具体文档 |
|---|---|---|
| Requirements | `requirements/VISION.md` | 需求、能力边界、用户可见行为变化时 |
| Architecture | `architecture/ARCHITECTURE.md` | 模块边界、数据流、API、配置、主流程相关时 |
| Roadmap | `roadmap/` | 大需求、阶段拆解、子 feature 状态相关时 |
| Compound knowledge | `compound/INDEX.md` | 决策、踩坑、技巧、探索结论可能影响当前工作时 |

## 当前进行中事项

- Features: 查看 `features/`
- Issues: 查看 `issues/`
- Refactors: 查看 `refactors/`
- Roadmaps: 查看 `roadmap/`

## 最近知识更新

<!-- cs-review managed: append short links to important index changes -->
```

## 1. `.codestable/architecture/ARCHITECTURE.md` 占位模板

```markdown
# {项目名} 架构总入口

> 状态：骨架（待填充）
> 创建日期：YYYY-MM-DD

## 1. 项目简介

## 2. 核心概念 / 术语表

## 3. 子系统 / 模块索引

| 模块/子系统 | 当前职责 | 具体文档 | 代码锚点 |
|---|---|---|---|

## 4. 关键架构决定

| 决定 | 当前状态 | 详情/证据 |
|---|---|---|

## 5. 已知约束 / 硬边界

## 6. 索引维护记录

<!-- cs-review project-sync managed: update when architecture docs are added/renamed/outdated -->
```

## 1.5 `.codestable/requirements/VISION.md` 能力索引模板

```markdown
# Requirements Vision

> 状态：骨架（待填充）
> 维护规则：这里只放能力摘要和链接；具体业务规则写入 `requirements/{slug}.md`。

## Current capabilities

| Capability | Status | Summary | Detail |
|---|---|---|---|

## Draft / proposed capabilities

| Capability | Source | Open question | Detail |
|---|---|---|---|

## Outdated / superseded capabilities

| Capability | Superseded by | Note |
|---|---|---|
```

## 1.6 `.codestable/compound/INDEX.md` 长期知识索引模板

```markdown
# Compound Knowledge Index

> 状态：骨架（待填充）
> 维护规则：这里只放可检索摘要和链接；全文写入 `YYYY-MM-DD-{doc_type}-{slug}.md`。

## Decisions

| Topic | Status | Summary | Detail |
|---|---|---|---|

## Learnings

| Topic | Reuse trigger | Summary | Detail |
|---|---|---|---|

## Tricks

| Task | Use when | Detail |
|---|---|---|

## Explore records

| Area | Question answered | Detail |
|---|---|---|
```

## 2. `.codestable/attention.md` 最小模板

attention.md 是 CodeStable 技能启动必读的项目注意事项入口。onboard 创建最小骨架，不替项目 owner 填实质内容；后续短规则由 `cs-review` 的长期知识记录规则追加；长解释应写入 compound 并在此处链接。

```markdown
# Attention

本文件是 CodeStable 技能启动必读的项目注意事项入口。所有 CodeStable 入口开始工作前必须读取它。

## 项目碎片知识

<!-- knowledge-sync managed: new entries are appended below by cs-review Project Sync when needed -->

### 编译与构建

### 运行与本地起服务

### 测试

### 命令与脚本陷阱

### 路径与目录约定

### 环境变量与凭证

### 其他
```
