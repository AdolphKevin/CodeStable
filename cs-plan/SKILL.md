---
name: cs-plan
description: CodeStable 用户可见三命令入口之一。用于代码实况初始化、项目知识刷新、任务规划、bug/重构/roadmap 判断和只读代码探索；输出可调试 route/playbook/evidence。
---

# cs-plan

`cs-plan` 是 CodeStable 的 **Planning / Onboard / Explore** 入口。它负责把用户诉求和当前仓库事实路由到正确 playbook，并产出可执行、不过度设计、可追踪的计划。

本 runtime 只暴露三个 CodeStable Skill：`cs-plan` / `cs-do` / `cs-review`。背后的规则是包级 `codestable-core/playbooks/` 里的可审计 playbook。不要调用或建议任何内部 Skill 名称。

## Runtime playbook map

| Route family | Runtime authority |
|---|---|
| `onboard.*` | `../codestable-core/playbooks/onboard.md` + `../codestable-core/onboard/` assets |
| `feature.*` | `../codestable-core/playbooks/feature.md` |
| `issue.*` | `../codestable-core/playbooks/issue.md` |
| `refactor.*` | `../codestable-core/playbooks/refactor.md` |
| `roadmap.*` | `../codestable-core/playbooks/roadmap.md` |
| `explore.plan` | `../codestable-core/playbooks/explore.md` |

`git-commit` 与 `business-flow-mapper` 是独立 utility Skill，不属于 CodeStable 生命周期。

## 启动扫描

1. **识别是否为 CodeStable 自身操作**：初始化、修复、刷新项目知识、检查状态、探索代码优先进入 `onboard.*` 或 `explore.plan`。
2. **确认 `.codestable/` 骨架**：
   - 不存在 → `Route: onboard.required`，执行代码实况初始化，不只是创建空骨架。
   - 存在但缺 `.codestable/INDEX.md`、`.codestable/attention.md`、`.codestable/reference/`、`.codestable/tools/`、`.codestable/requirements/VISION.md`、`.codestable/architecture/ARCHITECTURE.md`、`.codestable/compound/INDEX.md` → `Route: onboard.repair`。
   - 用户要求“重新整理 / 刷新 / 根据当前代码更新 .codestable” → `Route: onboard.refresh-knowledge`。
3. **读取项目知识入口**：骨架存在时先读 `.codestable/INDEX.md`、`.codestable/attention.md`、`.codestable/reference/project-knowledge-contract.md`；再按索引读取相关 architecture / requirements / compound / roadmap。
4. **恢复现场**：查看 `.codestable/features/`、`.codestable/issues/`、`.codestable/refactors/`、`.codestable/roadmap/` 是否有相关进行中事项；运行或查看 `git status --short` 判断是否有未收口变更。
5. **读用户原话**：如果只是介绍/流程问题，输出 `intro.only`；否则按路由表判断。
6. **保持小上下文**：小任务只读索引、attention 和相关代码入口；标准任务才打开具体长文档。

## 固定输出协议

每次结束都输出：

```text
Route: <route-id>
Playbook: <codestable-core/playbooks/*.md#section or none>
Reason: <为什么是这条路，必须包含复杂度/风险依据>
Read: <已经读取或应读取的关键路径列表>
Evidence: <代码锚点、文档锚点、命令、索引命中；没有则写 none>
Write-intent: <准备创建/更新的产物；无则写 none>
Next: <do | review | ask-user | onboard | stop>
```

合法 `route-id`：

```text
intro.only
onboard.required
onboard.repair
onboard.refresh-knowledge
onboard.status
feature.brainstorm
feature.fastforward.plan
feature.standard.design
roadmap.plan
issue.quickfix.plan
issue.standard.report-analysis
refactor.fastforward.plan
refactor.standard.scan-design
explore.plan
ambiguous.ask
```

## 常用显式操作

| 用户说法 | Route | 动作 |
|---|---|---|
| `cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架` | `onboard.required` / `onboard.status` | 没有骨架时先扫描当前项目，再创建代码实况索引和基础文档；已有完整骨架时报告状态 |
| `cs-plan：根据当前实现重新整理 .codestable` | `onboard.refresh-knowledge` | 刷新 code inventory、INDEX、ARCHITECTURE、VISION 和注意事项候选，不删除用户文档 |
| `cs-plan：检查并修复 .codestable 初始化状态` | `onboard.repair` / `onboard.status` | 补齐缺失 reference/tools/基础索引；不覆盖用户维护的细节文档 |
| `cs-plan：探索 auth 登录流程，不改代码` | `explore.plan` | 只读代码探索，输出证据、调用链、不确定点和长期记录候选；不落盘 |

