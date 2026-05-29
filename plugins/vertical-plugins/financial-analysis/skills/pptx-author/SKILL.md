---
name: pptx-author
description: 在磁盘上生成 .pptx 文件（无头模式），而非驱动活动 PowerPoint 文档——用于没有打开 Office 应用的托管 Agent 会话。
---

# pptx-author

当运行在**无头模式**（Managed Agent / CMA 模式）且需要将 PowerPoint Deck 作为**文件制品**交付，而非通过 `mcp__office__powerpoint_*` 编辑活动文档时，使用此 Skill。

## 输出约定

- 写入 `./out/<name>.pptx`。如 `./out/` 不存在则创建。
- 在最终消息中返回相对路径，以便编排层收集。

## 如何构建 Deck

编写简短 Python 脚本并用 Bash 运行。使用 `python-pptx`：

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation("./templates/firm-template.pptx")  # 如有模板
# 或：prs = Presentation()

slide = prs.slides.add_slide(prs.slide_layouts[5])    # 仅标题
slide.shapes.title.text = "估值摘要"
# ... 添加表格/图表/文本框 ...

prs.save("./out/pitch-<target>.pptx")
```

## 规范（与活动 Office 的 pitch-deck Skill 一致）

- **每页一个观点。** 标题说明结论；正文支撑。
- **每个数字追溯到模型。** 如果数字来自 `./out/model.xlsx`，在脚注标注工作表和单元格。
- **使用公司模板** —— 如果 `./templates/` 有挂载模板，使用它；否则使用默认布局。
- **图表** —— 当保真度重要时，优先嵌入从模型渲染的 PNG 而非原生 pptx 图表。
- **不外发。** 此 Skill 写文件；不发邮件也不上传。

## 何时不使用

如果 `mcp__office__powerpoint_*` 工具可用（Cowork 插件模式），优先使用它们——它们驱动用户的活动文档并提供检查点。此 Skill 是无头运行的文件生成备选方案。
