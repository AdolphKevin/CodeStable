---
name: cs-do
description: CodeStable 用户可见三命令入口之一。用于执行已规划或可明确快路径执行的 feature、bug 修复、重构任务；自包含完成 ready 判断、最小实现纪律和执行证据记录，不依赖内部 Skill 触发。
---

# cs-do

`cs-do` 是 CodeStable 对用户暴露的 **Execution 入口**。它只执行当前 ready 的工作，并把实现限制在已确认范围内；没有 ready 计划时退回 `cs-plan`。

本 runtime 包只暴露三个 CodeStable Skill：`cs-plan` / `cs-do` / `cs-review`。内部执行器不是 `SKILL.md`，而是包级 `codestable-core/` reference 文件；不要调用、建议或等待任何内部 Skill 名称。

## Runtime reference map

| Route family | Runtime authority |
|---|---|
| `feature.*` | `../codestable-core/references/executors/feature.md` |
| `issue.*` | `../codestable-core/references/executors/issue.md` |
| `refactor.*` | `../codestable-core/references/executors/refactor.md` |

`cs-do` 不负责 onboard、roadmap 拆解或 Project Sync。没有 `.codestable/` 或没有 ready plan 时，停止实现并返回 `cs-plan`。

## 启动扫描

1. 检查 `.codestable/` 和 `.codestable/INDEX.md` 是否存在；不存在则 `Route: onboard.required`，不要写代码。
2. 读取 `.codestable/INDEX.md` 与 `.codestable/attention.md`；按需读取 `.codestable/reference/project-knowledge-contract.md` 和 `.codestable/reference/workflow-conventions.md` 的最小实现纪律。
3. 通过索引定位相关 `architecture/`、`requirements/`、`compound/decision|learning|trick|explore`，只打开本次实现会触碰的具体文档。
4. 查看 `git status --short`，区分本次相关脏文件和旁路脏文件。
5. 扫描相关 `.codestable/features/`、`.codestable/issues/`、`.codestable/refactors/`、`.codestable/roadmap/` 产物，判断是否有 ready 项。
6. 读取将要修改的相关代码、测试和现有 helper/type/component/service；先复用，再新增。

## 固定输出协议

每次执行结束都输出：

```text
Route: <route-id>
Reason: <为什么现在可以执行，或为什么必须退回 plan>
Read: <关键 plan/artifact/code/test 路径>
Write-intent: <实际改动范围或准备改动范围>
Checks: <已跑命令/手工路径；没跑说明原因>
Next: <review | plan | ask-user | stop>
```

合法 `route-id`：

```text
onboard.required
feature.fastforward.do
feature.standard.implement
issue.quickfix.do
issue.standard.fix
refactor.fastforward.do
refactor.standard.apply
blocked.need-plan
blocked.need-user-decision
blocked.dirty-worktree
```

## 执行路由表

| 当前状态 / 用户诉求 | Route | 执行动作 |
|---|---|---|
| 没有 `.codestable/` | `onboard.required` | 停止实现，提示先用 `cs-plan` 完成 onboard |
| 用户给的是小功能且边界清楚，或已有 `feature.fastforward.plan` | `feature.fastforward.do` | 最小改动实现，跑验证；可写轻量 note，但不建完整 design/checklist |
| 有 approved feature design + checklist，且 checklist 有未完成项 | `feature.standard.implement` | 按 checklist 当前 step 执行，写 evidence/status |
| bug 根因明确、修复点清楚 | `issue.quickfix.do` | 定点修复、复现验证、写或准备写 fix-note |
| 有 confirmed analysis / 用户已拍板修复方案 | `issue.standard.fix` | 只按确认方案修，不顺手重构 |
| 局部小重构，行为等价可快速自证 | `refactor.fastforward.do` | 原地小改，跑等价测试；默认不留重构目录 |
| 有 approved refactor design + checklist | `refactor.standard.apply` | 逐步 apply，更新 checklist evidence |
| 找不到 approved plan、confirmed analysis 或可证明快路径边界 | `blocked.need-plan` | 退回 `cs-plan` 补计划/根因/方案 |
| 发现方案外风险、需求冲突、公开接口变化超出计划 | `blocked.need-user-decision` | 停止并给用户选择，不硬冲 |
| 工作区有大量无法归属的脏文件，可能污染本次 diff | `blocked.dirty-worktree` | 先说明哪些是旁路脏文件，要求 scoped 处理 |

## 实现纪律

执行前先应用 `.codestable/reference/workflow-conventions.md` 的最小实现纪律：

- 能不做就不做；能删就删；能用现有代码就复用。
- 先搜现有 helper/type/component/service/test，不新建平行体系。
- 不加未请求的抽象、扩展点、配置层、依赖、缓存、队列、插件机制。
- 不把 bug 修复扩大成重构；不把重构夹带行为变化；不把 feature 偷偷改成架构迁移。
- 不使用类型绕过、空 catch、全局 suppression、临时 debug log 作为完成手段。

## 产物更新规则

### feature standard

按 `{slug}-checklist.yaml` 当前 step 执行。每完成一步写 evidence：改了什么、验证了什么、剩余风险。实现阶段不写 acceptance；完成后 `Next: review`。

### feature fastforward

可直接改代码，但必须在输出里写清目标、非目标、验证证据。只有用户要求或有长期知识价值时才写 `.codestable/features/...` 或 `.codestable/compound/...`。

### roadmap-linked feature

当 feature design frontmatter 带 `roadmap` / `roadmap_item` 时，`cs-do` 可以在开始实现时把对应 item 从 `planned` 改为 `in-progress` 并记录 feature 目录；`done`、`blocked`、主文档勾选与关闭只能由 `cs-review` 的 Project Sync 完成。

### issue fix

修复后必须保存复现验证证据。快速通道也要写最小 fix-note 或在输出里明确 `Write-intent: fix-note`。发现根因不成立时停止，`Next: plan`，不要继续猜。

### refactor apply

每一批改动都要证明行为等价：测试、快照、手工路径或明确说明缺口。发现行为需求变化时停止，转回 `cs-plan` 重新分类为 feature/bug。

## 完成标准

本技能结束时必须满足：

- 相关测试/lint/typecheck/手工验证已运行，或明确说明为什么无法运行。
- 本次 diff 范围与 `Route` 匹配。
- checklist evidence / fix-note / apply evidence 已更新或明确留给 `cs-review`。
- 输出 `Next: review` 或清楚说明被 block 的原因。
