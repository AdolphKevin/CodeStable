---
name: cs-plan
description: CodeStable 用户可见三命令入口之一。用于规划新功能、bug、重构、大需求、代码探索或未接入仓库；自包含完成启动扫描、路由判断、explore 执行和 onboarding 路径，不依赖内部 Skill 触发。
---

# cs-plan

`cs-plan` 是 CodeStable 对用户暴露的 **Planning 入口**。它负责把用户诉求和当前仓库状态路由到正确工作类型，并产出可执行、不过度设计的 plan。

本 runtime 包只暴露三个 CodeStable Skill：`cs-plan` / `cs-do` / `cs-review`。内部执行器不是 `SKILL.md`，而是包级 `codestable-core/` reference 文件；不要调用、建议或等待任何内部 Skill 名称。

## Runtime reference map

| Route family | Runtime authority |
|---|---|
| `onboard.*` | `../codestable-core/references/executors/onboard.md` + `../codestable-core/onboard/` templates |
| `feature.*` | `../codestable-core/references/executors/feature.md` |
| `issue.*` | `../codestable-core/references/executors/issue.md` |
| `refactor.*` | `../codestable-core/references/executors/refactor.md` |
| `roadmap.*` | `../codestable-core/references/executors/roadmap.md` |
| `explore.plan` | `../codestable-core/references/executors/explore.md` |

`git-commit` 与 `business-flow-mapper` 是独立 utility Skill，不属于 CodeStable plan/do/review 生命周期。

## 启动扫描

收到调用后先做这些检查，再回复或落盘：

1. **确认 CodeStable 骨架**：检查项目根是否存在 `.codestable/`。
   - 不存在 → `Route: onboard.required`，按 `../codestable-core/references/executors/onboard.md` 搭骨架，不要直接 feature / issue / refactor。
   - 存在但 `.codestable/INDEX.md`、`.codestable/attention.md`、`.codestable/reference/`、`.codestable/tools/`、`.codestable/requirements/VISION.md`、`.codestable/architecture/ARCHITECTURE.md` 或 `.codestable/compound/INDEX.md` 缺失 → `Route: onboard.repair`，先修复骨架。
2. **读取项目知识入口**：骨架存在时必须先读 `.codestable/INDEX.md` 和 `.codestable/attention.md`；再按需读 `.codestable/reference/project-knowledge-contract.md`、`.codestable/reference/system-overview.md`、`.codestable/reference/workflow-conventions.md` 的相关段落。
3. **按索引定位具体知识**：先读索引级文档（`requirements/VISION.md`、`architecture/ARCHITECTURE.md`、`compound/INDEX.md`、相关 roadmap index），只在任务命中某个模块/能力/决策时再打开具体文档；不要全量扫描长期文档。
4. **恢复现场**：查看 `.codestable/features/`、`.codestable/issues/`、`.codestable/refactors/`、`.codestable/roadmap/` 下是否有相关进行中事项；运行或查看 `git status --short` 判断是否有未收口变更。
5. **读用户原话**：先识别是否只是介绍 / 询问流程；否则按路由表判断。
6. **只读必要上下文**：小任务只读 INDEX + attention + 相关代码入口；标准任务才通过索引进入相关 architecture / requirements / compound / roadmap 具体文档。

## 固定输出协议

每次结束都输出：

```text
Route: <route-id>
Reason: <为什么是这条路，必须包含复杂度/风险依据>
Read: <已经读取或应读取的关键路径列表>
Write-intent: <准备创建/更新的产物；无则写 none>
Next: <do | review | ask-user | onboard | stop>
```

合法 `route-id`：

