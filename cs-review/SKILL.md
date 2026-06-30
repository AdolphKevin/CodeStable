---
name: cs-review
description: CodeStable 三命令入口之一。触发：用户说 `cs-review`、`cs review`、"review 一下"、"验收一下"、"收口"。本技能是薄入口，只把诉求交给 `cs` 根入口的 review 路由，不另起一套流程。
---

# cs-review

这是 `cs review ...` 的独立技能别名。

不要在这里实现新流程；读取并遵守 `cs/SKILL.md` 的启动扫描和"三命令路由表"，然后按 `cs review` 语义分诊：

- feature 已实现 → feature acceptance
- issue 已修复 → 复现验证 + fix-note
- refactor 已完成 → 行为等价验证 + apply-notes
- 类型内验收通过后 → 执行 `.codestable/reference/workflow-conventions.md` 第 4.5 节 Project Sync
- 没有代码变更或事项已关闭 → 只做状态确认

本技能只解决"用户想用 `cs-review` 触发"的问题。所有路由口径以 `cs/SKILL.md` 为准。
