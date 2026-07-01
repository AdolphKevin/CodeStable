# CodeStable 共享口径
## Document map

Use this map first, then open only the section needed for the current route:

- 0. 目录结构与路径命名
- 1. 共享元数据口径
- 2. {slug}-checklist.yaml 生命周期
- 2.5 roadmap ↔ feature 衔接协议
- 3. 知识沉淀判断
- 4. 继续阅读

## 0. 目录结构与路径命名

onboard 完成后骨架（onboard playbook 负责搭建）：

```
.codestable/
├── INDEX.md               项目知识总索引；三入口启动后先读
├── attention.md           CodeStable 技能启动必读的短硬约束
├── requirements/          能力愿景层（"用户需要什么、系统提供什么能力来满足"，过去/现在/未来）
│   ├── VISION.md           中心索引（按 status 分组，每条带 pitch 一句话）
│   └── {slug}.md           一个能力一份，扁平（project-sync playbook 产出）
├── architecture/          架构中心目录（"用什么结构实现"，只记现状）
│   ├── ARCHITECTURE.md    总入口（索引 + 关键架构决定）
│   └── {type}-{slug}.md   子系统 / 模块 doc（project-sync playbook 产出）
├── roadmap/               规划层（"接下来怎么做这块大需求 + 模块怎么切 + 接口怎么定"）
│   └── {slug}/            一个大需求一个子目录（roadmap playbook 产出）
│       ├── {slug}-roadmap.md   主文档：背景 / 范围 / 模块拆分 / 接口契约 / 子 feature 清单 / 排期
│       ├── {slug}-items.yaml   机器可读子 feature 清单，acceptance 回写状态
│       └── drafts/             可选
├── features/              feature spec 聚合根
│   └── YYYY-MM-DD-{slug}/  每个 feature 一个目录
│       ├── {slug}-brainstorm.md  （可选，case 2 时产出）
│       ├── {slug}-design.md      （标准流程）
│       ├── {slug}-checklist.yaml （标准流程）
│       ├── {slug}-acceptance.md  （标准流程）
│       ├── {slug}-ff-note.md     （fastforward 通道唯一产物，与上面四份互斥）
│       └── {slug}-doc-sweep.md   （可选，手动 anchor sweep 产物）
├── issues/                issue spec 聚合根
│   └── YYYY-MM-DD-{slug}/
│       ├── {slug}-report.md
│       ├── {slug}-analysis.md   （根因不显然才有）
│       ├── {slug}-fix-note.md
│       └── {slug}-doc-sweep.md  （可选，手动 anchor sweep 产物）
├── refactors/             refactor spec 聚合根
│   └── YYYY-MM-DD-{slug}/
│       ├── {slug}-scan.md
│       ├── {slug}-refactor-design.md
│       ├── {slug}-checklist.yaml
│       ├── {slug}-apply-notes.md
│       └── {slug}-doc-sweep.md  （可选，手动 anchor sweep 产物）
├── doc-sweeps/            全项目文档熵维护报告（project-sync playbook 手动 project 模式）
│   └── YYYY-MM-DD-{slug}/
│       └── index.md
├── compound/              沉淀类文档统一目录
│   ├── INDEX.md            长期知识索引
│   └── YYYY-MM-DD-{doc_type}-{slug}.md
│                          doc_type ∈ {learning, trick, decision, explore}
├── brainstorm/            brainstorm 阶段 spike 实验代码区（由 cs-plan 路由、feature playbook 临时产出）
│   └── {slug}/            一次 spike 一个子目录，文件名随意
│                          验完不强制清理，结论回写到对应 brainstorm note
├── tools/                 跨工作流共享脚本（onboard 从技能包释放）
│   ├── scan-project.py     当前代码库存生成工具
│   └── scan-codestable-docs.py 文档熵减库存工具
└── reference/             共享参考文档（onboard 从技能包释放）
    ├── code-inventory.json 当前代码库存（机器可读）
    └── code-inventory.md   当前代码库存（人类可读）
```

### 命名规则

- 需求文档：`requirements/{slug}.md`（能力愿景，不带日期前缀，扁平不分组）；中心索引 `requirements/VISION.md`
- roadmap：`roadmap/{slug}/`（不带日期前缀，平铺不嵌套）
- feature / issue / refactor 目录：带日期前缀 `YYYY-MM-DD-{slug}`
- doc-sweep 项目级报告：`doc-sweeps/YYYY-MM-DD-{slug}/index.md`
- 沉淀类：`compound/YYYY-MM-DD-{doc_type}-{slug}.md`，日期用**归档当天**
- 架构 doc：`architecture/{type}-{slug}.md`（长效，不带日期前缀）；总入口固定 `ARCHITECTURE.md`
- 项目知识总入口固定为 `.codestable/INDEX.md`，项目注意事项入口固定为 `.codestable/attention.md`；所有 CodeStable 入口启动前必须读取这两份文件；不再兼容 `AGENTS.md` / `CLAUDE.md` 等外部入口

