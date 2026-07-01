# CodeStable 显式操作手册

## Document map

- 入口选择
- Onboard / 初始化与刷新
- Explore / 代码探索
- 手动记录 architecture / requirements / roadmap
- 手动记录 decision / learning / trick / explore / attention
- Doc-sweep / 文档熵减
- Task memory / 上下文包
- Scoped specs / 工程标准
- 项目知识索引维护

## 入口选择

| 操作类型 | 用哪个入口 | 为什么 |
|---|---|---|
| 初始化、修复、刷新 `.codestable/` | `cs-plan` | 进入生命周期前先建立代码实况索引 |
| 代码探索、理解流程、不改代码 | `cs-plan` | explore 是只读探索，不是知识沉淀本身 |
| 新功能 / bug / 重构 / roadmap 规划 | `cs-plan` | 需要路由和边界判断 |
| 执行已 ready 的实现任务 | `cs-do` | 只做明确边界内的工作 |
| 验收、状态收口、文档回写 | `cs-review` | review 拥有长期知识写回权 |
| 文档熵减、找过时文档 | `cs-review` | 需要代码证据优先和删除门槛 |
| 手动记录 architecture / requirements / roadmap 状态 | `cs-review` | Project Sync 显式模式 |
| 手动记录 decision / learning / trick / explore / attention / guide / libdoc | `cs-review` | Knowledge Sync 显式模式；不保留通用 `note` 类型 |
| 记录或更新工程标准 / 测试命令 / API 约定 | `cs-review` | Scoped specs 写回需要来源证据 |

## Onboard / 初始化与刷新

推荐初始化：

```text
cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架。
```

推荐刷新：

```text
cs-plan：根据当前实现重新整理 .codestable。
```

其他说法：

```text
cs-plan：onboard this repo for CodeStable.
cs-plan：检查并修复 .codestable 初始化状态。
cs-plan：刷新 CodeStable 项目知识索引。
```

路由结果：

```text
Route: onboard.required           # 没有 .codestable/，代码实况初始化
Route: onboard.repair             # 有骨架但缺基础件或仍是空模板
Route: onboard.refresh-knowledge  # 按当前实现刷新索引和库存
Route: onboard.status             # 骨架完整，只报告状态
```

初始化不是空目录创建。它应生成：

```text
.codestable/reference/code-inventory.json
.codestable/reference/code-inventory.md
.codestable/INDEX.md
.codestable/architecture/ARCHITECTURE.md
.codestable/requirements/VISION.md
.codestable/specs/INDEX.md
.codestable/tasks/INDEX.md
.codestable/compound/INDEX.md
.codestable/attention.md
```

原则：只根据 README、manifests、入口文件、routes、schemas、tests、config 和代码锚点写 facts；不确定的产品意图标记为 `inferred` 或 `unknown`。

## Explore / 代码探索

```text
cs-plan：探索一下 auth 登录流程，不改代码，列出关键文件、调用链和不确定点。
```

结果：

```text
Route: explore.plan
Write-intent: none
```

explore 默认只读、不落盘。探索结论未来会复用时，再用：

```text
cs-review：记录 explore：billing webhook 幂等逻辑的结论是 ...，证据见 ...
```

## 手动记录架构事实

```text
cs-review：记录 architecture：当前订单模块由 OrderService 负责写模型，OrderQuery 只读投影；证据看 src/order/*。
```

要求：必须有事实来源。计划中的架构不能写成 current architecture；应写 roadmap/design 或标注 proposed。

## 手动记录需求或业务规则

```text
cs-review：记录 requirements：免费用户每天最多导出 3 次报表，超过后提示升级。
```

要求：写用户可见能力、成功标准、边界和失败模式；不要把实现细节写成需求。

## 手动记录技术决策和项目知识

```text
cs-review：记录 decision：我们决定先不用 Redis 做任务状态，继续使用 Postgres row lock；原因是部署复杂度和当前吞吐都可接受。
cs-review：记录 learning：Vitest mock 顺序会影响 authClient 初始化，证据见 src/auth/__tests__/login.test.ts。
cs-review：记录 trick：新增后台列表页时复用 useServerTable，不要重新实现分页状态。
cs-review：记录 attention：测试必须使用 pnpm test -- --runInBand，因为共享测试数据库有状态。
```

如果用户只说“备注 / 项目说明”，先归类为 attention、learning、trick、decision、explore、guide 或 libdoc；无法判断时先问清楚。

## Doc-sweep / 文档熵减

```text
cs-review：做文档熵减，范围是 auth 模块。
cs-review：清理 .codestable 里和当前 billing 实现不一致的旧文档，先出报告不要删除。
```

结果：

```text
Route: project-sync.doc-sweep
```

硬规则：

- 先刷新或读取 `reference/code-inventory.*`。
- 每个旧文档 claim 必须映射到当前代码锚点、当前索引或更新的已验收文档。
- 默认只写 `.codestable/doc-sweeps/YYYY-MM-DD-{slug}/index.md` 和 lifecycle 标记。
- 不默认删除文件；删除需要用户明确确认、逐文件列表和充分证据。

## Task memory / 上下文包

非平凡任务会由 `cs-plan` 创建或更新：

```text
.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md
.codestable/tasks/YYYY-MM-DD-{slug}/journal.md
.codestable/tasks/YYYY-MM-DD-{slug}/proof.md
.codestable/tasks/YYYY-MM-DD-{slug}/status.yaml
```

它用于跨会话恢复，不替代 feature/issue/refactor/roadmap 产物。`cs-do` 追加 journal 和 proof evidence，`cs-review` 收口并只把长期事实提升到 architecture/requirements/compound/attention/specs。

## Scoped specs / 工程标准

记录工程标准时使用：

```text
cs-review：记录 specs：本项目 API handler 必须返回统一 ResultEnvelope，证据见 src/api/* 和 tests/api/*。
```

只记录经代码、测试、CI、README 或 owner 决策确认的规则。不要把单个偶然写法升级成团队规范。

## 项目知识索引维护

- `cs-plan`：先读索引和 attention，再按需打开具体文档；初始化/刷新时按当前代码整理索引。
- `cs-do`：按 ready artifact 和索引读取实现约束，不顺手改长期事实。
- `cs-review`：拥有长期知识新鲜度责任；写具体文档后，同步对应索引，并输出 `Index Sync`。

显式记录架构、需求、决策、探索结论时，请给出事实来源或代码锚点。证据不足时 `cs-review` 会询问，而不是编造项目知识。
