---
name: xlsx-author
description: 在磁盘上生成 .xlsx 文件（无头模式），而非驱动活动 Excel 工作簿——用于没有打开 Office 应用的托管 Agent 会话。
---

# xlsx-author

当运行在**无头模式**（Managed Agent / CMA 模式）且需要将 Excel 工作簿作为**文件制品**交付，而非通过 `mcp__office__excel_*` 编辑活动工作簿时，使用此 Skill。

## 输出约定

- 写入 `./out/<name>.xlsx`。如 `./out/` 不存在则创建。
- 在最终消息中返回相对路径，以便编排层收集。

## 如何构建工作簿

编写简短 Python 脚本并用 Bash 运行。使用 `openpyxl`：

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active; ws.title = "Inputs"
ws["B2"] = "Revenue"; ws["C2"] = 1_250_000_000
ws["C2"].font = Font(color="0000FF")           # 蓝色 = 硬编码输入
calc = wb.create_sheet("DCF")
calc["C5"] = "=Inputs!C2*(1+Inputs!C3)"        # 黑色 = 公式
wb.save("./out/model.xlsx")
```

## 规范（与 audit-xls 一致）

- **蓝/黑/绿。** 蓝色 = 硬编码输入，黑色 = 公式，绿色 = 链接到其他工作表/文件。
- **计算单元格无硬编码。** 每个计算单元格都是公式；每个输入都在 Inputs 工作表上。
- **命名范围** 用于任何从 Deck 或备忘录引用的值。
- **勾稽检查。** 包含一个 Checks 工作表，勾稽（BS 平衡、CF 与现金勾稽等）并显示 TRUE/FALSE。
- **每个文件一个模型。** 除非明确要求，不要追加到现有工作簿。

## 何时不使用

如果 `mcp__office__excel_*` 工具可用（Cowork 插件模式），优先使用它们——它们驱动用户的活动工作簿并提供检查点。此 Skill 是无头运行的文件生成备选方案。
