---
name: cs-feat-impl
description: feature 流程阶段 2——按 {slug}-checklist.yaml 里 design 切好的 paradigm 维度 steps 推进，每步具体改哪个文件由 implement 自决，写完用统一格式汇报。触发：用户说"方案确认了开始实现"、"按方案写代码"、"开工"。前提是 design 已 approved 且有 checklist。遇到方案外情况要回方案谈不要硬冲。
---

# cs-feat-impl

## 启动必读

开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。

到这一步用户已经在方案上签过字了，你的活是把方案变成代码。容易出问题的不是写代码本身，而是**实现路上发现方案没覆盖到的情况时怎么办**——硬冲下去就把方案当摆设了。下面整套规则就是为了让"停下来"成为默认动作。

> 共享路径与命名约定看 `.codestable/reference/shared-conventions.md` 第 0 节。

---

## 写代码时的三条姿态

具体规则是这三条姿态的落点，理解姿态比记规则重要。

进入具体 step 前先执行 `.codestable/reference/workflow-conventions.md` 第 3 节"最小实现纪律"：先找现有实现，优先标准库 / 平台能力，不写未请求的抽象和预留扩展点。

### 1. 默认写最少的代码

只写当前步骤明确要的东西。不顺手加"以后可能要"的可配置项、抽象层、参数开关、防御性兜底。判据：写完一段觉得"是不是还得加点 X"，先问 X 是不是当前用户能感知到的——不是就别加。整体写完一看 200 行其实 50 行能讲清楚 → 重写。多出来的代码不是中性的，是后人维护的负担。

### 2. 只动该动的，不顺手"改善"邻居

改某个函数时只改那个函数。同文件里别的函数风格丑、命名怪——除非和本次改动直接冲突，否则别碰。新代码风格匹配当前文件已有写法。混进的"顺手改"会把功能 PR 稀释成"一坨综合改动"，review 成本翻几倍。值得改的按下文"顺手发现"格式记成后续 issue。

孤儿处理：你这次改动让某个 import / 函数变成死代码 → 删掉。**不是**你改动造成的死代码 → 留着记成顺手发现。

### 3. design 没说的事别自己拍板

写到一半发现 design 没覆盖的角落（边界条件、错误路径、方案外文件）——默认停下来回 design 谈。下面"补丁分支"和"术语守护"是这条姿态的两个典型落点；**任何"design 没明说我替它选了一个"的瞬间都触发**。

---

## 启动检查

### 1. 方案文件够不够撑实现

frontmatter：`doc_type=feature-design` / `feature` 一致 / `status=approved` / `summary` 非空 / `tags` ≥ 2。

**标准 design**（节 0/1/2/3/4）：
- 第 0 节有内容；第 1 节含"明确不做"和复杂度档位
- 第 2.1 名词层用"现状 → 变化"两段式，每个新增/变更接口至少一个示例 + 来源位置
- 第 2.2 编排层开头有主流程图，"现状 → 变化"齐全，流程级约束已记
- 第 2.3 挂载点按"删了它 feature 是否消失"判据，没把内部代码改动误列进来
- 第 3 节有关键场景清单 + 反向核对项（不含测试代码 / framework 选型）

任一项不达标 → 退回 `cs-feat-design` 补齐。原因：方案漏的项实现时一定要现场补，等于绕过 checkpoint。

**注意**：标准 design 第 3 节"验收契约"只说"做完后什么应该成立"，不说"具体怎么做"。改动文件清单 / 函数级落点 / 测试代码归 implement 自决，不要因为 design 里没写就退回去要求补。

### 2. {slug}-checklist.yaml 在不在

- 文件存在，`feature` 字段一致
- `steps` 非空（design 已产出，paradigm 维度切片，通常 4-8 步；高风险链路因职责拆分可更多）；`checks` 非空
- 不存在 → 退回 `cs-feat-design` 生成
- 新版 checklist 应带证明字段：`steps[].proof_required`、`steps[].evidence`、`steps[].blocker`、`checks[].design_ref`、`checks[].proof_required`、`checks[].positive_case`、`checks[].negative_case`、`checks[].typed_signal`、`checks[].forbidden_basis`、`checks[].evidence`、`checks[].blocker`。
  - 旧 checklist 缺字段时，不要直接实现；先从 design 补齐这些字段并用 `validate-yaml.py --yaml-only` 和本 skill 的 `scripts/validate_checklist_evidence.py {checklist}` 校验。
  - step status 只允许 `pending` / `partial` / `blocked` / `done`；check status 只允许 `pending` / `partial` / `blocked` / `passed`。
  - `done` / `passed` 必须有非空 `evidence`；`partial` / `blocked` 必须有 `blocker`。

