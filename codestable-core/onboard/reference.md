# Onboard reference templates
## Document map

Use these templates when `cs-plan` runs onboard. They are code-informed templates, not empty skeletons:

- `.codestable/INDEX.md`
- `.codestable/architecture/ARCHITECTURE.md`
- `.codestable/requirements/VISION.md`
- `.codestable/compound/INDEX.md`
- `.codestable/attention.md`

## Template rules

Replace every `{...}` placeholder with observed facts or `unknown`. Do not leave generic “待补充” when the repo has code evidence. Use the confidence vocabulary: `observed`, `documented`, `inferred`, `unknown`.

## `.codestable/INDEX.md`

```markdown
# CodeStable Project Index

> 状态：code-informed
> 创建/刷新日期：YYYY-MM-DD
> 维护规则：索引只放摘要和链接；具体事实写入 architecture / requirements / roadmap / compound。

## 启动必读

- Attention: `attention.md`
- Knowledge contract: `reference/project-knowledge-contract.md`
- Code inventory: `reference/code-inventory.md` / `reference/code-inventory.json`
- Workflow conventions: `reference/workflow-conventions.md`

## 当前项目概览

- 项目简介：{from README or unknown}
- 主要技术栈：{observed stack hints from manifests}
- 包管理/构建：{observed package manager and key manifests}
- 关键入口：{observed app entrypoints, routes, CLIs, services}
- 测试入口：{observed test dirs and commands}

## 代码实况索引

| 主题 | 当前摘要 | 证据锚点 | 何时打开 |
|---|---|---|---|
| Architecture | 见 `architecture/ARCHITECTURE.md` | `{code anchors}` | 模块边界、数据流、API、配置、主流程相关时 |
| Requirements | 见 `requirements/VISION.md` | `{README/routes/UI anchors}` | 用户可见能力、业务规则、成功标准变化时 |
| Code inventory | 见 `reference/code-inventory.md` | `reference/code-inventory.json` | 不确定入口/模块/命令时 |
| Compound knowledge | 见 `compound/INDEX.md` | `{none initially}` | 决策、踩坑、技巧、探索结论影响当前工作时 |

## 当前进行中事项

- Features: `features/`
- Issues: `issues/`
- Refactors: `refactors/`
- Roadmaps: `roadmap/`
- Doc sweeps: `doc-sweeps/`

## 未确认 / 需要 owner 拍板

- {unknown or inferred product intent}

## 最近知识更新

<!-- cs-review managed: append short links to important index changes -->
```

## `.codestable/architecture/ARCHITECTURE.md`

```markdown
# {Project name} Architecture Index

> 状态：code-informed
> 创建/刷新日期：YYYY-MM-DD
> 事实来源：当前代码、manifests、README、测试和配置。

## 1. Observed stack

| Area | Observation | Confidence | Evidence |
|---|---|---|---|
| Runtime / language | {observed} | observed | `{manifest}` |
| Framework | {observed/inferred} | observed/inferred | `{config or entrypoint}` |
| Build / test | {observed} | observed | `{script or manifest}` |

## 2. Entrypoints and flows

| Entrypoint / flow | Current role | Evidence |
|---|---|---|
| `{path}` | {role} | observed |

## 3. Modules / subsystems

| Module | Current responsibility | Confidence | Code anchors | Detail doc |
|---|---|---|---|---|
| `{module}` | {responsibility} | observed/inferred | `{path}` | — |

## 4. Data / state / API anchors

| Area | Current observation | Evidence |
|---|---|---|
| Models / schema | {observed or unknown} | `{path or unknown}` |
| Routes / API | {observed or unknown} | `{path or unknown}` |
| Config / env | {observed or unknown} | `{path or unknown}` |

## 5. Known constraints and unknowns

- {observed constraints from tests/config}
- {unknowns requiring owner confirmation}

## 6. Index maintenance log

<!-- cs-review project-sync managed -->
```

## `.codestable/requirements/VISION.md`

```markdown
# Requirements Vision

> 状态：code-informed-initial
> 维护规则：这里只放能力摘要和链接；具体业务规则写入 `requirements/{slug}.md`。
> 注意：onboard 初稿中的能力可能来自 README、routes、UI 文案或测试名；未被用户确认的条目标为 `inferred-needs-owner-confirmation`。

## Current / observed capabilities

| Capability | Status | Summary | Evidence | Detail |
|---|---|---|---|---|
| `{capability}` | observed/documented/inferred-needs-owner-confirmation | {summary} | `{path}` | — |

## Draft / proposed capabilities

| Capability | Source | Open question | Detail |
|---|---|---|---|

## Outdated / superseded capabilities

| Capability | Superseded by | Note |
|---|---|---|
```

## `.codestable/compound/INDEX.md`

```markdown
# Compound Knowledge Index

> 状态：initialized
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

## `.codestable/attention.md`

```markdown
# Attention

本文件是 CodeStable 技能启动必读的短提醒入口。只记录每次都可能影响 plan/do/review 的项目特有规则。长解释写入 compound 并在此链接。

## Observed operational facts

### Build / run / test commands

- {observed command from package.json/Makefile/etc.}

### Environment / credentials

- {observed env/config requirement or unknown; never include secret values}

### Path conventions

- {observed source/test/generated directories}

## Owner-confirmation needed

- {inferred items that need confirmation}

## Project-specific warnings

<!-- knowledge-sync managed: append short confirmed warnings below -->
```
