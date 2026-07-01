# 调试 CodeStable 行为

调试入口是输出协议，而不是隐藏 Skill 名称。

## 先看六个字段

| 字段 | 判断什么 | 常见修复 |
|---|---|---|
| `Route` | 是否走对 feature/issue/refactor/roadmap/onboard/explore | 改 `cs-plan` 路由表或对应 playbook route 条件 |
| `Playbook` | 规则权威文件是否正确 | 改 `codestable-core/playbooks/<name>.md` 对应小节 |
| `Human Gate` | 是否该问用户却直接做了 | 改 `collaboration.md` gate 条件 |
| `Evidence` | 是否有代码/文档/命令锚点 | 加强 startup scan 或 context pack |
| `Task Memory` | 是否创建/读取/更新了 context pack、journal 和 proof trace | 改 `task-memory.md` 或入口扫描规则 |
| `Minimality` / `Overbuild Check` | 是否过度实现或漏安全检查 | 改 `minimality.md` 或 do/review 输出要求 |

## 常见问题

### 小任务被做大

检查 `Minimality Plan` 是否应该是 `reuse` / `one-home-change`，而不是 `new-minimal-code` 或 standard design。修 `minimality.md` 和 `feature.md#Fastforward discipline`。

### 文档熵减偏离当前代码

必须走 `Route: project-sync.doc-sweep`。如果没有 `code-inventory`、claim-to-anchor 表或 `unverified` 分类，修 `project-sync.md#Doc-sweep rules`。

### 新项目初始化太空

检查 `onboard.required` 是否生成了 `code-inventory.*`、`specs/INDEX.md`、`tasks/INDEX.md`、`ARCHITECTURE.md`、`VISION.md`，并且是否使用 `observed/documented/inferred/unknown` 标注置信度。修 `onboard.md` 和 `onboard/reference.md`。

### 跨会话丢上下文

非平凡任务应有 `.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md`、`journal.md` 和 `proof.md`。没有就修 `task-memory.md` 或 `cs-plan` 的 task memory 规则。