### 3. 把上下文读全

- 方案 doc 全文（重点：第 1 节、2.1/2.2/2.3/2.4、3）
- `{slug}-checklist.yaml`、需求来源（用户描述 + brainstorm note）、`.codestable/attention.md`
- 第 2.1 节接口示例的来源位置——读相关函数即可

### 3.5 实现前谓词对照（按需）

只有涉及路由、fallback、recovery、handoff、slot 消费、状态推进、回复组合这类容易漂移的 feature，才做 **design predicate → code predicate** 对照。普通 CRUD、小 UI、小命令改动不建矩阵。

1. 从 design / checklist 里抽出所有"可触发 / 允许 / fallback / recovery / waiting / unsatisfied / read-only"条件词。
2. 写成正反例矩阵：
   - design predicate：设计真正要求什么条件成立
   - code predicate：准备落到代码里的判断条件
   - 正向：什么输入 / typed signal 必须触发
   - 反向：什么相似输入 / typed signal 必须不触发
   - 禁止依据：不能靠哪些关键词、raw text 或未声明猜测
3. 检查 `code predicate` 是否比 `design predicate` 更宽或更窄；更宽 / 更窄都不能直接开写，先回 design 或 checklist 修正。

**测试通过 ≠ predicate 对齐**。如果测试只覆盖正向 happy path，没有覆盖矩阵里的反向行，不能认为实现符合 feature 预期。

把矩阵写进 checklist 对应 check 的 `evidence` / `blocker`。只有矩阵太长、或用户明确要独立证明材料时，才落盘到 `{slug}-implementation-evidence.md`。

```markdown
## Predicate Matrix

| design_ref | design predicate | code predicate | positive proof | negative proof | status |
|---|---|---|---|---|---|
| §3 owner probe | current open-text owner surface + non-owner stateful/response | {函数/条件} | {test/trace} | {test/trace} | pending |
```

没有正反例证据的行，status 保持 `pending` 或 `partial`，对应 checklist check 不能标 `passed`。

### 4. 跟用户确认从哪一步开始

通常第 1 步；接续上次中断时先看 checklist status：从第一个 `pending` / `partial` / `blocked` step 继续。`blocked` 需要先回方案或用户决策，不能跳过。

design 给的 `steps` 是 paradigm 维度切片（编排骨架 → 计算节点 → 持久化 → 测试），**具体每步改哪个文件由你执行时决定**。如果某一步实际是 3 个独立子动作、或发现微重构是它的前置（参考反射检查），跟用户对齐后追加 / 拆分 steps，**不偷偷做**。

**design 第 2.5 节微重构的衔接**：

- 如果 2.5 结论是"做微重构（拆文件）"或"做微重构（重组目录）"，checklist 第 1 步就是它——**独立跑完**，按 2.5 节"行为不变怎么验证"那条核对：
  - 拆文件：编译绿灯 + 现有测试通过 + 对外接口签名零 diff
  - 重组目录：编译绿灯 + 现有测试通过 + diff 仅限文件移动 + import 路径更新（**没有任何函数体改动**）

  **不要合并到下一步**——一旦混在一起，行为变更和结构变更就分不开，出问题回滚不到干净中间态
- 如果 2.5 结论是"不做"但写到中途反射检查触发了拆分信号 → 走下面"反射检查"那条路径（停下来 → 和用户对齐 → 能 provable 解决就追加独立 step），**不要绕过用户确认偷偷追加**
- 如果 2.5 末尾有"建议沉淀的 convention"段：implement 阶段**不主动归档**——只在重组目录跑通且行为零改动确认后，在汇报里带一句"design 2.5 建议沉淀的 convention 已就绪，等 acceptance 阶段作为长期规则项候选盘点"，把决定权交给 acceptance / 用户

---

## 实现期间的几条核心约束

### 严格按 steps 顺序走