### 架构 doc 分组规则（同类聚合）

`architecture/` 下用文件名第一段作 type 标记：`ui-chat.md` 和 `ui-events.md` 同 `ui` 类。**所有架构 doc 必须 `{type}-{slug}.md`**——只有一份的也要带合理 type 段（如 `cli-entry.md`），否则未来同类出现时聚合不了。

**触发**：某 type 在 `architecture/` 根目录达到 ≥6 份时（即新加第 6 份那次），把这一类全部收进同名子目录。

**收入后**：去掉 type 前缀。`ui-chat.md` → `ui/chat.md`。

**只升不降**：删到 ≤5 份也不折回平铺。

**触发时谁负责**：project-sync playbook 的 `backfill` / `update` 模式在 Phase 6 落盘前主动检查并搬迁；命中阈值时这次操作要把"本次新加 / 改的 + 已有同类全部"一起搬，并同步改 `ARCHITECTURE.md` 链接（搬迁本身要在 Phase 5 给用户 review，不偷偷做）。`check` 模式不主动搬迁，但发现 ≥6 仍平铺时在报告末尾列为观察项。

### 改目录结构

改 `codestable-core/onboard/reference/shared-conventions.md` 模板，新项目 onboard 时带上新版本；已有项目通过 `cs-plan：修复/刷新 CodeStable reference` 同步 `.codestable/reference/shared-conventions.md`。

---

## 1. 共享元数据口径

**feature spec**：brainstorm / design / acceptance 共用 `doc_type` / `feature` / `status` / `summary` / `tags`。子技能只补特有字段。`status`：brainstorm = `confirmed`（落盘即确认无 draft）；design = `draft` / `approved`；acceptance 见对应技能。

**issue spec**：report / analysis / fix-note 共用 `doc_type` / `issue` / `status` / `tags`。`severity` / `root_cause_type` / `path` 由对应阶段按需补。

**归档类（compound）**：

- learning / trick / decision / explore 四类**统一写入 `.codestable/compound/`**
- 每个文档 frontmatter 顶部带 `doc_type`（learning / trick / decision / explore）作跨子技能归属判定
- 文件名 `YYYY-MM-DD-{doc_type}-{slug}.md`——日期打头便于 `ls` 排序，type 段在中间便于 grep
- 各子技能在 `doc_type` 之外保留专属 frontmatter（learning 的 `track` / trick 的 `type` / decision 的 `category` / explore 的 `type`）
- 各子技能只认自己的 `doc_type` 不读写别家
- `status` 等通用字段语义和本文件保持一致

**外部读者文档**（guidedoc / libdoc）：frontmatter 由各自子技能定义。无特殊说明：`draft` = 待 review，`current` = 当前有效，`outdated` = 代码已变更待同步。

**写作约束**：子技能提字段时优先写"额外字段"或"阶段状态变化"，不重复展开整套通用字段。

### action spec 生命周期标记

feature / issue / refactor 的 `status` 表示原工作流阶段，**不表示当前设计有效性**。用户手动触发 project-sync playbook 后，旧 spec 被当前有效文档覆盖或推翻时，补生命周期字段：

- `lifecycle: absorbed`：旧文档说的是同一需求 / 问题，已被新锚点完整覆盖
- `lifecycle: superseded`：旧文档的设计 / 修法 / 重构方案已被新锚点推翻
- `absorbed_by` / `superseded_by`：指向新锚点路径
- `lifecycle_note`：一句话说明为什么被吸收或取代
- 新锚点可带 `absorbs` / `supersedes` 列表反向指回旧文档

默认不物理删除旧 spec；删除只处理空目录、未确认草稿、临时 spike 这类用户明确同意丢弃的内容。

---

## 2. {slug}-checklist.yaml 生命周期

- 是 feature 工作流的唯一执行清单
- 由 the feature playbook 在 design 确认通过后一次生成 `steps` + `checks`
- `feature.fastforward` **不生成** checklist（也不写 design / acceptance），是跳过 spec 流程直接写代码的超轻量通道；唯一留下的痕迹是动手后回写的 `{slug}-ff-note.md`（轻量回顾，参与 scoped-commit、可被 project-sync playbook backfill 检索到）
- checklist 是标准 feature 的**默认唯一证据载体**。不要再默认创建 `{slug}-implementation-evidence.md`；只有触发条件复杂、predicate 风险高、或用户明确要求独立证明材料时才建。