显式 onboard / refresh 请求优先级高于 feature/issue/refactor 判断。

## 路由表

| 用户诉求 / 仓库状态 | Route | 计划动作 |
|---|---|---|
| 只问 CodeStable 是什么、该怎么开始 | `intro.only` | 只介绍三入口和常用说法；不要倒出内部 playbook 路径 |
| 没有 `.codestable/` | `onboard.required` | 按当前代码实况创建 `.codestable/`、索引、reference、tools |
| 有骨架但缺基础件 | `onboard.repair` | 补齐基础件；空/占位索引按代码实况更新 |
| 用户要求刷新、重建索引、按当前实现整理 `.codestable` | `onboard.refresh-knowledge` | 重新扫描代码并更新索引；旧事实只标记候选，不直接删除 |
| 骨架完整且只要求检查状态 | `onboard.status` | 只报告状态、缺口和下一步；`Write-intent: none` |
| 想法模糊、成功标准不清 | `feature.brainstorm` | 先收敛目标、用户、成功标准和非目标 |
| 清楚、局部、低风险的新功能 | `feature.fastforward.plan` | 最小实现边界、复用路径、验证方式、禁止事项 |
| 跨模块/公开接口/数据/权限/计费/安全/多方案取舍 | `feature.standard.design` | 写 feature design，确认后再抽 checklist |
| 大到塞不进单个 feature 的平台能力 | `roadmap.plan` | 拆 roadmap、子 feature、依赖和验收信号 |
| bug 根因明确、影响面小 | `issue.quickfix.plan` | 记录现象、修复边界、验证方式 |
| bug 根因不明、复现不稳、多模块 | `issue.standard.report-analysis` | 先 report + analysis，不直接写代码 |
| 局部行为不变重构 | `refactor.fastforward.plan` | 列 1-3 个低风险变更和等价验证 |
| 跨模块重构或行为等价难证明 | `refactor.standard.scan-design` | 先 scan 影响面，再 design/checklist |
| 只问“怎么实现/先摸一下/解释流程”且不要求改代码 | `explore.plan` | 只读探索，不落盘；若值得沉淀，建议 `cs-review：记录 explore 结论：...` |
| 信息不足 | `ambiguous.ask` | 一次只问最少关键问题 |

## 快路径升级条件

默认偏向快路径；只有命中下面条件才升级标准流程：跨 3 个以上子系统或所有权边界；用户可见能力边界变化；公开 API、数据库结构、权限、计费、安全、迁移、配置格式变化；根因不明或需要用户拍板；无测试保护但要求行为等价；已有 CodeStable 文档与当前任务冲突。

小任务不要为了“有记录”强行建 roadmap、design、checklist 或 acceptance。

## Plan 产物要求

- `onboard.required`：按 `../codestable-core/playbooks/onboard.md` 执行代码实况初始化，创建 `.codestable/`、扫描项目、生成填充过的 INDEX / ARCHITECTURE / VISION / attention 初稿。
- `onboard.repair`：只补齐缺失基础件；若索引仍是空模板，按代码实况补齐；不覆盖用户维护的具体文档。
- `onboard.refresh-knowledge`：重新扫描项目实现，更新 `.codestable/reference/code-inventory.*`、索引摘要和 stale 候选；不删除文档。
- `onboard.status`：只报告状态，`Write-intent: none`。
- `feature.fastforward.plan`：输出目标/非目标、预计改动、复用路径、验证方式、禁止事项。
- `feature.standard.design`：写 `.codestable/features/{YYYY-MM-DD}-{slug}/{slug}-design.md`。
- `roadmap.plan`：写 `.codestable/roadmap/{slug}/` 和 `{slug}-items.yaml`。
- `issue.standard.report-analysis`：先 report，再 analysis；根因确认后 `Next: do`。
- `explore.plan`：只读探索，禁止写 `.codestable/compound/`。

## 不做的事

- 不在 `cs-plan` 阶段直接写业务代码，除非用户明确把 plan/do 合并且任务是低风险快路径。
- 不把小任务升级成大型文档流程。
- 不静默修改历史 approved design / analysis；需要变更时写 addendum 或新版本。
- 不把内部 playbook 路径当成用户待办；路径只用于调试输出的 `Playbook:` 字段。
