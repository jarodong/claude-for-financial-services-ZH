# 任务2：财务建模 - 详细工作流程

本文档提供了执行 initiating-coverage 技能中任务2（财务建模）的分步指引。

## 任务概述

**目的**：提取历史财务数据并构建包含预测和情景分析的综合 Excel 财务模型。

**前置条件**：⚠️ 开始前请核实
- **必需**：获取公司财务数据的途径
  - 上市公司：巨潮资讯网上的最新年报和近期季报
  - 非上市公司：可用来源的财务报表或估算数据
  - 或：用户提供的已提取历史财务数据
- **可选**：任务1的公司研究（用于业务背景）

**输出**：Excel 财务模型（.xlsx），包含6个核心工作表：
1. 收入模型
2. 利润表
3. 现金流量表
4. 资产负债表
5. 情景分析
6. DCF 输入

---

## 输入核实

**开始前 - 检查：**

**选项A：直接提取财务数据（最常见）**
- [ ] 能否访问年报文件（上市公司）？
- [ ] 或能否访问财务报表（非上市公司）？
- [ ] 是否准备好创建 Excel 文件进行历史数据提取？

**选项B：用户已预提取财务数据**
- [ ] 是否提供了历史财务数据文件？（.xlsx 或其他格式）
- [ ] 是否包含3-5年的利润表、现金流量表、资产负债表？
- [ ] 数据是否干净可用？

**可选背景：**
- [ ] 任务1的公司研究是否已完成以了解业务？

**如核实未通过**：请停止并获取财务报表（年报或同等文件）的访问权限后再继续。

---

## 模型结构和格式

### 颜色编码（行业标准）
- **蓝色文本**：硬编码输入（用户可修改）
- **黑色文本**：公式和计算
- **绿色文本**：链接到其他工作表
- **红色文本**：错误或标记（应予解决）

### 格式标准
- 专业的边框和底纹
- 清晰的分区标题
- 可折叠的分组行
- 关键输入/输出的命名区域
- 公式中不使用硬编码数字（除12个月等常量外）
- 清晰的单位标注（千元、百万元等）

### 公式最佳实践
- 所有数字应从假设推导
- 修改一个假设 → 整个模型自动更新
- 无循环引用
- 为关键单元格使用命名区域
- 保持公式简洁可审计
- 为复杂计算添加注释

---

## 分步建模工作流程

### 步骤1：提取历史财务数据

**如历史财务数据已提取，跳至步骤2。**

**上市公司：**

