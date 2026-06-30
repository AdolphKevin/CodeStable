# CodeStable 体系总览

本文档介绍 CodeStable 工作流家族整体——有哪些子技能、各管什么场景、产物怎么组织。无论是 AI 在运行时读到这个文件，还是人打开来看，都能对整个体系有个完整印象。

AI 辅助开发里，有几类场景会反复出现——加新功能、修 bug、遇到值得沉淀的经验、做技术选型、摸新模块的代码、接入新仓库。每种场景如果每次从零处理，都会出各自的典型问题：AI 给功能起的术语跟老代码冲突、bug 改完没人记得当时怎么诊断的、上周刚踩过的坑下周又踩一遍。

CodeStable 把这几类场景各配一套子技能，产物放进统一的目录结构、带统一的 YAML frontmatter,互相之间可以检索引用。


## 技能分成四部分

**根入口**——开放式诉求 / 不知道走哪个时的统一入口:

- `cs` — 介绍体系全貌 + 把诉求路由到正确技能。本技能不做事,只做分诊和提示

**做事**——从一段模糊想法走到上线的功能、或者从一份错误报告走到修好的 bug。默认先走轻量路径，复杂时再升级:

- `cs-feat` — 新功能,默认 fastforward；跨模块 / 新能力边界 / 高风险时升级为 design → implement → acceptance
- `cs-issue` — 修 bug,默认 fix-note 快速通道；根因不明 / 多模块影响时升级为 report → analyze → fix
- `cs-refactor` — 代码优化(行为不变、结构/性能/可读性变),默认小重构；跨模块 / 公开接口 / 无测试时升级为 scan → design → apply

轻量路径直接改代码，但必须读 `attention.md`、跑通用质量检查、留下最小记录并 scoped commit。标准路径才先产出 spec(功能方案 / 问题分析),用户 review 后再动手。针对的是术语冲突、范围失控、改完不留存档这三种 AI 默认会出的问题。

**沉淀**——把做事过程产生的知识存下来,下次遇到同类问题直接复用。普通 feature / issue / fastforward 收尾时只做轻量判断；只有下次一定会再踩、每次启动都必须知道、已拍板长期规则、或明确可复用做法才归档:

- `cs-note` — 自动提醒项：一两行、每次启动 CodeStable 技能都必须知道
- `cs-learn` — 可检索经验项：踩坑、失败尝试、调试路径、经验回顾
- `cs-trick` — 可复用处方项："以后做 X 就这样做"的技巧 / 库用法
- `cs-decide` — 长期规则项：已拍板的技术选型、架构决定、长期约束、编码规约
- `cs-explore` — 存档"调查了 X 问题,看到代码里是这样的"

**讨论层**——想法还模糊时的统一入口,不直接产出设计或代码:

- `cs-brainstorm` — 和用户对话做分诊:case 1(已经够清楚,直接 feature-design)、case 2(小需求,在 feature 里继续讨论并落 `{slug}-brainstorm.md`)、case 3(大需求,移交给 roadmap)

**辅助**——围着前几类转的周边工具:

- `cs-onboard` — 把新仓库接入 CodeStable 目录结构
- `cs-req` — 起草或刷新 `.codestable/requirements/` 下的需求文档——系统的能力愿景层，覆盖过去/现在/未来
- `cs-arch` — 架构相关一站式:起草新架构文档 / 刷新已有文档 / 做架构体检(含 design 自洽 / design↔代码一致 / architecture 目录多份文档间一致)。architecture 只记现状
- `cs-roadmap` — 把一块装不进单个 feature 的大需求拆成带依赖和状态的子 feature 清单,作为后续多次 feature 流程的种子和排期依据;独立于需求 / 架构档案
- `cs-doc-sweep` — 手动文档熵维护：围绕一个完成项清理旧 spec，或全项目分析 spec 有效性
- `cs-guide` — 写给外部读者的开发者指南 / 用户指南
- `cs-libdoc` — 为库的公开 API 逐条目生成参考文档
- `git-commit` — 根据 staged diff 生成规范提交信息并创建提交


## 场景路由

仓库里还没有 `.codestable/` 目录,先用 `cs-onboard` 搭骨架。

| 场景 | 子技能 |
|---|---|
| 想法还模糊 / "有个想法没想清楚" / "先聊聊" | `cs-brainstorm`(分诊后路由到 design / feature-brainstorm 落盘 / roadmap) |
| 新功能 / 新能力 | `cs-feat` |
| BUG / 异常 / 文档错误 | `cs-issue` |
| 代码优化 / 重构 / 重写(行为不变) | `cs-refactor` |
| 摸代码、提问调研 | `cs-explore` |
| 补 / 更新需求文档 | `cs-req` |
| 补 / 更新 / 检查架构文档 | `cs-arch` |
| 大需求拆解 / 排期规划 | `cs-roadmap` |
| 手动清理旧设计文档 / 全项目文档熵检查 / 新方案推翻旧方案 | `cs-doc-sweep` |
| 技术选型 / 约束 / 规约 | `cs-decide` |
| 踩坑回顾、经验总结 | `cs-learn` |
| 可复用的编程模式、库用法 | `cs-trick` |
| 开发者指南 / 用户指南 | `cs-guide` |
| 库 API 参考 | `cs-libdoc` |
| 提交代码 / 生成 commit message | `git-commit` |

