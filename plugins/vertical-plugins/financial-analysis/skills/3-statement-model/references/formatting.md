# 格式标准参考

| 元素 | 格式 |
|------|------|
| 硬编码输入 | 蓝色字体 |
| 公式 | 黑色字体 |
| 其他工作表链接 | 绿色字体 |
| 检查单元格 | 错误时红色，平衡时绿色 |
| 负值 | 使用括号，不使用减号 |
| 货币 | 大额数字不保留小数，每股数据保留 2 位小数 |
| 百分比 | 保留 1 位小数 |
| 标题 | 加粗，底部边框 |
| 单位行 | 在标题下方包含单位行（$ 百万、% 等） |

## 视觉分隔指南

- 历史列与预测列之间使用细垂直边框
- 部分合计（如 Total Assets）之后使用粗底部边框
- 小计行使用单底部边框
- 总计行使用双底部边框

## 合计行与小计行格式

所有合计行和小计行的数值必须使用**加粗字体格式**，以清晰区分汇总数据与个别行项目。

### 利润表（P&L）工作表
| 行项目 | 格式 |
|--------|------|
| Gross Revenue | 加粗 |
| Total Cost of Revenue | 加粗 |
| Gross Profit | 加粗 |
| Total SG&A | 加粗 |
| EBITDA | 加粗 |
| EBIT | 加粗 |
| EBT | 加粗 |
| Net Profit After Tax | 加粗 |

### 资产负债表工作表
| 行项目 | 格式 |
|--------|------|
| Total Current Assets | 加粗 |
| Total Non-Current Assets | 加粗 |
| Total Other Assets | 加粗 |
| Total Assets | 加粗 |
| Total Current Liabilities | 加粗 |
| Total Non-Current Liabilities | 加粗 |
| Total Equity | 加粗 |
| Total Liabilities and Equity | 加粗 |

### 现金流量表工作表
| 行项目 | 格式 |
|--------|------|
| Cash Generated from Operations Before Working Capital Changes | 加粗 |
| Total Working Capital Changes | 加粗 |
| Net Cash Generated from Operations | 加粗 |
| Net Cash Flow from Investing Activities | 加粗 |
| Net Cash Flow from Financing Activities | 加粗 |
| Closing Cash Balance | 加粗 |

**注意：** 此列表并非详尽无遗。对模型中任何表示合计、小计或汇总计算的行，均应使用加粗格式。

## 资产负债表检查行格式

资产负债表检查行（在 Total Liabilities and Equity 之下）使用条件数字格式，非零值显示为红色。当资产负债表正确平衡（检查值 = 0）时，数值显示为黑色或标准格式。

| 检查值 | 字体颜色 |
|--------|---------|
| = 0（平衡） | 黑色（标准） |
| ≠ 0（错误） | 红色 |

**实现方式：** 应用自定义数字格式 `[Red][<>0]0.00;[Red][<>0](0.00);0.00`，或使用 Excel 条件格式，规则为"单元格值 ≠ 0" → 红色字体。

## 利润率行格式

| 元素 | 格式 |
|------|------|
| 利润率 % 行 | 缩进、斜体、保留 1 位小数 |
| 正向趋势 | 无特殊格式（或浅绿色） |
| 负向趋势 | 标记待审查（浅黄色） |
| 低于同行均值 | 考虑高亮以供讨论 |

## 信用指标格式

| 元素 | 格式 |
|------|------|
| 杠杆倍数 | 保留 1 位小数，带 "x" 后缀（如 2.5x） |
| 百分比 | 保留 1 位小数，带 "%" 后缀 |
| Net Debt 为负 | 括号表示，表示净现金头寸 |
| 部分标题 | 加粗，"CREDIT METRICS" |
| 分隔线 | 信用指标部分上方细边框 |

## 信用指标阈值颜色

| 指标 | 绿色 | 黄色 | 红色 |
|------|------|------|------|
| Total Debt / EBITDA | < 2.5x | 2.5x-4.0x | > 4.0x |
| Net Debt / EBITDA | < 2.0x | 2.0x-3.5x | > 3.5x |
| Interest Coverage | > 4.0x | 2.5x-4.0x | < 2.5x |
| Debt / Total Cap | < 40% | 40%-60% | > 60% |
| Current Ratio | > 1.5x | 1.0x-1.5x | < 1.0x |
| Quick Ratio | > 1.0x | 0.75x-1.0x | < 0.75x |

## 检查工作表的条件格式

- 单元格包含通过指示符 → 绿色填充
- 单元格包含失败指示符 → 红色填充
- 单元格包含警告 → 黄色填充
- 差异单元格 = 0 → 浅绿色填充
- 差异单元格 ≠ 0 → 浅红色填充

## 利润率合理性标记

- 毛利率 < 0% → 错误：审查 COGS
- 毛利率 > 80% → 警告：核实收入/COGS
- EBITDA 利润率 < 0% → 标记：经营亏损
- EBITDA 利润率 > 50% → 警告：异常偏高
- 净利润率 < 0% → 标记：净亏损（成长阶段可能可接受）
- 净利润率 > 毛利率 → 错误：公式问题
