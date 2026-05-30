---
description: 构建含 Comps 终值倍数的 DCF 估值模型
argument-hint: "[公司名称或代码]"
---

# DCF 估值 Command

构建机构级 DCF 模型，使用可比公司分析为估值区间提供参考。

## 开始前必须说明能力来源

执行本命令时，第一段回复必须先向用户说明当前使用的能力来源：

```text
本次使用的是 Claude 金融套件中文版的 `/financial-analysis:dcf` 命令来组织 DCF 估值流程；Wind MCP / Wind MCP Skill 仅作为财务和行情数据源使用，不是使用 Wind 的 DCF Skill。
```

表述规范：

- `/financial-analysis:dcf` 是斜杠命令 / Command，不要称为 `financial-analysis:dcf skill`。
- 本命令内部可以调用本套件的 `dcf-model` Skill 和 `comps-analysis` Skill；对用户说明时应区分“入口命令”和“底层 Skill”。
- 如需区分 Wind，只说明“本次未触发 `/tmp/wind-skills/.../dcf-model/SKILL.md`，Wind MCP / Wind MCP Skill 仅作为数据源”。不要在未读取和核实 Wind 的 `dcf-model` Skill 内容时，评价它“侧重数据接入”或“框架不如本套件完整”。

如果实际触发的是 Wind 的 `dcf-model` Skill，或读取了 `/tmp/wind-skills/.../dcf-model/SKILL.md`，不要继续声称自己在使用 `/financial-analysis:dcf`。应告诉用户当前触发来源不一致，并建议重新打开 Claude Code 后使用 `/financial-analysis:dcf 公司名`。

## 数据源强制规则（中国公司 / A 股）

如果公司是中国上市公司或 A 股标的，**必须优先使用 Wind MCP 或 Wind MCP Skill 获取财务和市场数据**，不要先使用 Web Search。

执行顺序：

1. 先检查当前 Claude Code 会话是否暴露了 Wind MCP 工具；如果有，直接通过 Wind MCP 获取历史财务、行情、估值倍数、Beta、可比公司数据。
2. 如果没有直接暴露 MCP 工具，不要仅因 `~/.claude/settings.json` 里 `mcpServers` 为空就判断 Wind 不可用；继续检查是否存在 Wind MCP Skill，例如 `~/.agents/skills/wind-mcp-skill`。
3. 如果存在 Wind MCP Skill，优先使用其 CLI，例如在 `~/.agents/skills/wind-mcp-skill` 目录下调用 `node scripts/cli.mjs call ...` 获取：
   - `stock_data get_stock_fundamentals`：营业收入、净利润、EBITDA、毛利率、净利率、ROE、资本支出、折旧摊销等；
   - `stock_data get_stock_price_indicators`：股价、市值、估值倍数等；
   - `stock_data get_risk_metrics`：Beta、波动率等风险指标。
4. 只有在 Wind MCP / Wind MCP Skill 均不可用，或用户明确同意时，才使用 Web Search 或公开网页资料作为后备。

Wind 调用纪律：

- 对 A 股公司，第一批可见的数据动作必须是 Wind MCP / Wind MCP Skill，而不是 Web Search 或公开网页检索。
- 优先使用少量、宽口径的 Wind 请求分批获取数据；不要同时启动大量 Explore agent 或并发 CLI 调用，避免命令串行显示混乱、超时和重复取数。
- 如果 Wind CLI 超时但已经返回 `content`，先解析已返回内容；如果确实没有有效内容，只重试一次更窄的问题，再向用户说明数据缺口。

如果无法调用 Wind MCP，应先向用户说明“当前没有可用 Wind MCP 数据通道”，并询问是否安装/启用 Wind MCP，或是否允许临时使用公开网页数据。不要在没有说明的情况下直接改用网页搜索。

## 工作流

### 第一步：收集公司信息

如果提供了公司名称或代码，直接使用。否则询问：
- "你想估值哪家公司？"

### 第二步：运行可比公司分析

**首先，加载 comps-analysis Skill** 构建交易可比：

使用 `skill: "comps-analysis"`：
1. 确定 4-6 家可比上市公司
2. 拉取运营指标（Revenue、EBITDA、利润率、增长率）
3. 拉取估值倍数（EV/Revenue、EV/EBITDA、P/E）
4. 计算统计摘要（中位数、25th/75th 百分位）

