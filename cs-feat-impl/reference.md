# cs-feat-impl reference

## 实现完成汇报模板

```markdown
## 实现完成汇报

### 动了哪些文件
{git status 真实输出}

### 改了哪些函数 / 类型（按步骤分组）
**步骤 N：{步骤名}**
- file:line  函数名  改动类型（新增 / 修改 / 删除）

### 是否触碰到方案外的文件？
{是 / 否。是的话说明原因 + 是否已同步更新方案 doc}

### 是否引入了方案 doc 里没有的新概念 / 抽象？
{是 / 否。是的话说明已回填方案 doc（标准 design 补第 0 节 + 第 2.1 节；fastforward 补第 1 节）并做过 grep 防冲突}

### 代码质量反射检查自检
{对照 shared-conventions 第 7 节，触发哪些信号 + 怎么处理；都没触发写"无触发"}

### 推进顺序退出信号核对
{对照 steps 逐条列 action + exit_signal + proof_required + evidence + status（应全为 done；否则说明 partial/blocked 原因）}

### 设计谓词对照
{引用 `{slug}-implementation-evidence.md` Predicate Matrix；说明是否发现更宽或更窄的实现，以及怎么修正}

### 验收场景自检
**标准 design**：对照第 3 节关键场景清单，每条靠什么证据满足（类型 / 单测 / 集成 / 手工 / assert）+ 反向核对项是否守住
**Fastforward design**：对照第 2 节验收标准逐条核对

### Red-Team 复核
{引用 `{slug}-implementation-evidence.md` Red-Team Review；列出被降级为 partial/blocked 的项；如果无，说明每个 passed 的反证尝试结果}
```

## 容易踩的坑

- 代码只写了一部分就发"完成汇报"。若出现 `partial` / `blocked`，发"实现阻塞 / 部分完成汇报"，不要包装成完成。
- 汇报里写"修改了相关文件"而不列 file:line。
- 看到方案外的代码顺手改了。
- 引入新类型 / 概念但没回去更新方案 doc。
- 加 `if (用户是 X) { 特殊处理 }` 补丁分支而不停下来。
- 用户 review 还没通过就自己进入验收阶段。
- 关键场景清单一条都没落证据。
- 把 paradigm 维度 steps 当 file:line 读。steps 是切片策略不是改动清单；step 内部偷偷拆子步骤而不跟用户对齐等于绕过 review。
