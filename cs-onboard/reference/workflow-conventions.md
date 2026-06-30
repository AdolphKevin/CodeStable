# CodeStable 流程共享规则

由 `cs-onboard` 复制到项目的 `.codestable/reference/workflow-conventions.md`。本文件存放流程质量、收尾提交、归档守护、写代码反射检查；目录、命名、元数据口径见 `shared-conventions.md`。

---

## 3. 最小实现纪律

feature / issue / refactor 进入写代码阶段前，先按这条顺序压缩实现范围。命中前面的规则就停，不为"以后可能"写代码。

1. **先问是否要做**：推测性需求不做；复杂需求先交付最窄可用闭环。
2. **先找项目现有实现**：已有 helper / 类型 / 模式能覆盖就复用，不重写一份近似逻辑。
3. **优先标准库 / 平台能力**：标准库、HTML / CSS、数据库约束、框架内置能力能解决，就不引入自定义层。
4. **不为小逻辑加依赖**：只有已安装依赖刚好覆盖时才用；新增依赖必须有明确收益。
5. **改共享根因点**：bug fix 先搜调用方，优先在共同入口修根因，不在每个调用方打补丁。
6. **不加未请求抽象**：单实现接口、工厂、配置开关、万能 helper、预留扩展点默认不写。
7. **非平凡逻辑留最小检查**：有分支、循环、解析、钱 / 权限 / 数据安全路径时，留下能失败的最小测试或自检。

可刻意省略的复杂度，用一行 `ponytail:` 注释说明上限和升级条件；没有明确上限的省略不需要解释。

---

## 3.5 代码质量检查

feature-acceptance / issue-fix / refactor-apply / 用户明确说"检查一下"时，先跑这套通用检查，再进入报告收尾。它只覆盖最近改动，不替代系统审计。

### 1. 识别本次改动

```bash
git diff --name-only HEAD
git status --short
```

把改动按来源分三类：

- 本次工作范围内：继续检查
- `.codestable/` 本次产物：随对应流程一起检查
- 无关脏文件：向用户说明并跳过，不纳入本次结论

### 2. 读对应工作产物

- feature：`design.md`、`checklist.yaml`、`implementation-evidence.md`（如果有）、`acceptance.md`（断点续作时）
- issue：`report.md`、`analysis.md`（如果有）、`fix-note.md`（断点续作时）
- refactor：`scan.md`、`refactor-design.md`、`checklist.yaml`、`apply-notes.md`

同时读 `.codestable/attention.md` 和本次改动触碰到的相关 `architecture/`、`requirements/`、`compound/decision` 文档。索引文档只是入口，真正检查要读到被引用的具体文档。

### 3. 跑项目检查

优先使用项目现有命令（README、package scripts、Makefile、CI 配置里已有的 lint / typecheck / test）。没有全量命令时，跑能覆盖本次改动的最小命令，并说明没跑什么。

检查项：

- linter 通过
- typecheck / compile 通过（项目有就跑）
- 相关测试通过；新增函数 / bug fix / 行为变更要有对应测试或可定位证据
- 没有调试日志、临时 print、未解释的 warning suppression、类型安全绕过

### 4. 跨层检查

改动只在单层内可跳过。触碰 2 层以上时逐项看：

- 数据流：读写方向、schema / type 传递、错误传播一致
- 复用：新增常量 / 工具前先搜现有同类；同值 2 处以上才抽共享
- 依赖：新文件 import 路径正确，无循环依赖
- 同层一致性：同概念在相邻模块里的命名和行为一致

发现问题就直接修，修完重跑相关检查。不能修的写成明确 blocker，不要把"应该没事"当通过。

---

## 4. 收尾提交（scoped-commit）

acceptance / issue-fix 走完后把本次产物提交为一个 commit：

- **范围**：本次工作改到的代码 + 相关 spec 文档 + 本次实际更新过的架构 doc + 本次实际更新过的 roadmap items.yaml / 主文档
- **不该进**：和本次工作无关的顺手修改；属于"下次另起 feature / issue"的扩大范围
- **提交前确认**：用户没明确同意不要 `git commit`
- **commit message**：一句话说清"做了什么"，不贴 spec 目录路径

提交前先用 `git status --short` 分类 dirty path：

- 本次工作代码 / 文档仍未提交 → 不允许宣告 finish；回到 scoped-commit
- 只有 `.codestable/` 流程产物未提交 → 纳入本次 scoped-commit
- 明显属于其他窗口 / 其他任务 → 报告一次并排除
- 分不清 → 问用户是纳入提交还是忽略，别猜

子技能只描述本阶段特有提交范围，通用规则看这里。