```text
intro.only
onboard.required
onboard.repair
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

这些操作不再通过单独的内部 Skill 名称调用，而是通过 `cs-plan` 的路由执行：

```text
cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架。
cs-plan：onboard this repo for CodeStable.
cs-plan：检查并修复 .codestable 初始化状态。
cs-plan：探索 auth 登录流程，不改代码，只列关键文件和不确定点。
```

`cs-plan` 必须根据实际骨架状态输出 `onboard.required`、`onboard.repair` 或 `onboard.status`，而不是建议用户调用不存在的 `cs-onboard`。

## 路由表

| 用户诉求 / 仓库状态 | Route | 计划动作 |
|---|---|---|
| 只问 CodeStable 是什么、该怎么开始 | `intro.only` | 只介绍三入口：`cs-plan` / `cs-do` / `cs-review`；不要倒出内部 reference 名称 |
| 用户明确要求初始化 / onboard / 检查 CodeStable | `onboard.required` / `onboard.repair` / `onboard.status` | 按当前骨架状态创建、修复或只报告；不要覆盖已有项目文档 |
| 没有 `.codestable/` | `onboard.required` | 先搭 `.codestable/` 骨架、reference 和 tools |
| 有 `.codestable/` 但缺 INDEX / attention / reference / tools / VISION / ARCHITECTURE / compound INDEX 等基础件 | `onboard.repair` | 补齐骨架，之后再规划具体任务 |
| `.codestable/` 骨架完整，用户只要求检查初始化状态 | `onboard.status` | 报告已具备的目录、缺失风险和下一步；不写无关文件 |
| 想法模糊、目标/成功标准/边界还没收敛 | `feature.brainstorm` | 先讨论真实问题、用户、成功标准和非目标，不急着写 design |
| 清楚、局部、低风险的新功能 | `feature.fastforward.plan` | 只给最小实现边界、验证方式、禁止事项；默认不建 design/checklist |
| 新功能涉及跨模块、公开接口、数据结构、权限/计费/安全、高风险路径或多方案取舍 | `feature.standard.design` | 写 feature design，拍板后抽 checklist |
| “权限系统 / 通知中心 / SSO / 多阶段平台能力”这类大到塞不进单个 feature 的需求 | `roadmap.plan` | 先拆 roadmap、子 feature、接口契约和依赖顺序 |
| bug 根因明确、影响面小、修复点清楚 | `issue.quickfix.plan` | 记录现象、修复边界、验证命令；下一步可直接 `cs-do` 修并写 fix-note |
| bug 根因不明、复现不稳、多模块或高风险 | `issue.standard.report-analysis` | 先 report + analysis，定位根因和候选方案，不直接写代码 |
| 单函数/单组件/局部性能或可读性优化，行为不变且测试可自证 | `refactor.fastforward.plan` | 列 1-3 个低风险变更和等价验证；默认不建 refactors 目录 |
| 跨模块重构、公开接口调整、行为等价难证明、无测试保护 | `refactor.standard.scan-design` | 先 scan 影响面，再写 refactor design/checklist |
| 用户问“这个模块怎么实现 / 先摸一下代码 / 解释这段流程”且没有要求改代码 | `explore.plan` | 由 `cs-plan` 直接执行定向代码探索，输出证据和结论；不落盘，需沉淀时交给 `cs-review` |
| 需求太抽象，缺少目标/成功标准/现象/边界 | `ambiguous.ask` | 一次只问最少的关键问题，不硬猜 |


## 显式子命令 / intent alias

`cs-plan` 承接所有“开始前要想清楚”的操作，包括初始化和代码探索。用户不需要、也不能依赖内部 `cs-onboard` / `cs-explore` Skill。

| 用户显式说法 | Route | 执行动作 |
|---|---|---|
| `cs-plan：初始化 CodeStable` / `onboard 这个仓库` / `为这个项目创建 .codestable` | `onboard.required` / `onboard.status` | 没有骨架时创建 `.codestable/`、`INDEX.md`、`attention.md`、`requirements/VISION.md`、`architecture/ARCHITECTURE.md`、`compound/INDEX.md`、`reference/`、`tools/`；已有完整骨架时只报告状态 |
| `cs-plan：修复 .codestable` / `刷新 CodeStable reference/tools` / `升级骨架` | `onboard.repair` / `onboard.status` | 缺失时补齐目录和基础 reference/tools；完整时不覆盖用户维护的业务文档 |
| `cs-plan：探索/摸一下/解释 <模块>`，且用户没有要求改代码 | `explore.plan` | 执行定向代码探索，输出证据、入口、调用链、风险和下一步建议；不落盘，需沉淀时交给 `cs-review` |

显式 onboard 请求优先级高于 feature/issue/refactor 判断：即使仓库已经有代码，只要用户要求初始化或修复 CodeStable，先完成 onboard/repair，不顺手开始业务任务。

## 快路径与标准流程的升级条件

默认偏向快路径；只有命中下面条件才升级标准流程：

- 跨 3 个以上子系统或所有权边界。
- 新增或改变用户可见能力边界。
- 改公开 API、数据库结构、权限、计费、安全、数据迁移、配置格式。
- 根因不明、多候选方案、需要用户拍板。
- 无测试保护但要求行为等价。
- 已有 `.codestable/` 文档中有相关 decision / requirement / architecture 冲突。

小任务不要为了“有记录”强行建 roadmap、design、checklist 或 acceptance；这会污染长期记忆。

## Plan 产物要求

### `onboard.required` / `onboard.repair` / `onboard.status`

按 `../codestable-core/references/executors/onboard.md` 执行。`cs-plan` 是 onboard 的唯一入口；不要依赖不可发现的内部 Skill。

- `onboard.required`：创建 `.codestable/` 骨架、reference 和 tools。
- `onboard.repair`：只补齐缺失基础件，不覆盖已有项目文档。
- `onboard.status`：骨架完整时只报告状态和推荐下一步，`Write-intent: none`。

### `feature.fastforward.plan`

输出轻量计划：目标和非目标、预计改动文件/模块、复用现有模式的搜索路径、验证命令或手工路径、禁止事项。

### `feature.standard.design`

写 `.codestable/features/{YYYY-MM-DD}-{slug}/{slug}-design.md`，至少包含用户问题、成功标准、非目标、现有证据、方案、影响面、风险、验证策略、open questions。用户确认后再抽 `{slug}-checklist.yaml`。

### `roadmap.plan`

写 `.codestable/roadmap/{slug}/`：主 roadmap + `{slug}-items.yaml`。每个子 feature 必须有边界、依赖、验收信号；不要把大需求塞成一个巨型 design。

### `issue.quickfix.plan`

不必补完整 report/analysis。保留最小事实：现象、根因假设/已知根因、修复范围、验证方式。下一步 `cs-do` 修复后写 fix-note。

### `issue.standard.report-analysis`

先写 report，再 analysis。analysis 阶段只定位和给方案，不改代码；根因确认后 `Next: do`。

### `refactor.fastforward.plan`

只列局部改动和行为等价验证。默认不建 `.codestable/refactors/`，除非用户明确要记录。

### `refactor.standard.scan-design`

先 scan，再 design/checklist。每一步都必须能证明行为不变或明确风险。

### `explore.plan`

按 `../codestable-core/references/executors/explore.md` 执行定向探索：明确问题、读取有限证据、列路径和结论、不改代码、不写 `.codestable/compound/`。只有结论未来会复用时，输出“长期记录候选”，并建议用户用 `cs-review：记录 explore 结论：...` 完成沉淀。

## 不做的事

- 不在 `cs-plan` 阶段直接写业务代码，除非用户明确把 plan/do 合并且任务是低风险快路径。
- 不把小任务升级成大型文档流程。
- 不静默修改历史 approved design / analysis；需要变更时写 addendum 或新版本。
- 不把内部 reference 名称当成用户待办。用户只需要看到三入口和下一步动作。
