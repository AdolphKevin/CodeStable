---
name: cs-review
description: CodeStable 用户可见三命令入口之一。用于验收改动、验证修复、Project Sync、代码证据优先的文档熵减、显式记录架构/需求/决策/知识，并输出可调试 route/playbook/evidence。
---

# cs-review

`cs-review` 是 CodeStable 的 **Review / Sync / Closure** 入口。它验证本次变更是否真的完成，并决定哪些长期文档应该回写；也承接用户显式要求的架构、需求、决策、踩坑、技巧、注意事项、文档熵减等长期维护操作。

本 runtime 只暴露三个 CodeStable Skill：`cs-plan` / `cs-do` / `cs-review`。背后规则是 `codestable-core/playbooks/` 里的可审计 playbook。

## Runtime playbook map

| Route family / Sync target | Runtime authority |
|---|---|
| `feature.acceptance` | `../codestable-core/playbooks/feature.md` |
| `issue.fix-verify` | `../codestable-core/playbooks/issue.md` |
| `refactor.apply-verify` | `../codestable-core/playbooks/refactor.md` |
| roadmap item status / roadmap closure | `../codestable-core/playbooks/roadmap.md` + `../codestable-core/playbooks/project-sync.md` |
| `project-sync.manual` / architecture / requirements / roadmap / audit | `../codestable-core/playbooks/project-sync.md` |
| `project-sync.doc-sweep` | `../codestable-core/playbooks/project-sync.md#doc-sweep-rules` |
| `knowledge-sync.manual` / decision / learning / trick / explore / attention / guide / libdoc | `../codestable-core/playbooks/knowledge-sync.md` |

## 启动扫描

1. 检查 `.codestable/` 和 `.codestable/INDEX.md`；不存在则停止，输出 `Next: plan`，提示先用 `cs-plan：初始化 CodeStable`。
2. 读取 `.codestable/INDEX.md`、`.codestable/attention.md`、`.codestable/reference/project-knowledge-contract.md`；再根据目标读取 `requirements/VISION.md`、`architecture/ARCHITECTURE.md`、`compound/INDEX.md` 或对应 roadmap index。
3. 判断用户是否显式要求：
   - 记录 / 同步 architecture、requirements、roadmap、decision、learning、trick、explore、attention、guide、libdoc → manual sync；
   - 文档熵减、清理旧文档、找过时文档、doc-sweep → `project-sync.doc-sweep`；
   - 否则进入普通 review，查看 diff、artifact 和验证证据。
4. manual sync 不要求当前代码 diff，但必须有用户事实、代码锚点、已有文档、reviewed diff 或明确来源。
5. doc-sweep 必须刷新/读取 code inventory，并用当前代码锚点验证文档，不得只凭旧文档互相覆盖。
6. 普通 review 要区分本次范围和旁路脏文件。

## 固定输出协议

每次结束都输出：

```text
Route: <route-id>
Playbook: <codestable-core/playbooks/*.md#section or none>
Reason: <验收结论和证据摘要；manual/doc-sweep 要写明来源>
Read: <关键 artifact / diff / check / doc / code anchor 路径>
Evidence: <测试、diff、代码锚点、用户来源、库存报告或 stale 证据>
Write-intent: <实际写回或不写回的文档范围>
Checks: <已跑命令/手工路径；manual 可写 not-applicable + 来源>
Writeback Matrix: architecture=<yes/no>, requirements=<yes/no>, roadmap=<yes/no>, compound=<yes/no>, attention=<yes/no>, guides-or-libdoc=<yes/no>, doc-sweep=<yes/no>
Index Sync: root=<yes/no>, architecture-index=<yes/no>, requirements-index=<yes/no>, compound-index=<yes/no>, roadmap-index=<yes/no>, doc-sweep-index=<yes/no>
Next: <commit | do | plan | ask-user | stop>
```

合法 `route-id`：

```text
feature.acceptance
issue.fix-verify
refactor.apply-verify
project-sync.manual
project-sync.doc-sweep
knowledge-sync.manual
review.status-only
review.blocked-unrelated-dirty-files
review.blocked-insufficient-evidence
```

## 用户意图表

| 用户说法 | Route | 目标 |
|---|---|---|
| `cs-review：验收这个 feature` | `feature.acceptance` | 对照 design/checklist/diff/checks 验收 |
| `cs-review：验证 bug 修复` | `issue.fix-verify` | 对照 report/analysis/fix-note 和复现路径验证 |
| `cs-review：检查这次重构是否等价` | `refactor.apply-verify` | 对照 refactor plan 和测试证明行为不变 |
| `cs-review：记录 architecture/requirements/roadmap：...` | `project-sync.manual` | 写当前项目事实或规划状态，必须有来源 |
| `cs-review：做文档熵减 / 清理过时文档 / doc-sweep` | `project-sync.doc-sweep` | 先用当前代码和索引核验，再产出 sweep report；默认不删除 |
| `cs-review：记录 decision/learning/trick/explore/attention/guide/libdoc：...` | `knowledge-sync.manual` | 写可复用长期知识，必须有来源或代码锚点 |

不保留通用 `note` 类型。用户说“备注/项目说明”时先归类；归类不了则 `Next: ask-user`。

## Project Sync 判断

写长期文档必须满足“当前事实 + 来源证据 + 索引同步”。没有信号时输出 `no-sync` 是正确行为。

| 信号 | 写哪里 | 不写哪里 |
|---|---|---|
| 公开接口、模块边界、数据/状态归属、配置格式、主流程改变 | architecture | requirements，除非用户可见能力也变了 |
| 用户可见能力、业务规则、成功标准、失败模式改变 | requirements | architecture，除非实现结构也变了 |
| roadmap item 状态、依赖、scope/blocker 改变 | roadmap | architecture/requirements，除非当前事实也变了 |
| 当前变更产生可复用决策/踩坑/技巧/探索结论 | compound 或 attention | requirements，除非它是业务规则 |
| 用户要求文档熵减 | doc-sweep report + index lifecycle | 不直接删除、不凭旧文档覆盖当前代码 |

## Doc-sweep 硬规则

文档熵减必须走 `project-sync.doc-sweep`，不是普通 `project-sync.manual` 的随手改写。

1. 先刷新或读取 `.codestable/reference/code-inventory.json`；缺失时运行 `.codestable/tools/scan-project.py` 或使用包内工具。
2. 读取 `.codestable/INDEX.md`、architecture/requirements/compound/roadmap 索引和目标文档。
3. 对每个候选文档建立 `doc claim -> code anchor / current index / newer doc` 映射。
4. 分类只能是：`current`、`unverified`、`conflicts-with-code`、`superseded-by`、`archive-candidate`。
5. 默认只写 `.codestable/doc-sweeps/YYYY-MM-DD-{slug}/index.md` 报告和索引 lifecycle 标记；**不删除文件**。
6. 只有同时满足“用户明确要求删除 + 当前代码/索引/新文档证据充分 + 删除列表逐项列出”时，才可以删除；否则 `Next: ask-user`。

## Review / Sync 退出条件

- 验收类 review 必须有 checks 或手工路径；没有则 `review.blocked-insufficient-evidence`。
- manual sync 必须有来源；没有则 `ask-user`。
- doc-sweep 必须有代码锚点核验；不能只根据旧文档互相判断新旧。
- 写长期事实时先写具体文档，再更新对应索引，最后必要时更新 `.codestable/INDEX.md`。
- 不静默改 approved design / analysis / roadmap history；需要变更时写 addendum 或新版本。
