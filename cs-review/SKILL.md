---
name: cs-review
description: CodeStable 用户可见三命令入口之一。用于验收 feature、验证 bug 修复、检查重构等价性、执行 Project Sync、显式记录架构/需求/决策/知识和收口；自包含完成 writeback 判断，不依赖内部 Skill 触发。
---

# cs-review

`cs-review` 是 CodeStable 对用户暴露的 **Review / Sync / Closure 入口**。它负责验证本次变更是否真的完成，以及哪些长期文档应该回写；也承接用户显式要求的架构、需求、决策、踩坑、技巧、注意事项等长期记录。

本 runtime 包只暴露三个 CodeStable Skill：`cs-plan` / `cs-do` / `cs-review`。内部执行器不是 `SKILL.md`，而是包级 `codestable-core/` reference 文件；不要调用、建议或等待任何内部 Skill 名称。

## Runtime reference map

| Route family / Sync target | Runtime authority |
|---|---|
| `feature.acceptance` | `../codestable-core/references/executors/feature.md` |
| `issue.fix-verify` | `../codestable-core/references/executors/issue.md` |
| `refactor.apply-verify` | `../codestable-core/references/executors/refactor.md` |
| roadmap item status / roadmap closure | `../codestable-core/references/executors/roadmap.md` + `../codestable-core/references/executors/project-sync.md` |
| `project-sync.manual` / architecture / requirements / roadmap / audit / doc-sweep | `../codestable-core/references/executors/project-sync.md` |
| `knowledge-sync.manual` / decision / learning / trick / explore / attention / guide / libdoc | `../codestable-core/references/executors/knowledge-sync.md` |

## 启动扫描

1. 检查 `.codestable/` 和 `.codestable/INDEX.md`；不存在则停止，输出 `Next: plan`，提示先用 `cs-plan：初始化 CodeStable` onboard。
2. 读取 `.codestable/INDEX.md`、`.codestable/attention.md` 和 `.codestable/reference/project-knowledge-contract.md`；再根据目标读取 `requirements/VISION.md`、`architecture/ARCHITECTURE.md`、`compound/INDEX.md` 或对应 roadmap index。
3. 先判断用户是否显式要求“记录 / 同步 / 更新 architecture、requirements、roadmap、decision、learning、trick、explore、attention、guide、libdoc”。
   - 是 → 进入 manual sync；不要求存在代码 diff，但必须有用户给出的事实、当前代码锚点、已有文档或本次变更作为证据来源。
   - 否 → 进入普通 review；查看 `git status --short` 与 diff，区分本次范围和旁路脏文件。
4. 查找当前相关 feature / issue / refactor 产物：design、checklist、analysis、fix-note、apply-notes、acceptance、roadmap item。
5. 确认本次是否有足够证据：自动化检查、手工路径、复现路径、行为等价证明，或 manual sync 的明确来源。

## 固定输出协议

每次结束都输出：

```text
Route: <route-id>
Reason: <验收结论和证据摘要；manual sync 要写明来源>
Read: <关键 artifact / diff / check / doc / code anchor 路径>
Write-intent: <实际写回或不写回的文档范围>
Checks: <已跑命令/手工路径；manual sync 可写 not-applicable + 来源>
Writeback Matrix: architecture=<yes/no>, requirements=<yes/no>, roadmap=<yes/no>, compound=<yes/no>, attention=<yes/no>, guides-or-libdoc=<yes/no>
Index Sync: root=<yes/no>, architecture-index=<yes/no>, requirements-index=<yes/no>, compound-index=<yes/no>, roadmap-index=<yes/no>
Next: <commit | do | plan | ask-user | stop>
```

合法 `route-id`：

```text
feature.acceptance
issue.fix-verify
refactor.apply-verify
project-sync.manual
knowledge-sync.manual
review.status-only
review.blocked-unrelated-dirty-files
review.blocked-insufficient-evidence
```

## 常用显式操作

