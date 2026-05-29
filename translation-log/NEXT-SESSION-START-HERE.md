# 本土化适配完成 — 项目状态总览

**最后更新**:2026-05-29
**项目**:Anthropic 金融套件中文化(`claude-for-financial-services-ZH`)
**执行人**:李向东 + Claude Code

---

## 一、一句话现状

**翻译覆盖率 100%,术语评审覆盖率 100%,本土化适配覆盖率 100%。** 全部 83 个文件已完成术语评审和本土化适配。翻译层和本土化层均已收工。

---

## 二、完整评审记录(2026-05-26 ~ 05-28)

| 日期 | 工作内容 | 文件数 | 修正数 |
|---|---|---:|---:|
| 05-26 | 大批量初译 + 3 个核心 Agent 主提示词深度评审 | ~113 | 10 |
| 05-27 | 术语表建库 + 全量盘点 + 补译 4 个缺失文件 | 4 | 0 |
| 05-28 | 方案 B 纵向下钻:全量 subagents + support files + Skills 术语评审 | 83 | 3 |

### 05-28 评审明细

| 类别 | 文件数 | 修正数 | 修正内容 |
|---|---:|---:|---|
| subagent YAML(30 个) | 30 | 0 | 全部通过 |
| support files(README + agent.yaml + steering-examples) | 21 | 1 | statement-auditor README "签署"→"签批" |
| Skill SKILL.md(~40 个) | ~32 | 2 | gl-recon "签署包"→"签批包"; valuation-reviewer "签署"→"签批" |

---

## 三、修正清单(全项目共 3 处)

| # | 文件 | 修正 | 术语规则 |
|---|---|---|---|
| 1 | `statement-auditor/README.md` | "人工签署"→"人工签批" | sign-off→签批 |
| 2 | `gl-reconciler/skills/gl-recon/SKILL.md` | "签署包"→"签批包" | sign-off→签批 |
| 3 | `valuation-reviewer/README.md` | "签署"→"签批" | sign-off→签批 |

---

## 四、术语基线(已确认,全项目强制执行)

| 领域 | 英文 | 正确译法 | 错误译法 |
|---|---|---|---|
| PE/VC | Waterfall | **分配瀑布** | 瀑布图 |
| PE/VC | marks | **报告估值** | 报告标记 |
| PE/VC | underwriting | **交易时的投资评估** | 交易时承销 |
| KYC | escalation | **上报** | 升级 |
| KYC | negative media | **负面舆情** | 负面媒体 |
| KYC | compliance sign-off | **合规签批** | 合规签署 |
| KYC | PEP | **PEP(政治公众人物)** | PEP(不加注) |
| 基金会计 | system drift | **系统口径差异** | 系统漂移 |
| 基金会计 | sign-off | **签批** | 签署 |
| 基金会计 | posting | **入账** | 账簿过账 |
| 基金会计 | untrusted source | **不受信来源** | 不受信任的来源 |
| KYC | the firm | **本机构** | 公司/事务所 |

完整术语表见 `translation-log/terminology-glossary.md`。

---

## 五、已建立的资产文件

| 文件 | 路径 | 用途 |
|---|---|---|
| 术语表 | `translation-log/terminology-glossary.md` | 12 条已确认术语对照,评审强制基线 |
| 全量盘点表 | `translation-log/inventory-status.md` | 按模块的文件清单与翻译状态 |
| 本文 | `translation-log/NEXT-SESSION-START-HERE.md` | 项目状态总览 |

---

## 六、已完成评审的全部文件清单

### 10 个 Agent 主提示词

`plugins/agent-plugins/{kyc-screener,gl-reconciler,valuation-reviewer,earnings-reviewer,market-researcher,meeting-prep-agent,model-builder,month-end-closer,pitch-agent,statement-auditor}/agents/*.md`

### 30 个 subagent YAML

`managed-agent-cookbooks/<agent>/subagents/{三个子代理}.yaml`

### 21 个 support 文件

`managed-agent-cookbooks/<agent>/{README.md, agent.yaml, steering-examples.json}` × 7 个 Agent(3 个核心 Agent 的 README 在第一天已评审)

### ~40 个 Skill SKILL.md

覆盖全部 10 个 Agent 的 Skills,含共享 Skill(skills, audit-xls, pptx-author, comps-analysis, sector-overview, 3-statement-model, dcf-model, lbo-model)在多 Agent 间的身份一致性确认。

---

## 七、已决策跳过

| 模块 | 原因 |
|---|---|
| partner-built(LSEG、S&P Global) | 国内不使用 |
| 基础设施文件(.gitignore/.githooks/.github/) | 不影响运行 |

---

## 八、过程教训

1. **术语表是锚**:没有术语表,每次评审都是主观判断;有了术语表,评审变成机械化比对,效率和一致性都高。
2. **先盘点再动手**:全量盘点发现实际缺失远少于预期,避免了遗漏或重复。
3. **共享 Skill 必须确认一致性**:audit-xls、xlsx-author 等 Skill 在 7+ 个 Agent 间共享,必须确认各副本与源一致。
4. **sign-off 是最高频偏差词**:3 处修正全部来自 sign-off→签批,说明金融语境下"签署"vs"签批"是最容易误译的术语。

---

**结论**:全项目 83 个文件术语评审完毕,3 处修正已落地。翻译层收工。本土化适配层(Phase 5C)已完成,详见下方记录。

---

## 九、Phase 5C 本土化适配层完成记录(2026-05-29)

### 一句话总结

全部操作文件已从"美国金融语境的中文翻译"升级为"中国金融语境的可用工具"。SEC/EDGAR→巨潮资讯网、Bloomberg→Wind/iFinD、GAAP→企业会计准则、百万美元→百万元、IRA→个人养老金账户、示例公司全部替换为中国 A 股/H 股标的。

### 执行记录

| Phase | 内容 | 修改文件数 | 替换数 |
|---|---|---|---|
| 0 | TERMS.md 第七节:本土化适配规则 | 1 | 7 类规则表 |
| 1 | sec-filings.md 重写 | 1(+2 sync) | 全文重写 |
| 2 | SEC/EDGAR 引用替换 | 20 | ~60 |
| 3 | 数据供应商替换 | 17 | ~40 |
| 4 | GAAP 引用替换 | 5 | 9 |
| 5 | USD 货币引用替换 | 32 | ~100 |
| 6 | 美国金融产品替换 | 5 | ~15 |
| 7 | 示例公司替换 | 6 | ~25 |
| 8 | 同步验证+agent prompt 修复 | 5 | 7 |

### 建立的新资产

| 文件 | 路径 | 用途 |
|---|---|---|
| 本土化适配规则 | `docs-zh/TERMS.md` 第七节 | 7 类替换规则表,后续维护基线 |
| 中国公告数据提取参考 | `vertical-plugins/.../sec-filings.md` | 从 SEC 指南重写为中国上市公司公告提取指南 |

### 保留的美国引用(跨境附录)

sec-filings.md 的"附录:跨境场景"中保留了 SEC EDGAR 内容,用于分析在美上市的中国公司。这是预期行为,不是遗漏。

### 过程教训

1. **先建规则再动手**:TERMS.md 第七节的替换规则表确保了跨文件一致性。
2. **按类别批量替换**:按替换类别(而非按文件)推进,避免遗漏。
3. **sync 脚本是关键**:51 个 skill 目录通过脚本自动同步,手动编辑 agent-plugins 副本会引入不一致。
4. **agent prompt 不走 sync**:5 个 agent 主提示词需要单独修复。
5. **跨境场景需保留**:不能一味删除美国引用,需区分"默认假设"和"跨境场景"。
