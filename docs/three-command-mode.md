# CodeStable 三命令模式

## Document map

- 可发现入口
- 三入口显式 intent
- Playbook 拓扑
- 调试口径
- 项目知识闭环

## 可发现入口

CodeStable 默认只暴露三个生命周期入口：

```text
cs-plan
cs-do
cs-review
```

另外两个独立 utility：

```text
git-commit
business-flow-mapper
```

CodeStable 不依赖 frontmatter 可见性字段隐藏内部能力。共享规则是 `codestable-core/playbooks/` 下的普通 playbook 文件，不是 `SKILL.md`。

## 三入口显式 intent

| 操作 | 用户说法 | Route |
|---|---|---|
| 初始化 `.codestable/` | `cs-plan：初始化 CodeStable` | `onboard.required` |
| 修复骨架 | `cs-plan：检查并修复 .codestable` | `onboard.repair` |
| 根据当前代码刷新项目知识 | `cs-plan：根据当前实现重新整理 .codestable` | `onboard.refresh-knowledge` |
| 检查状态 | `cs-plan：检查 CodeStable 初始化状态` | `onboard.status` |
| 只读代码探索 | `cs-plan：探索 <模块>，不改代码` | `explore.plan` |
| 功能 / bug / 重构 / roadmap 规划 | `cs-plan：<需求>` | `feature.*` / `issue.*` / `refactor.*` / `roadmap.*` |
| 执行 ready 工作 | `cs-do：继续执行` | `*.do` / `*.implement` / `*.fix` / `*.apply` |
| 验收并同步 | `cs-review：验收并做 Project Sync` | `feature.acceptance` / `issue.fix-verify` / `refactor.apply-verify` |
| 手动记录长期事实 | `cs-review：记录 architecture/requirements/decision/...` | `project-sync.manual` / `knowledge-sync.manual` |
| 文档熵减 | `cs-review：做文档熵减，范围是 <scope>` | `project-sync.doc-sweep` |

## Playbook 拓扑

```text
codestable-core/playbooks/
├── onboard.md          # 代码实况初始化、repair、refresh、status
├── explore.md          # 只读代码探索
├── feature.md          # feature fastforward / standard design / implementation / acceptance
├── issue.md            # bug report / analysis / fix / verify
├── refactor.md         # refactor scan / plan / apply / verify
├── roadmap.md          # 大需求拆解和 roadmap 状态
├── project-sync.md     # architecture / requirements / roadmap / doc-sweep / audit
└── knowledge-sync.md   # decision / learning / trick / explore / attention / guide / libdoc
```

这些 playbook 是单一权威源。不要在 `cs-plan` / `cs-do` / `cs-review` 目录里复制同名规则。

## 调试口径

三入口必须输出：

```text
Route: ...
Playbook: codestable-core/playbooks/<name>.md#<section>
Evidence: ...
```

当行为不满意：

1. 先看 `Route` 是否错；错则改入口路由表。
2. Route 对但动作错，改 `Playbook` 指向的小节。
3. Evidence 不足，补对应 playbook 的 evidence/hard-stop。
4. 文档写偏，优先检查 `project-sync.md` 或 `knowledge-sync.md` 的写权限和证据门槛。

## 项目知识闭环

- `cs-plan` 读 `.codestable/INDEX.md`、`attention.md` 和索引，再按需读具体知识；初始化/刷新时生成代码实况索引。
- `cs-do` 按 ready artifact + 项目索引实现，不顺手改长期事实。
- `cs-review` 负责长期事实新鲜度：先验证，再写具体文档，再更新索引。
- 文档熵减走 `project-sync.doc-sweep`：代码证据优先，默认报告和 lifecycle 标记，不默认删除。