按 `steps` 列表顺序执行，不合并、不跳。每推进一步先补 checklist 对应项的 `evidence` / `blocker`，再改 status：证据完整才改为 `done`；证据不足改为 `partial`；无法继续改为 `blocked`。

最常见违规是"顺手把下一步也做了"——每步都对应独立可验证的退出信号，两步合做意味着出问题时不知道是哪一步引入的、回滚也回不到干净中间态。

每个 done 必须绑定证据：改 `status: done` 前，先能指出对应的单测 / 集成测试 / trace / 类型约束 / grep 反向核对。只有"我写了代码"或"测试全绿"不够；证据必须能对应到该 step 的 exit_signal 和 checks 里的正反例矩阵。

状态规则：

- `done`：`proof_required` 全部满足，`evidence` 非空且能定位到 test / trace / grep / schema / file:line。
- `partial`：已有部分实现或部分证据，但还有 design/checklist 要求未满足；必须写 `blocker` 或剩余缺口。
- `blocked`：当前 step 因 design 缺口、依赖缺失或用户决策无法继续；必须写 `blocker`，并停下来回方案谈。
- 禁止批量替换 status；每次改 status 都要伴随同一项的 evidence/blocker 更新。

check 规则同理：没有正反例证据的验收场景不能标 `passed`；只能 `partial` 或 `pending`。

### 不做方案外的改动

发现值得重构的点（参考 `.codestable/reference/workflow-conventions.md` 第 7 节"写代码时的反射检查"），只要**不在本次功能影响面内**就记成后续 issue：

```markdown
> 顺手发现：{文件:行号} {问题简述}。不在本次范围，记录待后续 issue。
```

顺手改的代码不在方案里，验收对不上；后人 git blame 也分不清是为本次功能还是顺手。

### 术语守护

**标准 design**：新写的类型 / 函数 / 变量名都要去方案 doc 第 0 节对照，不允许出现 doc 里没有的新概念。要引入新概念 → 先停下来改第 0 节、grep 防冲突、用户确认。

**Fastforward 通道**：不进入本技能；若在轻量实现里要新起概念名，也要 grep 一下当前代码防冲突。

代价：术语冲突意味着同概念两个名字 / 同名字两个概念——后者会让搜索完全失效。

### 出现"补丁分支"的冲动时停下来

写代码时冒出 `if (特殊情况) { 特殊处理 }` 这种结构，**停**。这种分支基本只有一个原因：方案没覆盖到这种情况。继续写得到的是"为了让代码能跑而加的特殊逻辑"——下次别人改这块时不知道这个分支为什么存在。回方案谈：补进 design / 砍掉 / 明确为遗留问题。

### 代码质量反射检查

除上面流程约束外，还有一组针对代码质量的反射检查——看 `.codestable/reference/workflow-conventions.md` 第 7 节。

核心：**不是"超过 N 行必须拆"，而是"遇到 X 情况就停下来问自己"**。每条对应 AI 默认会走进去的坑（往大文件继续追加、往大类加方法、补丁分支、复制粘贴、第 4+ 个参数、往万能 util 堆东西）。

反射检查结论是"要拆 / 新建文件 / 重命名 / 抽共用层"且超出现有 steps 范围 → 跟用户商量决定，不偷偷拆完继续写。判据按和 design 2.5 一致的边界分两路（避免 impl 自己造一套口径）：

- **能用"只搬不改行为"解决**（拆函数 / 拆文件 / 移动定义，编译器全程绿灯，对外签名零 diff）→ 和用户对齐后**追加为独立 step**插在当前 step 之前，跑完独立验证退出再继续
- **超出"只搬不改行为"边界**（要改函数签名 / 改返回值结构 / 改调用关系语义 / 模块拆合）→ **本 feature 不做**，记成"顺手发现"格式提示用户后续走 `cs-refactor`，当前 step 用最少的改动绕过去；不要因为"反正都看到了"就在 feature 里顺手做掉——这会把功能 PR 稀释成综合改动，也违反 design 2.5 早就划好的边界

### 完成前 red-team 复核

所有 step 自认为可以收尾后，不要马上输出完成汇报。先做一次反向审查：

