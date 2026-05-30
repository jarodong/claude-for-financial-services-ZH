# 金融套件中文本土化风格指南

> 本指南用于约束 README、Agent、Skill、Plugin 文档的中文表达。docs-zh/TERMS.md 解决“术语怎么写”，本文件解决“整段文字怎么写”。

## 一、核心原则

1. 结论前置：先说明功能、用途和边界，再解释细节。
2. 中文读者优先：专业缩写可以保留，但不能让读者猜含义。
3. 术语统一：同一术语在同一文件内不混用不同译法。
4. 不替用户承担责任：涉及投资、交易、合规、会计入账、客户准入时，必须保留人工复核、签批和责任边界。
5. 本土化不是简单替换：SEC、Bloomberg、GAAP 等按语境替换为巨潮资讯网、Wind/iFinD、企业会计准则等；跨境或方法论语境可保留原术语并加说明。

## 二、术语处理规则

### 1. 固定保留英文缩写 + 中文释义

首次出现和表格入口使用“英文（中文释义）”。

| 英文 | 推荐写法 |
|------|----------|
| DCF | DCF（折现现金流估值法） |
| LBO | LBO（杠杆收购模型） |
| Comps | Comps（可比公司分析） |
| Precedents | Precedents（可比交易分析） |
| WACC | WACC（加权平均资本成本） |
| IRR | IRR（内部收益率） |
| MOIC | MOIC（投资倍数） |
| NAV | NAV（净资产值） |
| GL | GL（总分类账） |
| KYC | KYC（客户身份识别/了解你的客户） |
| AML | AML（反洗钱） |
| TLH | TLH（税损收割） |
| CIM | CIM（保密信息备忘录） |
| Teaser | Teaser（匿名推介材料） |
| Pitch Deck | Pitch Deck（推介材料） |

### 2. 中文 + 英文括注

中文金融语境已有稳定表达时，首次出现使用“中文（英文）”，后续直接用中文。

| 中文 | 推荐写法 |
|------|----------|
| 投决会备忘录 | 投决会备忘录（Investment Committee Memo） |
| 管理层演示 | 管理层演示（Management Presentation） |
| 数据室 | 数据室（Data Room） |
| 尽职调查 | 尽职调查（Due Diligence） |
| 三表模型 | 三表模型（3-Statement Model） |

### 3. 直接中文化

财务报表项目和会计科目一般直接用中文，不需要保留英文。

| 英文 | 中文 |
|------|------|
| Income Statement | 利润表 |
| Balance Sheet | 资产负债表 |
| Cash Flow Statement | 现金流量表 |
| Revenue | 营业收入 |
| Net Income | 净利润 |
| Accounts Receivable | 应收账款 |
| Accounts Payable | 应付账款 |

## 三、AI 产品术语

Agent、Skill、Plugin、MCP、Claude Code 等属于产品或技术名，原则上保留英文；首次出现时加中文解释。

| 英文 | 推荐写法 |
|------|----------|
| Agent | Agent（智能体） |
| Skill | Skill（技能） |
| Plugin | Plugin（插件） |
| MCP | MCP（模型上下文协议） |
| Command | Command（命令） |
| Managed Agent | Managed Agent（托管 Agent） |

后续行文中可直接使用 Agent、Skill、Plugin、MCP，不必每次重复括注。

## 四、本土化表达

| 原表达 | 中国语境优先表达 | 说明 |
|--------|------------------|------|
| SEC filing | 上市公司公告 / 巨潮资讯网公告 | 面向 A 股场景 |
| Bloomberg | Wind / iFinD / Choice | 面向国内机构数据源 |
| GAAP | 企业会计准则 | 面向中国会计准则场景 |
| USD / $ | 人民币 / ¥ | 示例默认口径 |
| 10-K / 10-Q | 年报 / 季报 | 面向中国上市公司 |
| Board of Directors | 董事会 | 公司治理语境 |

跨境交易、海外上市公司研究、原仓库说明或工具兼容性说明中，可以保留美国语境，但应明确“美国/海外语境”。

## 五、README 写作规则

1. README 是产品门面，不做大段研究说明。
2. 表格中的 Agent 名可保留英文名，但应补中文功能解释。
3. 功能描述优先使用动词和结果，如“生成简报包”“运行估值模板”“标记缺失”。
4. 不把金融工具写成可自动决策系统，涉及投资建议、交易执行、入账、准入审批时必须保留人工复核边界。
5. 贡献说明、安装步骤、命令和路径保持原技术表达，不为了中文化而破坏可执行性。

## 六、常见混用修正

| 不推荐 | 推荐 |
|--------|------|
| Deck 质检 | Pitch Deck（推介材料）质检 |
| 路演材料 / 推介材料 / Pitch Deck 混用 | 统一为 Pitch Deck（推介材料），后续用“推介材料” |
| DCF 模型 | DCF（折现现金流估值法）模型 |
| GL 对账 | GL（总分类账）对账 |
| KYC 文件 | KYC（客户身份识别/了解你的客户）文件 |
| 投委会 Memo | 投决会备忘录（Investment Committee Memo） |

## 七、质检要求

修改 README 或批量翻译 Markdown 后，至少运行：python3 scripts/check-zh-terms.py README.md

批量检查时可将 Markdown 文件列表传入脚本。脚本只做基础规则检查，不能替代人工专业判断；涉及投资、合规、会计和交易文件时，仍需业务人员复核。
