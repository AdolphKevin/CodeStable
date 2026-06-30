---
name: cs-plan
description: CodeStable 三命令入口之一。触发：用户说 `cs-plan`、`cs plan`、"plan 一下"、"先规划"。本技能是薄入口，只把诉求交给 `cs` 根入口的 plan 路由，不另起一套流程。
---

# cs-plan

这是 `cs plan ...` 的独立技能别名。

不要在这里实现新流程；读取并遵守 `cs/SKILL.md` 的启动扫描和"三命令路由表"，然后按 `cs plan` 语义分诊：

- 模糊新能力 → 讨论 / brainstorm
- 清楚 feature → feature design 或 fastforward
- 大需求 → roadmap
- bug → issue report / analysis
- refactor → refactor scan / design

本技能只解决"用户想用 `cs-plan` 触发"的问题。所有路由口径以 `cs/SKILL.md` 为准。