`steps` 的粒度是 **编排-计算分离维度的切片策略**——按"先编排骨架、后计算节点、最后持久化与测试"写（最简 Workflow 先行 → 逐个节点填充），**不下沉到 file:line / 函数级**。具体改哪个文件由 implement 阶段决定。

**design 的职责**：

- 提取 `steps`（4-8 步，每步独立可验证退出信号）：后端节奏 = 编排骨架 → 计算节点逐个填 → 接通持久化 → 测试覆盖；前端 = 静态结构 → 交互逻辑 → 状态接入 → 联调收尾
- 提取 `checks`：第 1 节"明确不做"→ 范围守护；第 2.1 接口 → 名词契约；第 2.2 主流程 + 流程级约束 → 编排骨架；第 2.3 挂载点 → 挂载点；第 3 节场景清单 → 验收场景

**implement 的职责**：

- 按 `steps` 顺序执行，每步完成把 status `pending` → `done`
- 每个 `done` / `passed` 的证据优先写进 checklist 对应项的 `evidence`；证据不足就保持 `partial` / `blocked`
- 实现到具体文件级时需要拆分某步、或发现微重构是其前置（参考第 7 节反射检查）→ 跟用户对齐后追加 / 拆分 steps，**不偷偷做**
- 不改写 `checks`

**acceptance 的职责**：只更新 `checks[].status`（`pending` → `passed` / `failed`），不重写 `steps`。

**写作约束**：子技能描述 checklist 时只补本阶段读 / 写哪一部分，不重新定义生命周期。

---

## 2.5 roadmap ↔ feature 衔接协议

`.codestable/roadmap/{slug}/{slug}-items.yaml` 是规划层和 feature 执行层的唯一接口。三个技能共同读写它——是 skill 都读写项目共享产物，不算耦合。

**items.yaml 状态机**：

```
planned  → in-progress  （feature playbook 开始实现时改）
in-progress → done      （cs-review Project Sync 验收通过后改）
planned  → dropped      （roadmap playbook update 模式，用户决定不做时改）
```

`done` / `dropped` 是终态。需要回退重做的新加一条 slug 略改的条目，不改终态。

**roadmap playbook 的职责**：生成和维护 roadmap 主文档 + items.yaml；把 `planned` 改 `dropped`（用户放弃时）；不改 `in-progress` / `done`。

**feature playbook 的职责**（从 roadmap 起头时）：

1. design.md frontmatter 加 `roadmap: {roadmap-slug}` + `roadmap_item: {子 feature slug}`
2. items.yaml 对应条目 `status: in-progress` + `feature: YYYY-MM-DD-{slug}`
3. 校验 yaml

直接起 feature（非 roadmap 来）两字段留空，不触发 roadmap 写。

**cs-review Project Sync 的职责**：

1. 读 design frontmatter `roadmap` / `roadmap_item`
2. 空 → 跳过
3. 有值 → items.yaml 对应条目 `status: done`；同步主文档子 feature 清单显示状态；校验 yaml

回写是**实际写文件的动作**，验收报告要明确记录回写结果。

**最小闭环标记**：items.yaml 每份只有一条 `minimal_loop: true`，标记"做完后系统能端到端跑通最窄路径"。design 启动 `minimal_loop` 条目时优先级最高。

---

## 3. 知识沉淀判断

feature-acceptance / issue-fix / feature-ff 收尾时做一次轻量知识沉淀判断，再进入指南、API 参考、commit 等后续收尾动作。盘点问的是**这条信息以后怎么被用到**，不是让用户选择 `learning` / `decision` / `attention` 这些内部归档类型。

**对用户隐藏内部 reference 名**：knowledge-sync / project-sync 是内部路由，不是用户待办。除非用户主动点名某个 Skill，否则对用户说"已同步项目知识 / 已更新需求 / 已归并架构 / 这条需要你拍板"，不要说"请执行内部同步"。

### 四类候选

| 候选 | 判据 | 内部路由 |
|---|---|---|
| 自动提醒项 | 每次 CodeStable 会话开始都必须知道，且一两句话能讲清 | the knowledge-sync workflow 写入 `.codestable/attention.md` |
| 长期规则项 | 以后做类似工作必须遵守的规约、约束、选型或架构决定 | the knowledge-sync workflow 归档，必要时后续由 project-sync playbook 引用 |
| 可检索经验项 | 一次踩坑、失败尝试、调试路径或经验回顾，未来搜到就够 | the knowledge-sync workflow 归档 |
| 可复用处方项 | "以后做 X 就这样做"的可复用技巧、库用法或技术处方 | the knowledge-sync workflow 归档 |

