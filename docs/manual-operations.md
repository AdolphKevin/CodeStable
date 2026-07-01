# CodeStable 显式操作手册

## Document map

- 入口选择
- Onboard / 初始化
- Explore / 代码探索
- 手动记录 architecture / requirements / roadmap
- 手动记录 decision / learning / trick / explore / attention
- Project knowledge freshness

本 runtime 只暴露 `cs-plan` / `cs-do` / `cs-review` 三个 CodeStable 入口。onboard、explore、architecture sync、decision record 等不再是独立 Skill，而是三入口里的显式意图。

## 入口选择

| 操作类型 | 用哪个入口 | 为什么 |
|---|---|---|
| 初始化、修复、检查 `.codestable/` | `cs-plan` | onboard 是进入 CodeStable 生命周期前的规划前置步骤 |
| 代码探索、理解流程、不改代码 | `cs-plan` | explore 是只读探索，不是知识沉淀本身 |
| 新功能 / bug / 重构 / roadmap 规划 | `cs-plan` | 需要路由和边界判断 |
| 执行已 ready 的实现任务 | `cs-do` | 只做已经有明确边界的工作 |
| 验收、状态收口、文档回写 | `cs-review` | review 拥有 Project Sync 的最终写回权 |
| 手动记录 architecture / requirements / roadmap 状态 | `cs-review` | 这是 Project Sync 的显式模式 |
| 手动记录 decision / learning / trick / explore / attention / guide / libdoc | `cs-review` | 这是 Knowledge Sync 的显式模式；不保留通用 `note` 类型，备注必须先归类 |

## Onboard / 初始化

推荐说法：

```text
cs-plan：初始化 CodeStable，给这个仓库建立 .codestable 骨架。
```

可选说法：

```text
cs-plan：onboard this repo for CodeStable.
cs-plan：检查并修复 .codestable 初始化状态。
cs-plan：补齐 CodeStable reference 和 tools，不要覆盖已有项目文档。
```

路由结果：

```text
Route: onboard.required   # 没有 .codestable/
Route: onboard.repair     # 有骨架但缺基础件
Route: onboard.status     # 骨架完整，只报告状态
```

原则：onboard 只创建或修复 CodeStable 运行时骨架，不规划 feature，也不改业务代码。

## Explore / 代码探索

推荐说法：

```text
cs-plan：探索一下 auth 登录流程，不改代码，列出关键文件、调用链和不确定点。
```

路由结果：

```text
Route: explore.plan
```

原则：explore 默认只读、不落盘。只有探索结论未来会复用，且用户要求或后续 review 判定需要沉淀时，才通过 `cs-review` 进入 knowledge-sync。

## 手动记录架构事实

推荐说法：

```text
cs-review：记录 architecture：当前订单模块由 OrderService 负责写模型，OrderQuery 只读投影；证据看 src/order/*。
```

路由结果：

```text
Route: project-sync.manual
Writeback Matrix: architecture=yes, requirements=no, roadmap=no, compound=no, attention=no, guides-or-libdoc=no
```

要求：

- 必须有事实来源：用户明确给出的决定、当前代码锚点、已有文档或本次 diff。
- 如果是“计划中的架构”，不能写成 current architecture；应写成 roadmap/design，或标注 draft/proposed。
- 不要为了记录架构而改 feature / issue / refactor 历史产物。

## 手动记录需求或业务规则

推荐说法：

```text
cs-review：记录 requirements：免费用户每天最多导出 3 次报表，超过后提示升级。
```

路由结果：

```text
Route: project-sync.manual
Writeback Matrix: requirements=yes, architecture=no, roadmap=no, compound=no, attention=no, guides-or-libdoc=no
```

要求：写用户可见能力、成功标准、边界和失败模式；不要把实现细节写成需求。

## 手动记录技术决策

推荐说法：

```text
cs-review：记录 decision：我们决定先不用 Redis 做任务状态，继续使用 Postgres row lock；原因是部署复杂度和当前吞吐都可接受。
```

路由结果：

```text
Route: knowledge-sync.manual
Writeback Matrix: compound=yes, architecture=<yes/no>, requirements=no, roadmap=<yes/no>, attention=no, guides-or-libdoc=no
```

要求：decision 至少包含背景、决定、理由、替代方案、后果。若这个决定改变当前架构事实，再同时更新 architecture；否则只写 compound decision。

## 手动记录注意事项、踩坑、技巧、决策或探索结论

推荐说法：

```text
cs-review：记录 attention：本仓库测试必须使用 pnpm test -- --runInBand，因为共享测试数据库有状态。
cs-review：记录 learning：Vitest mock 顺序会影响 authClient 初始化，见 src/auth/__tests__/login.test.ts。
cs-review：记录 trick：新增后台列表页时复用 useServerTable，不要重新实现分页状态。
cs-review：记录 explore：我刚才确认了 billing webhook 的幂等逻辑，帮我沉淀为可检索说明。
```

如果用户只说“备注 / 项目说明”，先判断它应该是 attention、learning、trick、decision、explore、guide 还是 libdoc；无法判断时不要落盘，先问清楚。

路由结果：

```text
Route: knowledge-sync.manual
```

原则：只记录未来会复用的信息。不要使用泛化 `note` 入口；如果用户说“备注 / 项目说明”，先归类为 attention、learning、trick、decision、explore、guide 或 libdoc。一次性调试噪音、泛泛经验、没有项目证据的建议不要写入 `.codestable/`。

## 不应该这样做

```text
cs-onboard：初始化项目
cs-decide：记录决策
cs-arch：更新架构
```

这些旧阶段型 Skill 在 runtime 包中已经不存在。请通过 `cs-plan` 或 `cs-review` 表达意图。

## 项目知识索引维护

`cs-plan` 初始化后会创建 `.codestable/INDEX.md`、`requirements/VISION.md`、`architecture/ARCHITECTURE.md` 和 `compound/INDEX.md`。日常规则是：

- `cs-plan`：先读索引和 attention，再按需打开具体 architecture / requirements / compound / roadmap 文档。
- `cs-do`：按当前 ready artifact 和索引读取实现约束，不在实现阶段顺手改长期事实。
- `cs-review`：拥有长期知识的新鲜度责任；写具体文档后，同步对应索引，并在输出里给出 `Index Sync`。

显式记录架构、需求、决策、探索结论时，请给出事实来源或代码锚点。证据不足时 `cs-review` 会询问，而不是编造项目知识。
