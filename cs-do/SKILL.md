---
name: cs-do
description: CodeStable 三命令入口之一。触发：用户说 `cs-do`、`cs do`、"do 一下"、"继续执行"、"开始做"。本技能是薄入口，只把诉求交给 `cs` 根入口的 do 路由，不另起一套流程。
---

# cs-do

这是 `cs do ...` 的独立技能别名。

不要在这里实现新流程；读取并遵守 `cs/SKILL.md` 的启动扫描和"三命令路由表"，然后按 `cs do` 语义分诊：

- 有 approved feature design / checklist → feature implement
- 有 confirmed issue analysis / 已确认根因 → issue fix
- 有 approved refactor design / checklist → refactor apply
- 没有可执行计划 → 退回 `cs plan`

本技能只解决"用户想用 `cs-do` 触发"的问题。所有路由口径以 `cs/SKILL.md` 为准。