**用户可见话术**：先列候选内容和建议用途，但用用户能理解的状态词：

- 已自动同步：证据充分、无需用户再判断的事实 / 经验 / 规约
- 需要拍板：是否长期有效、是否已决定、是否每次启动都该提醒还不确定
- 不沉淀：只是一次性实现细节或噪音

feature acceptance 中证据已经充分的候选要继续触发对应归档执行器，不要停在"建议执行某技能"；只有候选是否长期有效、是否已拍板、是否值得每次提醒不确定时，才问用户。不要问"要不要沉淀 learning / 归档 decision / 记到 attention"。

**统一规则**：

- 默认不写沉淀；只有满足下面任一条才归档：下次一定会再踩、每次启动都必须知道、已拍板长期规则、能复用的明确做法。
- 没有候选只写一句"无沉淀项"，避免收尾阶段静默跳过。
- 收尾技能只列候选；实际写文件交给对应归档执行器，避免多处重复落盘逻辑。feature acceptance 识别出已拍板 / 已验证的候选时，收尾技能必须继续路由并执行归档执行器，不能只提示用户另行触发。
- 用户说"不用"立即跳过当前候选，不重复追问。
- 长期规则项必须来自用户已确认的结论、已实现验证结果、或可追溯代码证据，不替用户拍板。
- `attention.md` 只放短、稳、每次启动必须知道的摘要；需要背景、理由、替代方案时写入 compound，必要时让 attention 链接详细归档。
- `.codestable/INDEX.md`、`requirements/VISION.md`、`architecture/ARCHITECTURE.md`、`compound/INDEX.md` 是索引，不是长文档；review 写入具体文档后必须同步相关索引或说明无变化。

### Bug 防复发判断

issue-fix 默认不做长分析。只有命中任一条件才做 5 分钟防复发判断：同类 bug 反复出现、修了两次以上才对、跨层契约不清、测试缺口明显、靠隐含假设才出错。

判断 5 件事，结论只落必要产物：

- 根因类型：缺 spec / 跨层契约 / 变更传播遗漏 / 测试缺口 / 隐含假设
- 之前修法为什么没中：表面修 / 范围不全 / 工具没扫到 / 心智模型错层
- 下次怎么挡住：文档 / 类型 / 运行时校验 / 测试 / review checklist
- 还有哪里可能同类问题：相邻模块 / 同接口调用方 / 同数据流
- 值不值得沉淀：满足本节归档条件才写 learning / decision / trick / attention

### 可执行契约回写

跨层 / infra / API / CLI / DB / 配置格式发生变化时，架构或需求回写不能只写原则。至少补这些能执行和验证的信息：

- 触发范围：什么场景使用这条契约
- 签名：命令 / API / schema / env key / 配置字段
- 契约：输入输出、错误语义、边界行为
- 验证矩阵：good / base / bad cases
- 测试点：断言什么，在哪个测试或手工路径证明
- wrong vs correct：至少一组反例和正确写法

### 各流程收尾顺序

**feature-acceptance**：

1. 轻量知识沉淀判断（只处理满足归档条件的候选）
2. 对已拍板 / 已验证候选直接执行归档：自动提醒项 → the knowledge-sync workflow；长期规则项 → the knowledge-sync workflow；可检索经验项 → the knowledge-sync workflow；可复用处方项 → the knowledge-sync workflow
3. 文档同步盘点：README / docs / guide / libdoc 已存在且被本次能力改到或变得过期 → acceptance 内直接更新
4. `scoped-commit`

对用户汇报时合并成一句："已完成验收，并同步项目知识 / 需求 / 架构 / 现有文档。"只有不确定项单独列出让用户拍板。

需要从零写一份完整外部指南或大批量 API 参考时，才作为独立文档工作处理；不要把本次改动造成的现有文档过期丢成"后续建议"。

**issue-fix**：

1. 轻量知识沉淀判断（只处理满足归档条件的候选）
2. `scoped-commit`

**feature-ff**（比标准 acceptance 短，没有 architecture / req 回写动作）：

1. 轻量知识沉淀判断（可一句话说明）
2. `scoped-commit`

---

## 4. 继续阅读

本文件只保留目录、元数据、checklist、roadmap 衔接和知识沉淀判断。下面这些跨流程规则拆到 `workflow-conventions.md`，避免单个 Markdown 过长：

- 代码质量检查（第 3.5 节）
- 最小实现纪律（第 3 节）
- 收尾提交（第 4 节）
- 动手前上下文读取（第 5 节）
- 归档类子技能共享守护规则（第 6 节）
- 写代码时的反射检查（第 7 节）