这些操作不再通过单独的内部 Skill 名称调用，而是通过 `cs-review` 的 Project Sync / Knowledge Sync 显式模式执行：

```text
cs-review：记录 architecture：当前订单模块边界是 ...，证据见 src/order/*。
cs-review：记录 requirements：免费用户每天最多导出 3 次报表，超过后提示升级。
cs-review：记录 decision：我们决定先不用 Redis 做任务状态，继续使用 Postgres row lock；原因是 ...。
cs-review：记录 attention：测试必须使用 pnpm test -- --runInBand，因为共享测试数据库有状态。
cs-review：记录 learning/trick/explore：<未来会复用的项目证据和结论>。
```

显式记录时仍必须输出 Writeback Matrix。没有证据来源或复用价值时不要写入长期文档。不要创建 generic note；用户只说“备注 / 项目说明”但未说明类型时，先归类为 attention、learning、trick、decision、explore、guide 或 libdoc；归类不了就 `Next: ask-user`。

## Review 路由表

| 当前状态 | Route | 动作 |
|---|---|---|
| 用户明确要求记录/同步 architecture、requirements、roadmap、audit、doc-sweep | `project-sync.manual` | 读取目标文档和证据，更新当前事实或规划状态；不要求代码 diff，但必须标注来源 |
| 用户明确要求记录 decision、learning、trick、explore、attention、guide、libdoc；或说“备注”但内容可明确归类到这些目标之一 | `knowledge-sync.manual` | 读取现有 compound/attention/guide/libdoc，去重后写可复用知识；没有事实来源或复用价值则跳过/询问 |
| feature 已实现，有 design/checklist 或 fastforward 证据 | `feature.acceptance` | 对照目标/非目标/验收标准检查实现，写 acceptance 或验收摘要 |
| issue 已修复，有 report/analysis/fix-note 或复现路径 | `issue.fix-verify` | 复现旧问题、验证修复、确认无回归，写/补 fix-note |
| refactor 已完成 | `refactor.apply-verify` | 验证行为等价、测试覆盖和 diff 范围，写/补 apply-notes |
| 没有相关代码变更，事项也已关闭 | `review.status-only` | 只做状态确认，不写长期文档 |
| 存在无法归属的大量脏文件 | `review.blocked-unrelated-dirty-files` | 先隔离 scope，不把旁路文件纳入验收 |
| 没有可验证证据，且无法运行检查 | `review.blocked-insufficient-evidence` | 不通过验收，列缺失证据和下一步 |

## Manual sync 语义

`project-sync.manual` 和 `knowledge-sync.manual` 是显式记录模式，不是普通验收的副作用。

| 用户显式说法 | Route | 目标 |
|---|---|---|
| `cs-review：记录架构 ...` / `sync architecture ...` | `project-sync.manual` | `.codestable/architecture/` |
| `cs-review：记录 requirement / 业务规则 ...` | `project-sync.manual` | `.codestable/requirements/` |
| `cs-review：更新 roadmap item ...` | `project-sync.manual` | `.codestable/roadmap/` |
| `cs-review：做 doc-sweep / audit ...` | `project-sync.manual` | 对应 sweep / audit 产物；范围必须明确 |
| `cs-review：record decision ...` / `记录决策 ...` | `knowledge-sync.manual` | `.codestable/compound/*-decision-*.md` |
| `cs-review：记录 learning / 踩坑 ...` | `knowledge-sync.manual` | `.codestable/compound/*-learning-*.md` |
| `cs-review：记录 trick / 项目技巧 ...` | `knowledge-sync.manual` | `.codestable/compound/*-trick-*.md` |
| `cs-review：记录 explore 结论 ...` | `knowledge-sync.manual` | `.codestable/compound/*-explore-*.md` |
| `cs-review：更新 attention ...` | `knowledge-sync.manual` | `.codestable/attention.md`，只写短硬约束 |

