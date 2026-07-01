# CodeStable 三命令模式

CodeStable 生命周期入口只有三个：

```text
cs-plan    # 计划 / 初始化 / 刷新 / 探索
cs-do      # 执行 ready 工作
cs-review  # 验收 / 同步 / 收口 / 长期记录
```

## 为什么不是更多 Skill

旧版阶段型能力没有消失，而是收敛为 playbook：

```text
codestable-core/playbooks/
  collaboration.md
  task-memory.md
  minimality.md
  feature.md
  issue.md
  refactor.md
  roadmap.md
  project-sync.md
  knowledge-sync.md
```

宿主只发现三个 CodeStable 入口；工程纪律仍在单一权威 playbook 中，可调试、可修改、不会参与 Skill 触发竞争。

## 三入口职责

| 入口 | 负责 | 不负责 |
|---|---|---|
| `cs-plan` | 初始化、刷新、路由、设计、任务上下文包、只读探索、human gate 判断 | 写业务代码、关闭任务、长期知识沉淀 |
| `cs-do` | 执行 ready 工作、应用 minimality ladder、更新 evidence/journal/proof trace | 猜产品决策、顺手改架构/需求/知识库 |
| `cs-review` | 验收、overbuild 检查、task finish、Project Sync、doc-sweep、手动记录长期事实 | 未验证就同步、无确认删除文档 |

## 固定调试字段

三个入口都会输出可追踪字段：

```text
Route: ...
Playbook: ...
Human Gate: ...
Evidence: ...
Task Memory: ...
Minimality Plan / Minimality / Overbuild Check: ...
Next: ...
```

这让调试从“猜模型为什么这么做”变成检查：路由是否错、human gate 是否漏、context pack 是否不足、minimality rung 是否选错、review 证据是否不足。