1. **下载年报文件**
   - 前往巨潮资讯网 (https://www.cninfo.com.cn)
   - 搜索公司名称或股票代码
   - 下载最新年报
   - 导航至第十一节 财务报告

2. **创建历史财务数据 Excel 文件**
   - 文件名：`[公司]_历史财务数据_[日期].xlsx`
   - 此文件将成为模型的基础

3. **提取利润表（3-5年）**
   - 创建工作表1："历史利润表"
   - 提取3-5年的所有行项目：
     - 收入（总计及按分部披露的）
     - 收入成本 / COGS
     - 毛利润
     - 营业费用（研发、销售及营销、管理费用分项列示）
     - EBITDA（如未披露则计算：EBIT + D&A）
     - EBIT / 营业利润
     - 利息费用/收入
     - 其他收入/费用
     - 税前利润
     - 所得税和税率
     - 净利润
     - 每股收益（基本和稀释）
     - 流通股数（基本和稀释）

4. **提取现金流量表（3-5年）**
   - 创建工作表2："历史现金流量表"
   - 提取所有行项目：
     - 经营活动（从净利润开始）
     - 折旧和摊销
     - 股权激励
     - 营运资金变动（应收账款、存货、应付账款）
     - 经营活动现金流
     - 投资活动（资本支出、收购）
     - 融资活动（债务发行/偿还、股权、股利）
     - 现金净变动
     - 期初和期末现金

5. **提取资产负债表（3-5年）**
   - 创建工作表3："历史资产负债表"
   - 提取所有行项目：
     - 流动资产（现金、应收账款、存货、其他）
     - 非流动资产（固定资产、无形资产、商誉）
     - 总资产
     - 流动负债（应付账款、应计费用、短期债务）
     - 非流动负债（长期债务、递延税项）
     - 总负债
     - 股东权益（普通股、留存收益）
     - 负债及权益合计

6. **计算历史指标**
   - 创建工作表4："历史指标"
   - 从报表计算：
     - 收入增长率%（同比）
     - 毛利率%
     - EBITDA 利润率%
     - 营业利润率%
     - 净利率%
     - 自由现金流（经营现金流 - 资本支出）
     - FCF 利润率%
     - ROIC（近似值：NOPAT / 投入资本）
     - 资产负债率
     - 流动比率（流动资产 / 流动负债）

7. **记录来源和注释**
   - 创建工作表5："注释"
   - 记录：
     - 年报提交日期和财年结束日
     - 任何一次性项目或已注明的调整
     - 扣非前后差异
     - 分部明细（如按产品/地区划分的收入）
     - 数据质量说明和局限性

**非上市公司：**

1. **收集可用数据**
   - 财务报表（如有）
   - 包含收入数据的新闻稿
   - 融资公告
   - 行业估算或可比公司数据

2. **创建简化历史文件**
   - 估算收入（如有）
   - 估算利润率（如需要可参考可比公司）
   - 关键比率和指标
   - 记录所有假设和来源

**核实：**
- [ ] 所有3张财务报表已提取（3-5年）
- [ ] 各报表之间数据勾稽一致（净利润匹配）
- [ ] 关键指标计算正确
- [ ] Excel 文件已保存且可打开
- [ ] 数据来源已记录（年报日期、页码）

**预测模型的基础现已完成。继续步骤2。**
   - 资本支出
   - 营运资金项目
   - 债务和利息费用
   - 股数（基本和稀释）

3. **整理历史数据以备录入**
   - 准备3-5年实际数据
   - 将直接录入利润表、现金流量表和资产负债表工作表
   - 历史年份在列中，预测年份随后

4. **计算历史趋势**
   - 收入 CAGR
   - 利润率变化趋势
   - 费用杠杆
   - 营运资金模式
   - 资本支出占收入比例
   - 这些趋势将为预测假设提供依据

**注**：假设将直接在各工作表中以蓝色文本输入记录，而非单独的工作表。

### 步骤2：收入建模

**关键提示：这是模型中最重要和最详细的部分。**

#### A. 按产品/类别划分的收入（20-30行）

创建详细表格：
```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
产品类别 A
  子产品 A1             XX      XX      XX      XX      XX      XX      XX      XX      XX
  子产品 A2             XX      XX      XX      XX      XX      XX      XX      XX      XX
  子产品 A3             XX      XX      XX      XX      XX      XX      XX      XX      XX
  类别 A 合计           XX      XX      XX      XX      XX      XX      XX      XX      XX
  占总收入比例          X%      X%      X%      X%      X%      X%      X%      X%      X%
  同比增长率            -       X%      X%      X%      X%      X%      X%      X%      X%

产品类别 B
  [类似结构]

[继续所有产品类别]

服务收入                XX      XX      XX      XX      XX      XX      XX      XX      XX
其他收入                XX      XX      XX      XX      XX      XX      XX      XX      XX

总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
总收入增长率            -       X%      X%      X%      X%      X%      X%      X%      X%
```

**关键要求：**
- 显示每个类别的绝对收入（百万元）
- 计算每个类别占总收入的百分比
- 显示每个类别的同比增长率
- 必须有细分子类别（而非仅3-5个顶层类别）
- 显示随时间的结构变化
- 将所有预测链接到假设工作表

#### B. 按地区划分的收入（15-20行）

创建详细表格：
```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
北美
  美国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  加拿大                XX      XX      XX      XX      XX      XX      XX      XX      XX
  墨西哥                XX      XX      XX      XX      XX      XX      XX      XX      XX
  北美合计              XX      XX      XX      XX      XX      XX      XX      XX      XX
  占总收入比例          X%      X%      X%      X%      X%      X%      X%      X%      X%
  同比增长率            -       X%      X%      X%      X%      X%      X%      X%      X%

欧洲
  英国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  德国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  法国                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他欧洲              XX      XX      XX      XX      XX      XX      XX      XX      XX
  欧洲合计              XX      XX      XX      XX      XX      XX      XX      XX      XX
  占总收入比例          X%      X%      X%      X%      X%      X%      X%      X%      X%
  同比增长率            -       X%      X%      X%      X%      X%      X%      X%      X%

亚太地区
  [类似结构]

其他地区
  [类似结构]

总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
```

**核实：**
- 按产品划分的收入合计 = 按地区划分的收入合计 = 总收入
- 所有百分比加总为100%
- 增长率计算正确

#### C. 按渠道划分的收入（如适用）

```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
直销                    XX      XX      XX      XX      XX      XX      XX      XX      XX
电商/线上               XX      XX      XX      XX      XX      XX      XX      XX      XX
批发/合作伙伴           XX      XX      XX      XX      XX      XX      XX      XX      XX
零售门店
  自营门店              XX      XX      XX      XX      XX      XX      XX      XX      XX
  门店数量              XX      XX      XX      XX      XX      XX      XX      XX      XX
  单店销售额            XX      XX      XX      XX      XX      XX      XX      XX      XX
其他渠道                XX      XX      XX      XX      XX      XX      XX      XX      XX

总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
```

### 步骤3：营业费用建模

#### A. 收入成本
1. **拆分 COGS 组成**
   - 产品成本（原材料、制造）
   - 运输和物流
   - 服务交付成本
   - 其他直接成本

2. **链接到收入**
   - 计算 COGS 占收入的百分比
   - 按年建模毛利率
   - 链接到假设工作表

#### B. 研发费用
```
研发费用                2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
研发人员数              XX      XX      XX      XX      XX      XX      XX      XX      XX
人均研发薪酬            XX      XX      XX      XX      XX      XX      XX      XX      XX
研发人员成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
研发其他成本            XX      XX      XX      XX      XX      XX      XX      XX      XX
研发费用合计            XX      XX      XX      XX      XX      XX      XX      XX      XX
占收入比例              X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### C. 销售及营销费用
```
销售及营销              2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
销售及营销人员数        XX      XX      XX      XX      XX      XX      XX      XX      XX
人均薪酬                XX      XX      XX      XX      XX      XX      XX      XX      XX
人员成本                XX      XX      XX      XX      XX      XX      XX      XX      XX
营销支出                XX      XX      XX      XX      XX      XX      XX      XX      XX
其他成本                XX      XX      XX      XX      XX      XX      XX      XX      XX
销售及营销费用合计      XX      XX      XX      XX      XX      XX      XX      XX      XX
占收入比例              X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### D. 管理费用
```
管理费用                2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
管理人员数              XX      XX      XX      XX      XX      XX      XX      XX      XX
人均薪酬                XX      XX      XX      XX      XX      XX      XX      XX      XX
人员成本                XX      XX      XX      XX      XX      XX      XX      XX      XX
其他成本                XX      XX      XX      XX      XX      XX      XX      XX      XX
管理费用合计            XX      XX      XX      XX      XX      XX      XX      XX      XX
占收入比例              X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### E. 折旧和摊销
- 链接到资本支出计划
- 按假设中的折旧率计算
- 计算年度 D&A

### 步骤4：构建利润表

**创建包含40-50个行项目的完整利润表：**

```
利润表                  2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

收入
[链接到收入模型工作表]
总收入                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  同比增长率            -       X%      X%      X%      X%      X%      X%      X%      X%

收入成本
[链接到 COGS 明细]
COGS 合计              XX      XX      XX      XX      XX      XX      XX      XX      XX

毛利润                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  毛利率                X%      X%      X%      X%      X%      X%      X%      X%      X%

营业费用
研发费用合计            XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入比例            X%      X%      X%      X%      X%      X%      X%      X%      X%
销售及营销费用合计      XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入比例            X%      X%      X%      X%      X%      X%      X%      X%      X%
管理费用合计            XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入比例            X%      X%      X%      X%      X%      X%      X%      X%      X%
折旧和摊销              XX      XX      XX      XX      XX      XX      XX      XX      XX

营业费用合计            XX      XX      XX      XX      XX      XX      XX      XX      XX
  占收入比例            X%      X%      X%      X%      X%      X%      X%      X%      X%

EBITDA                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  EBITDA 利润率         X%      X%      X%      X%      X%      X%      X%      X%      X%

EBIT                    XX      XX      XX      XX      XX      XX      XX      XX      XX
  EBIT 利润率           X%      X%      X%      X%      X%      X%      X%      X%      X%

利息费用                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
利息收入                XX      XX      XX      XX      XX      XX      XX      XX      XX
其他收入/（费用）       XX      XX      XX      XX      XX      XX      XX      XX      XX

税前利润                XX      XX      XX      XX      XX      XX      XX      XX      XX

所得税                  (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  税率                  X%      X%      X%      X%      X%      X%      X%      X%      X%

净利润                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  净利率                X%      X%      X%      X%      X%      X%      X%      X%      X%

流通股数
基本股数（百万）        XX      XX      XX      XX      XX      XX      XX      XX      XX
稀释股数（百万）        XX      XX      XX      XX      XX      XX      XX      XX      XX

每股收益
基本每股收益            X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元
稀释每股收益            X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元   X.XX元
```

### 步骤5：构建现金流量表

```
现金流量表              2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

经营活动
净利润                  XX      XX      XX      XX      XX      XX      XX      XX      XX
调整项目：
  折旧和摊销            XX      XX      XX      XX      XX      XX      XX      XX      XX
  股权激励              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他非现金项目        XX      XX      XX      XX      XX      XX      XX      XX      XX

营运资金变动：
  应收账款              (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  存货                  (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  应付账款              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他营运资金          (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)

经营活动现金流          XX      XX      XX      XX      XX      XX      XX      XX      XX

投资活动
资本支出                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
收购                    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
其他投资                XX      XX      XX      XX      XX      XX      XX      XX      XX

投资活动现金流          (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)

自由现金流              XX      XX      XX      XX      XX      XX      XX      XX      XX
  FCF 利润率            X%      X%      X%      X%      X%      X%      X%      X%      X%

融资活动
债务发行                XX      XX      XX      XX      XX      XX      XX      XX      XX
债务偿还                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
股权融资                XX      XX      XX      XX      XX      XX      XX      XX      XX
股利支付                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
其他融资                XX      XX      XX      XX      XX      XX      XX      XX      XX

融资活动现金流          XX      XX      XX      XX      XX      XX      XX      XX      XX

现金净变动              XX      XX      XX      XX      XX      XX      XX      XX      XX

期初现金                XX      XX      XX      XX      XX      XX      XX      XX      XX
期末现金                XX      XX      XX      XX      XX      XX      XX      XX      XX
```

### 步骤6：构建资产负债表

创建包含35-45个行项目的完整资产负债表：

```
资产负债表              2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

资产
流动资产：
  现金及等价物          XX      XX      XX      XX      XX      XX      XX      XX      XX
  应收账款              XX      XX      XX      XX      XX      XX      XX      XX      XX
  存货                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  预付费用              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他流动资产          XX      XX      XX      XX      XX      XX      XX      XX      XX
流动资产合计            XX      XX      XX      XX      XX      XX      XX      XX      XX

非流动资产：
  固定资产原值          XX      XX      XX      XX      XX      XX      XX      XX      XX
  累计折旧              (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  固定资产净值          XX      XX      XX      XX      XX      XX      XX      XX      XX
  无形资产              XX      XX      XX      XX      XX      XX      XX      XX      XX
  商誉                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他非流动资产        XX      XX      XX      XX      XX      XX      XX      XX      XX
非流动资产合计          XX      XX      XX      XX      XX      XX      XX      XX      XX

资产合计                XX      XX      XX      XX      XX      XX      XX      XX      XX

负债
流动负债：
  应付账款              XX      XX      XX      XX      XX      XX      XX      XX      XX
  应计费用              XX      XX      XX      XX      XX      XX      XX      XX      XX
  递延收入              XX      XX      XX      XX      XX      XX      XX      XX      XX
  短期债务              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他流动负债          XX      XX      XX      XX      XX      XX      XX      XX      XX
流动负债合计            XX      XX      XX      XX      XX      XX      XX      XX      XX

非流动负债：
  长期债务              XX      XX      XX      XX      XX      XX      XX      XX      XX
  递延税项              XX      XX      XX      XX      XX      XX      XX      XX      XX
  其他非流动负债        XX      XX      XX      XX      XX      XX      XX      XX      XX
非流动负债合计          XX      XX      XX      XX      XX      XX      XX      XX      XX

负债合计                XX      XX      XX      XX      XX      XX      XX      XX      XX

权益
  普通股                XX      XX      XX      XX      XX      XX      XX      XX      XX
  资本公积              XX      XX      XX      XX      XX      XX      XX      XX      XX
  留存收益              XX      XX      XX      XX      XX      XX      XX      XX      XX
  库存股                (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  其他权益              XX      XX      XX      XX      XX      XX      XX      XX      XX
权益合计                XX      XX      XX      XX      XX      XX      XX      XX      XX

负债及权益合计          XX      XX      XX      XX      XX      XX      XX      XX      XX

勾稽检查                OK      OK      OK      OK      OK      OK      OK      OK      OK
```

**勾稽检查公式：**
- 各年资产合计必须等于负债及权益合计
- 任何不平衡以红色标记

### 步骤7：构建 DCF 输入工作表

为估值（任务3）准备输入：

```
DCF 输入                2025E   2026E   2027E   2028E   2029E

EBIT                    XX      XX      XX      XX      XX
税率                    X%      X%      X%      X%      X%
NOPAT                   XX      XX      XX      XX      XX

加：D&A                 XX      XX      XX      XX      XX
减：资本支出            (XX)    (XX)    (XX)    (XX)    (XX)
减：NWC 变动            (XX)    (XX)    (XX)    (XX)    (XX)

无杠杆自由现金流        XX      XX      XX      XX      XX

终值年份指标：
  2029E 收入            X,XXX元
  2029E EBITDA          XXX元
  2029E EBIT            XXX元
  2029E 无杠杆 FCF      XXX元
```

### 步骤8：构建情景分析工作表

创建三种情景的不同假设：

#### 情景假设表
```
假设                          乐观        基准        悲观
收入 CAGR（2025-2029）        XX%         XX%         XX%
2029E 毛利率                  XX%         XX%         XX%
2029E EBITDA 利润率           XX%         XX%         XX%
资本支出占收入比例            X%          X%          X%
[添加其他关键假设]
```

#### 情景输出表
```
指标                          乐观        基准        悲观
2029E 收入（百万元）        X,XXX元      X,XXX元      X,XXX元
2029E EBITDA（百万元）      XXX元        XXX元        XXX元
2029E EBITDA 利润率           XX%         XX%         XX%
2029E 净利润（百万元）      XXX元        XXX元        XXX元
2029E 每股收益                X.XX元       X.XX元       X.XX元
2029E FCF（百万元）         XXX元        XXX元        XXX元
2029E FCF 利润率              XX%         XX%         XX%

累计 FCF 2025-2029（百万元）XXX元        XXX元        XXX元
```

**记录情景假设依据：**
- 乐观情景：[描述乐观但可实现的假设]
- 基准情景：[描述最可能的情景]
- 悲观情景：[描述下行风险和触发因素]

### 步骤9：质量检查

**验证模型完整性：**
1. [ ] 测试所有公式（抽查计算）
2. [ ] 修改假设 → 验证模型正确更新
3. [ ] 测试情景切换
4. [ ] 验证颜色编码（蓝/黑/绿）
5. [ ] 检查各年资产负债表是否平衡
6. [ ] 验证无循环引用（Excel 会标记）
7. [ ] 检查预测中是否有硬编码数字
8. [ ] 验证所有跨表链接有效
9. [ ] 测试收入合计在所有工作表中一致
10. [ ] 检查格式和呈现

---

## 质量标准

### 模型完整性
- 所有公式在各工作表之间正确链接
- 预测中无硬编码数字（假设工作表除外）
- 无循环引用
- 各年资产负债表平衡
- 情景切换正常工作

### 完整性
- 所有6个核心工作表：收入模型、利润表、现金流量表、资产负债表、情景分析、DCF 输入
- 利润表40-50个行项目
- 收入模型20-30行（产品明细）
- 收入模型15-20行（地区明细）
- 完整的现金流量表和资产负债表含所有行项目
- 乐观/基准/悲观情景完整

### 专业格式
- 一致的颜色编码（蓝/黑/绿）
- 清晰的标题和标签
- 规范的边框和底纹
- 关键单元格的命名区域
- 可折叠的分组行
- 单位标注清晰（千元 vs. 百万元）

### 文档记录
- 假设附有依据说明（蓝色文本单元格含注释）
- 数据来源在单元格注释或工作表内注释部分注明
- 复杂计算附有解释注释
- 方法论已描述

---

## 文件命名规范

将财务模型保存为：

`[公司]_财务模型_[日期].xlsx`

示例：`Tesla_财务模型_2024-10-27.xlsx`

---

## 成功标准

一个成功的财务模型应：

1. 包含所有6个核心工作表（收入模型、利润表、现金流量表、资产负债表、情景分析、DCF 输入）
2. 完全动态（修改假设 → 模型自动更新）
3. 预测中无硬编码数字
4. 包含详细的收入分解（按产品20-30行，按地区15-20行）
5. 利润表包含40-50个行项目
6. 包含乐观/基准/悲观情景
7. 专业格式化，带颜色编码
8. 勾稽平衡（资产负债表、现金流量表）
9. 可审计且易于追踪
10. 支持估值分析，含正确的 FCF 计算

---

## 常见模型类型 - 特别注意事项

### 高增长科技/SaaS
- 关注 ARR 增长和净留存率
- 按产品线和地区建模
- 研发和销售营销支出较重
- 盈利时间线
- 单位经济模型（LTV/CAC）

### 电商/零售
- 按产品类别和渠道划分收入
- 门店数量和同店增长（如适用）
- 存货周转和营运资金
- 履约成本
- 客户获取

### 制造/工业
- 产能利用率
- 原材料成本和定价
- 毛利率桥接（量/价/组合/成本）
- 资本支出密集型模型
- 营运资金周期

---

## 后续步骤

完成任务2后，财务模型将用于：
- **任务3（估值）**：DCF 输入、预测财务数据
- **任务4（图表）**：收入趋势、利润率图表、情景比较的数据
- **任务5（报告组装）**：报告表格和分析的财务数据