---

## 5. 动手前上下文读取

写代码前先读和本次改动真正相关的上下文，不搞全库仪式化扫描：

- 当前工作产物：feature 读 design / checklist；issue 读 report / analysis；fastforward 读用户请求和相关代码
- 项目硬约束：总是读 `.codestable/attention.md`
- 结构边界：触碰模块边界 / 跨层时读相关 `architecture/`
- 能力边界：用户可感能力变化时读相关 `requirements/`
- 已拍板知识：到 `compound/` 搜 decision / learning / trick / explore

检索规则：

- 先搜 `architecture/` 和 `compound/`
- 在 `compound/` 用 `doc_type` 过滤（learning / trick / decision / explore）
- 搜到的结果只作参考输入，不盲目套用——可能已 `outdated` 或不适合当前上下文
- 搜到和当前方向冲突的 decision → **必须**正面回应"为什么仍然这么做"或调整方向

子技能只补本阶段查询命令。完整搜索语法看 `.codestable/reference/tools.md`。

---

## 6. 归档类子技能共享守护规则

`cs-learn` / `cs-trick` / `cs-decide` / `cs-explore` 共享下面这组规则。子技能正文只写特有反模式，通用看这里：

1. **只增不删**——已归档除非被明确取代（`status=superseded`）否则不删；理由丢失成本极高
2. **宁缺毋滥**——用户说不出理由的节直接省略，不要 AI 编造
3. **不替用户写实质内容**——AI 负责起草结构和串联语言，实质结论必须来自用户或可追溯的代码证据
4. **attention.md 检查**——写完后若沉淀暴露出"每次启动都该知道"的一两行硬约束，内部路由到自动提醒归档；对用户说"已加入启动必读提醒"或"这条是否每次启动都该提醒需要你确认"。不要提示用户执行 `cs-note`，也不要直接改外部 AI 入口
5. **起草前先查重叠**——动手写前用 `search-yaml.py --query` 查语义相近的旧文档。命中就把候选列给用户在三条路径里选：
   - **更新已有**（默认优先）：沿用原文件名和原创建日期，**不新建**；frontmatter 补 `updated: YYYY-MM-DD`；超出小修在文末加"YYYY-MM-DD 更新"简述
   - **supersede**：旧文档保留原文，`status: superseded` + `superseded-by: {新文件名}`，正文顶部加 `**[已取代]** 见 {新 slug}`；新文档 frontmatter 带 `supersedes: {旧文件名}`
   - **确实是不同主题**：新建，文末"相关文档"列出已有那条说明区别
6. **识别用户意图是"改已有"还是"记新的"**——用户说"改 / 更新 / 修订 / 补充 {某条}"、明确指向某条旧文档、或话题高度重合时默认走"更新已有"，不要闷头新建。分不清就问。

各子技能只认自己的 `doc_type`，不读写别家产物。

---

## 7. 写代码时的反射检查

`cs-feat-impl` 和 `cs-issue-fix` 共用。AI 默认会往"大函数 / 大文件 / god class / 处处特殊分支"漂，这一节把漂移截在发生那一刻。

**不是阈值，是触发器**——硬数字会诱发为拆而拆把自然聚合的代码切碎。每条都是"遇到 X 情况就停下来问自己"。

| 触发场景 | 停下来问自己 |
|---|---|
| 要往一个已经很长的文件追加代码时 | 文件承担几件事？新加的是已有职责延伸还是第 N+1 件事？是第 N+1 就默认新建文件 |
| 要给已经很多方法的类加方法时 | 新方法是核心职责的自然扩展，还是把类推向"什么都能干"？ |
| 写的函数已超过一屏时 | 函数在做几件事？几件事就拆 |
| 要加 `if (特殊情况) { 特殊处理 }` 分支时 | 抽象维度选错了？正确做法可能是把特殊路径和通用路径分成不同函数 / 策略 / 类 |
| 要 copy-paste 一段代码时 | 能抽成共用还是只字面相似？能抽就抽 |
| 要给函数加第 4+ 个参数时 | 函数做的事是不是太多了？参数列表是 API 恶化的早期信号 |
| 要新写"万能工具类 / helper"时 | 真没归属还是只是想不起来放哪儿就先堆 util？ |

**停下来之后**：反射检查只把问题提出来，结论用户定。停下来想清楚的动作（拆 / 新建 / 重命名 / 抽共用）会让改动超出现有 steps 范围 → 跟用户对齐再决定（纳入当前推进 / 记顺手发现留后续）。

不许偷偷拆完继续写，也不许忽略信号硬冲。默认动作是停、问、再继续。
