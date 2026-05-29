# 上市公司财务数据提取参考

**何时使用：** 当模型模板要求从上市公司公告中提取财务数据时参考此文件。对于直接提供数据或使用其他数据源（如 Wind/iFinD）的模板，无需此参考。

---

## 从中国上市公司公告中提取数据

使用上市公司数据填充模型模板时，直接从公告文件中提取财务数据。

### 第一步：定位公告

1. 使用巨潮资讯网：`http://www.cninfo.com.cn/new/disclosure`
2. 或使用交易所网站：
   - 上交所：`http://www.sse.com.cn`
   - 深交所：`http://www.szse.com.cn`
3. 搜索公司名称或股票代码，筛选公告类型（年报/季报/临时公告）

### 第二步：识别报告货币

在提取数据之前，识别报告货币：
- 检查封面或标题中的报告货币
- 查看报表标题（如"人民币千元"或"人民币百万元"）
- 审阅附注一（公司基本情况和主要财务指标）

**常见货币标识**

| 标识 | 货币 |
|------|------|
| ¥, CNY, RMB | 人民币 |
| $, USD | 美元 |
| €, EUR | 欧元 |
| £, GBP | 英镑 |
| ¥, JPY | 日元 |
| CHF | 瑞士法郎 |
| CAD, C$ | 加拿大元 |

将模型货币设置为与文件一致；在假设工作表中记录。

### 第三步：导航至财务报表

在年报或季报中，定位：
- **年报**：第十一节 财务报告
- **季报**：第一节 主要财务数据
- 需提取的关键部分：
  - 合并利润表
  - 合并资产负债表
  - 合并现金流量表
  - 财务报表附注（获取明细数据）

### 第四步：数据提取映射

**利润表（来自合并利润表）**

| 文件行项目 | 模型行项目 |
|-----------|-----------|
| 营业收入 | Revenue |
| 营业成本 | COGS |
| 销售费用 / 管理费用 / 研发费用 | SG&A |
| 折旧和摊销 | D&A |
| 财务费用—利息支出 | Interest Expense |
| 所得税费用 | Taxes |
| 净利润 | Net Income |

**资产负债表（来自合并资产负债表）**

| 文件行项目 | 模型行项目 |
|-----------|-----------|
| 货币资金 | Cash |
| 应收账款 | AR |
| 存货 | Inventory |
| 固定资产 | PP&E (Net) |
| 总资产 | Total Assets |
| 应付账款 | AP |
| 短期借款 / 一年内到期的非流动负债 | Current Debt |
| 长期借款 | LT Debt |
| 未分配利润 | Retained Earnings |
| 所有者权益合计 | Total Equity |

**现金流量表（来自合并现金流量表）**

| 文件行项目 | 模型行项目 |
|-----------|-----------|
| 净利润 | Net Income |
| 固定资产折旧、油气资产折耗、生产性生物资产折旧 | D&A |
| 应收款项的减少（或增加） | ΔAR |
| 存货的减少（或增加） | ΔInventory |
| 应付账款的增加（或减少） | ΔAP |
| 购建固定资产、无形资产和其他长期资产支付的现金 | CapEx |
| 吸收投资收到的现金 | Equity Issuance |
| 取得借款收到的现金 / 偿还债务支付的现金 | Debt activity |
| 分配股利、利润或偿付利息支付的现金 | Dividends |

### 第五步：从附注中提取辅助明细

对于明细表，从财务报表附注中提取：
- **附注：借款** → 到期时间表、利率、契约条款
- **附注：固定资产** → 固定资产原值、累计折旧、使用年限
- **附注：营业收入** → 分部拆分、地区拆分
- **附注：租赁** → 经营租赁 vs 融资租赁义务

### 第六步：历史数据要求

- 年报提供 2 年对比期（本期和上期）
- 季报提供 1 年对比期
- 如需 3 年以上历史数据，需逐年查找历史年报
- 使用季报补充季度颗粒度数据

### 数据提取清单

- 识别报告货币和单位（千元、百万元、元）
- 2 年历史利润表
- 2 年历史现金流量表
- 2 年历史资产负债表
- 验证 IS 净利润 = CF 起始净利润（每年）
- 验证 BS 货币资金 = CF 期末现金（每年）
- 从附注中提取借款到期时间表
- 提取 D&A 明细或使用年限假设
- 记录任何需要标准化的非经常性/一次性项目

### 处理常见文件差异

| 差异 | 处理方式 |
|------|---------|
| D&A 嵌入在营业成本/管理费用中 | 从现金流量表中提取 D&A |
| "其他" 行项目金额重大 | 查看附注获取明细 |
| 追溯调整 | 使用调整后的数据，在假设中注明 |
| 财年 ≠ 日历年 | 使用财年末标注（如 FYE 2025-03） |
| 非人民币报告货币 | 调整模型货币以匹配文件 |

---

## 附录：跨境场景——从 SEC 文件中提取数据

> 当分析在美国上市的公司（如中概股）或需使用 SEC 文件时，参考以下流程。

### 定位 SEC 文件

1. 使用 SEC EDGAR：`https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=[TICKER]&type=10-K`
2. 季度数据使用 `type=10-Q`

### 导航至财务报表

在 10-K 或 10-Q 中，定位：
- **Item 8**（10-K）或 **Item 1**（10-Q）：财务报表
- 需提取的关键部分：
  - Consolidated Income Statement
  - Consolidated Balance Sheet
  - Consolidated Cash Flow Statement
  - Notes to Financial Statements

### 数据提取映射（SEC 格式）

**利润表**

| 文件行项目 | 模型行项目 |
|-----------|-----------|
| Net revenues / Net sales | Revenue |
| Cost of goods sold | COGS |
| Selling, general and administrative | SG&A |
| Depreciation and amortization | D&A |
| Interest expense, net | Interest Expense |
| Income tax expense | Taxes |
| Net income | Net Income |

**资产负债表**

| 文件行项目 | 模型行项目 |
|-----------|-----------|
| Cash and cash equivalents | Cash |
| Accounts receivable, net | AR |
| Inventories | Inventory |
| Property, plant and equipment, net | PP&E (Net) |
| Total assets | Total Assets |
| Accounts payable | AP |
| Short-term debt / Current portion of LT debt | Current Debt |
| Long-term debt | LT Debt |
| Retained earnings | Retained Earnings |
| Total stockholders' equity | Total Equity |

**现金流量表**

| 文件行项目 | 模型行项目 |
|-----------|-----------|
| Net income | Net Income |
| Depreciation and amortization | D&A |
| Changes in accounts receivable | ΔAR |
| Changes in inventories | ΔInventory |
| Changes in accounts payable | ΔAP |
| Capital expenditures | CapEx |
| Proceeds from issuance of common stock | Equity Issuance |
| Proceeds from / Repayments of debt | Debt activity |
| Dividends paid | Dividends |

### 历史数据要求（SEC）

- 10-K 提供 3 年 IS/CF、2 年 BS
- 第 3 年 BS 从前一年的 10-K 中提取
- 使用 10-Q 补充季度颗粒度数据