完整的操作手册、退出条件、和其他工作流的关系,各子技能里讲。


## 知识沉淀判断

收尾阶段不再让用户先区分 learning / decision / attention。默认不写沉淀；AI 只在满足归档条件时按"未来怎么被用到"列候选:

- **自动提醒项**：每次 CodeStable 会话开始都必须知道,且一两句话能讲清 → `cs-note` 写入 `.codestable/attention.md`
- **长期规则项**：以后做类似工作必须遵守的规约、约束、选型或架构决定 → `cs-decide` 归档
- **可检索经验项**：一次踩坑、失败尝试、调试路径或经验回顾,未来搜到就够 → `cs-learn` 归档
- **可复用处方项**："以后做 X 就这样做"的可复用技巧、库用法或技术处方 → `cs-trick` 归档

没有候选就一句"无沉淀项"结束。用户只确认不确定候选是否保留；`doc_type` 是 AI 内部归档路由。`learning` / `trick` / `decision` / `explore` 仍共用 `.codestable/compound/` 目录,靠 frontmatter 的 `doc_type` 字段和文件名中间的 type 段(`YYYY-MM-DD-{doc_type}-{slug}.md`)区分。`attention.md` 不属于 compound,它是所有 CodeStable 技能启动时强制读取的短摘要入口。


## 愿景档案 vs 结构档案 vs 规划档案 vs 单次动作

四类文档各管一段时间尺度,不要混:

- **愿景档案**(requirements)——描述"用户需要什么、系统提供什么能力来满足"。`status` 区分三个时间深度：`draft`（未来愿景）、`current`（现在的能力）、`outdated`（过去的痕迹）。draft req 可独立于实现存在——先把愿景定下来，后续 roadmap 排期和 design 实现才有稳定对齐基准
- **结构档案**(architecture)——描述"系统现在用什么结构实现"。只记现状,默认在 feature-acceptance 时跟着代码同步;必要时由 cs-arch 主动刷新。**不写"未来会加什么层"**
- **规划档案**(roadmap)——描述"接下来打算怎么分步实现"。独立于愿景和结构档案,改动不牵连 requirements / architecture。所有条目 done / dropped 后 roadmap 进入 `completed` 状态,作为历史档案留存
- **单次动作**(feature / issue / refactor)——本次要做的一件具体事情的 spec。动作走完后,相关沉淀提炼进愿景档案、结构档案和沉淀类文档；用户手动维护文档熵时由 `cs-doc-sweep` 标 `lifecycle`

用户说"我想要一个 X 系统"这种大需求,先走 roadmap 拆成若干子 feature,再一条一条走 feature 流程。直接起 feature 会变成巨型 design 塞不下、拆了又没有追踪抓手。


## 默认快路径，复杂再升级

CodeStable 的默认生命周期是：

```
Orient → Change → Check → Close
```

小 feature 走 `cs-feat-ff`，小 bug 直接 fix-note，小重构走 `cs-refactor-ff`。升级条件：跨模块、新术语或新能力边界、高风险数据路径、根因不明、多候选方案、公开接口变化、无测试却要求行为等价。

升级后才进入分阶段流程：feature 走 brainstorm(可选) → design → implement → acceptance, issue 走 report → analyze → fix。每个阶段有退出条件,上一个没满足,下一个不开始。


## 进一步参考

- `.codestable/reference/shared-conventions.md` — 目录结构、YAML frontmatter 口径、`{slug}-checklist.yaml` 生命周期
- `.codestable/reference/workflow-conventions.md` — 最小实现纪律、质量检查、收尾 commit 约定、归档类共享规则、写代码反射检查
- `.codestable/reference/tools.md` — `search-yaml.py` / `validate-yaml.py` 用法
- `.codestable/reference/maintainer-notes.md` — 断点恢复、新增子工作流的登记

目录结构(requirements/、architecture/、roadmap/、features/、issues/、refactors/、doc-sweeps/、compound/、tools/、reference/)的权威定义在 `shared-conventions.md`。要改目录先改那里——方法是改 `cs-onboard/reference/shared-conventions.md` 这个模板,新项目 onboard 时会带上新版本。


## 相关

- `.codestable/attention.md` — CodeStable 技能启动必读的项目注意事项
- `.codestable/architecture/ARCHITECTURE.md` — 项目架构总入口