1. 逐条读 design 第 1 节"明确不做"、第 2.2 流程级约束、第 2.3 挂载点、第 3 验收契约。
2. 对照当前代码和 evidence，尝试证明每个 `passed` / `done` 是错的。
3. 凡是只能用"测试全绿"、"应该可以"、"schema 有字段"解释的项，降级为 `partial` 或 `pending`。
4. 把审查结论写进相关 checklist 项的 `evidence` / `blocker`；只有已有独立 evidence 文件时才同步写入 `Red-Team Review`。

red-team 复核发现 P1/P0 缺口时，停下来报告，不进入 acceptance。

复核后必须运行：

```bash
python /Users/naonao/.agents/skills/cs-feat-impl/scripts/validate_checklist_evidence.py {path/to/{slug}-checklist.yaml}
```

脚本失败时，按报错补 evidence / blocker 或降级 status，不进入完成汇报。

---

## 收尾时输出统一汇报

只有当 checklist evidence 脚本通过，且没有 `partial` / `blocked` 项时，才用下面模板汇报实现完成并**停下来等用户 review**。如果仍有 `partial` / `blocked`，输出"实现阻塞 / 部分完成汇报"，列出 blocker 和需要用户或 design 决策的点，不要说完成。

固定模板的意义：含糊汇报等于把验证责任推回用户。固定模板逼你把改了哪些文件、是否触碰方案外、是否引入新概念一一说清楚。

具体模板看 `reference.md` 的"实现完成汇报模板"。

汇报后停等 review。

---

## 测试用例怎么落

标准 design 第 3 节"关键场景清单"每条 = 一个可验证行为约束。你的活是把每条变成可观察证据：单测 / 集成 / 手工操作 / 类型编译期保证。

具体怎么测、用什么 framework、mock 怎么搭——design 没规定，自决。但你得在 `steps` 里写清楚"哪一步落哪个测试"，汇报里逐项核对每条场景都有证据。

**测试通过 ≠ 验收场景满足**——前者只说明你写的用例过了，不说明每条场景都有用例覆盖。

**测试通过 ≠ predicate 对齐**——涉及触发条件时，至少要覆盖正反例矩阵：一个应该触发的相邻场景、一个看起来相似但不应该触发的场景。没有反向用例时，不要把相关 check 标成 done。

类型系统保证的（如 TypeScript 签名直接排除某种调用），汇报里说"类型签名已落地，编译期保证"。

---

## 退出条件

- [ ] 所有 steps 的 status 都 `done`；所有 checks 的 status 都 `passed`
- [ ] checklist 中每个 `done` / `passed` 都有 evidence；每个 `partial` / `blocked` 都有 blocker；不存在批量标绿
- [ ] predicate-heavy feature 已完成 design predicate / code predicate 对照；普通改动明确跳过
- [ ] `scripts/validate_checklist_evidence.py {slug}-checklist.yaml` 通过
- [ ] 完成汇报已输出，用户 review 通过
- [ ] 没有未处理的"需要叫停"信号
- [ ] 第 3 节关键场景每条都有证据 / 测试覆盖
- [ ] 若创建了 `{slug}-implementation-evidence.md`，内容已和 checklist 证据一致
- [ ] 完成前 red-team 复核没有留下 P1/P0 缺口；若有则已停下来报告
- [ ] 没有"顺手发现"被偷偷修掉（都进 issue 列表）
- [ ] 没有方案外文件改动（或已同步更新方案 doc）

---

## 退出后

只有退出条件全部满足且用户 review 通过后，告诉用户："所有步骤完成，方案 doc 已同步。下一步阶段 3 验收闭环，触发 cs-feat-accept。"

别自己顺手开始写验收报告——验收需要独立的 checklist 节奏，提前进入会让把关失效。

**实现过程中如果踩到了项目通用的硬约束 / 命令陷阱 / 环境设置**（"啊原来这个项目要先 X 才能 Y"，一两行能讲清、下个 feature 的 AI 还会再撞一次）→ 在告诉用户去 accept 前**顺便提一句**："这次发现 {具体那条}，我会在 acceptance 的知识沉淀判断里作为自动提醒项候选列出。"——单条即可，不连写多条；用户说"不用列"就跳过，accept 第 8 节会兜底判断。

---

## 容易踩的坑

详细清单看 `reference.md` 的"容易踩的坑"；执行时发现踩中任一项，先停下来修正 evidence / checklist / design，再继续。