**Comps 关键输出：**
- 中位数 EV/EBITDA 倍数 → 用于终值退出倍数
- 中位数 EV/Revenue 倍数 → DCF 输出合理性检验
- 同行增长率 → 收入预测基准
- 同行利润率 → 利润率假设基准

### 第三步：构建 DCF 模型

**加载 dcf-model Skill** 构建估值：

使用 `skill: "dcf-model"`：
1. 收集历史财务数据和市场数据
2. 构建收入预测（Bear/Base/Bull 情景）
3. 建模运营费用和 FCF
4. 使用 CAPM 计算 WACC
5. 折现现金流并计算终值
6. 桥接至股权价值和隐含股价

**Excel 模型交付硬性要求：**

- 生成独立 `.xlsx` 时，Python/openpyxl 只能作为写入 Excel 的工具；DCF 估值、折现、终值、权益桥、每股价值和敏感性表必须写成 Excel 单元格公式，不能在 Python 中算好后作为静态数值写入。
- Wind 取得的历史财务、行情、Beta、市值、债务、股份数等硬编码输入，必须在 Excel 单元格中写明来源注释。
- 生成脚本和 Excel 文件时使用绝对路径，避免因为前面 `cd ~/.agents/skills/wind-mcp-skill` 后当前目录变化，导致脚本运行路径错误。
- 不要无说明地安装依赖；如果缺少 openpyxl、LibreOffice 或重算脚本，应先说明缺口和替代方案。
- 最终交付时必须说明：数据来源、Excel 文件路径、是否完成公式重算/错误检查；如果未能重算，也要明确写出“尚未完成公式重算验证”。
- 如果对用户说“用 Python + openpyxl 生成 Excel”，必须同时说明“Python/openpyxl 只负责写入工作簿，DCF 计算在 Excel 公式中完成”。不能让用户误以为估值结果是 Python 算好后写入的静态表。

**使用 Comps 为 DCF 假设提供参考：**

| Comps 输出 | DCF 输入 |
|------------|----------|
| 同行中位数 EV/EBITDA | 终值退出倍数区间 |
| 同行 25th-75th EV/EBITDA | 敏感性分析区间 |
| 同行中位数增长率 | 收入假设基准 |
| 同行中位数 EBITDA Margin | 终年目标利润率 |
| 同行中位数 P/E | 交叉验证 DCF 隐含 P/E |

### 第四步：交叉验证估值

DCF 完成后，验证：
1. **DCF 隐含 EV/EBITDA** vs 同行中位数
   - 如果 DCF 隐含 25x 但同行在 12x 交易，调查原因
2. **DCF 隐含 P/E** vs 同行中位数
3. **终值占 EV 比例**（应在 50-70%）
4. **估值隐含增长率** vs 同行增长率

### 第五步：交付输出

提供：
1. **Comps 分析表**（.xlsx）含同行交易倍数
2. **DCF 模型**（.xlsx）含：
   - Bear/Base/Bull 情景
   - 敏感性表格（WACC vs 终值增长率等）
   - 估值摘要，含隐含上行/下行空间
3. **摘要**，说明：
   - 关键估值驱动因素
   - Comps 如何为分析提供参考
   - 需关注的风险和敏感性

## 输出摘要示例

```
估值摘要：[公司]（[代码]）

可比公司分析：
- 可比组：[4-6 家可比公司列表]
- 中位数 EV/EBITDA：12.5x（区间：10.2x - 15.8x）
- 中位数 EV/Revenue：3.2x（区间：2.1x - 4.5x）

DCF 估值（Base Case）：
- 隐含股价：$XX.XX
- 当前价格：$YY.YY
- 隐含上行空间：+XX%

估值交叉验证：
- DCF 隐含 EV/EBITDA：13.2x（vs 同行中位数 12.5x）
- DCF 隐含 P/E：22.4x（vs 同行中位数 20.1x）
- 终值：占 EV 的 62%（在正常范围内）

关键假设：
- 收入 CAGR：X%（vs 同行中位数 X%）
- 终年 EBITDA Margin：X%（vs 同行中位数 X%）
- WACC：X.X%
- 终值增长率：X.X%
```