显式记录必须满足至少一个事实来源：用户明确拍板、当前代码锚点、已验收 feature/issue/refactor、已有 design/analysis/roadmap、会议/issue 摘要，或可复现的项目经验。缺证据时输出 `Next: ask-user`，不要编造长期事实。

## Project Sync 信号矩阵

普通 review 必须验收通过后才判断是否回写。manual sync 只有在用户显式要求记录/同步，且有明确来源时才可直接写长期文档。不要因为进入 review 就自动改长期文档。

| 同步目标 | 需要回写的信号 | 不应回写的情况 |
|---|---|---|
| `.codestable/architecture/` | 模块边界、公开 API、数据结构、配置格式、主流程、依赖关系发生变化；或用户显式要求记录当前架构事实并给出证据 | 纯 UI 文案、局部 bug、内部变量名、无行为变化的小重构、没有证据的未来设想 |
| `.codestable/requirements/` | 用户可见能力、业务规则、成功标准、能力边界发生变化；或用户显式要求记录业务规则 | 只修实现错误但需求本身没变、实现细节 |
| `.codestable/roadmap/` | roadmap item 完成、范围变更、阻塞解除/新增、子 feature 关系变化；或用户显式要求更新规划状态 | 不属于 roadmap 的独立小任务 |
| `.codestable/compound/` | 出现未来可复用的踩坑、技巧、探索证据、已拍板长期决策 | 一次性实现细节、没有复用价值的调试过程 |
| `.codestable/attention.md` | 每次 CodeStable 启动都必须知道的一两句话硬约束 | 长篇说明、普通经验、低频细节 |
| `docs/` / libdoc | 新增或改变公开组件/API/命令/用户操作路径 | 内部实现改动、无对外阅读价值 |

判定结果必须写进 `Writeback Matrix`。凡是写入 architecture / requirements / roadmap / compound / attention，都必须同时判断并更新对应索引；若索引无需变化，要说明原因。若全部为 no，写：

```text
Project Sync: no-sync — 本次变更没有触发 architecture / requirements / roadmap / compound / attention / guide 更新信号。
Index Sync: no-sync — 索引无需更新。
```

## Roadmap writeback authority

Roadmap completion has a single owner: `cs-review` Project Sync.

- `cs-do` may mark a roadmap item `in-progress` when implementation begins.
- `cs-review` marks roadmap items `done` after acceptance evidence passes, updates main roadmap checkboxes, or records blocked/paused state in roadmap notes/status when closure is not possible. It must not invent item statuses outside the roadmap schema.
- Feature implementation and acceptance summaries must not directly close roadmap status outside review.
- Roadmap status changes do not imply architecture/requirements updates unless current project facts changed.

## 历史完整性规则

- 不静默重写已 approved 的 design、analysis、roadmap，让历史看起来“本来就是这样”。
- 方案执行中有偏差：在 acceptance / fix-note / apply-notes 里记录偏差、原因和最终状态。
- 长期事实变了：更新 architecture / requirements 的当前事实文档，并在 review 产物里引用该更新。
- 旧 spec 被新方案吸收或推翻：只在用户明确要求文档熵清理时进入 doc-sweep；普通 review 不主动大扫除。

## 验证要求

普通 review 至少提供一种硬证据：自动化命令、手工路径、复现路径或行为等价证明。

manual sync 的证据可以不是测试命令，但必须是可追溯来源：用户明确给出的事实/决定、当前代码锚点、已有文档、会议/issue 摘要或本次 diff。来源不足时输出 `review.blocked-insufficient-evidence` 或 `Next: ask-user`，不要编造架构或决策。

## 收口标准

Review 通过或 manual sync 完成后：

- 已写 acceptance / fix-note / apply-notes，或明确本次是 manual sync 无需验收产物。
- Project Sync matrix 已给出 yes/no 和证据。
- 旁路脏文件已排除。
- 输出 `Next: commit` 或 `Next: stop`；若不通过，输出 `Next: do`、`Next: plan` 或 `Next: ask-user`。
