---
description: 从 PowerPoint 模板文件创建可复用的 PPT 模板 Skill
argument-hint: "[.pptx 或 .potx 文件路径]"
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# PPT 模板创建器 Command

从用户提供的 PowerPoint 模板创建自包含的 PPT 模板 Skill。

## 操作步骤

1. **询问模板文件**（如未提供）：
   - "请提供 PowerPoint 模板文件路径（.pptx 或 .potx）"
   - 模板应包含你想使用的幻灯片布局和品牌元素

2. **加载 ppt-template-creator Skill**：
   - 使用 `skill: "ppt-template-creator"` 工具加载完整 Skill 指令
   - 按照 Skill 中的工作流分析模板并生成新 Skill

3. **收集额外信息**：
   - 公司/模板名称（用于命名 Skill）
   - 主要用途（Pitch Deck、董事会材料、客户演示等）

4. **执行 Skill 工作流**：
   - 分析模板结构（布局、占位符、尺寸）
   - 生成 Skill 目录，含 assets/ 和 SKILL.md
   - 创建示例演示文稿进行验证
   - 打包 Skill

5. **交付打包好的 Skill** 给用户
