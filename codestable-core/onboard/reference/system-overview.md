# CodeStable Balanced 体系总览

本文档由 `cs-plan` 的 onboard 路径复制到项目 `.codestable/reference/system-overview.md`。它说明 CodeStable Balanced 的三入口、运行时产物和路由原则。

## 用户心智：三入口

用户日常只需要记三条命令：

| 命令 | 作用 |
|---|---|
| `cs-plan` | 把事情定清楚：初始化、代码探索、功能方案、根因分析、roadmap、小任务边界 |
| `cs-do` | 推进当前 ready 的实现、修复或重构；没有 ready 输入就退回 plan |
| `cs-review` | 验证结果、Project Sync、状态收口和提交前范围确认 |

## 共享工程纪律：playbook，不是 Skill

共享工程纪律不以 `SKILL.md` 形式存在，而是由三入口读取包内 playbook，并在 onboard 后通过 `.codestable/reference/` 共享项目口径。

| Playbook | 负责内容 |
|---|---|
| onboard playbook | 初始化或修复 `.codestable/` 骨架、reference、tools |
| feature playbook | feature brainstorm / fastforward / design / checklist / implement / acceptance |
| issue playbook | bug report / root-cause analysis / quickfix / standard fix / fix-note |
| refactor playbook | fastforward refactor / standard scan-design-apply / behavior equivalence |
| roadmap playbook | 大需求拆解、roadmap 主文档、items.yaml 子 feature 清单 |
| project-sync playbook | architecture / requirements / roadmap / audit / doc-sweep 同步 |
| knowledge-sync playbook | attention / decision / learning / trick / explore / guide / libdoc 沉淀 |
| explore playbook | 定向代码探索，由 `cs-plan` 直接执行 |

工程纪律已收敛到上面的 runtime playbooks；用户只需要三入口。

## 独立 utility Skill

`git-commit` 与 `business-flow-mapper` 作为独立 Skill 保留，不属于 CodeStable plan/do/review 生命周期。

## 路由原则

| 场景 | 入口 route | Runtime authority |
|---|---|---|
| 仓库未接入 / 骨架缺失 | `onboard.required` / `onboard.repair` | onboard playbook |
| 只做代码理解，不改代码 | `explore.plan` | explore playbook |
| 想法模糊但可能是功能 | `feature.brainstorm` | feature playbook |
| 小功能 | `feature.fastforward.*` | feature playbook |
| 标准功能 | `feature.standard.*` | feature playbook |
| 大需求 / 平台能力 | `roadmap.plan` | roadmap playbook |
| 根因明确 bug | `issue.quickfix.*` | issue playbook |
| 根因不明 bug | `issue.standard.*` | issue playbook |
| 小重构 | `refactor.fastforward.*` | refactor playbook |
| 标准重构 | `refactor.standard.*` | refactor playbook |
| 验收后的项目事实同步 | Project Sync matrix | project-sync / knowledge-sync playbooks |

## 文档分层

- **requirements**：用户需要什么、系统提供什么能力来满足；可表示 draft/current/outdated。
- **architecture**：系统现在用什么结构实现；只记当前事实，不写未来计划。
- **roadmap**：接下来怎么分步做；大需求拆成可执行子 feature。
- **feature / issue / refactor**：单次行动的计划、执行证据和验收记录。
- **compound / attention**：长期知识、规则、技巧、探索证据和每次启动必须知道的短约束。

## 默认快路径，复杂再升级

默认生命周期是：

```text
Orient → Change → Check → Close
```

小 feature、小 bug、小重构走快路径；只有跨模块、新能力边界、高风险数据路径、根因不明、多方案取舍、公开接口变化、无测试却要求行为等价等情况，才升级到标准分阶段流程。

## Project Sync

`cs-review` 收口时统一判断：architecture、requirements、roadmap、compound、attention、guide/libdoc 是否需要回写。没有命中信号就写“无同步项”，不要为了完整感硬写文档。

## 进一步参考

- `.codestable/reference/shared-conventions.md` — 目录结构、YAML frontmatter 口径、checklist 生命周期。
- `.codestable/reference/workflow-conventions.md` — 最小实现纪律、质量检查、Project Sync、收尾 commit 约定。
- `.codestable/reference/tools.md` — 共享工具脚本用法。
- `.codestable/reference/maintainer-notes.md` — 断点恢复、新增工作流登记。
