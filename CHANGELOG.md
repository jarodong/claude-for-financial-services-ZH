# 更新日志

## V1.0（2026-05-29）

### 翻译层（Phase 5A/5B）— 已完成

- 全部 83 个文件完成中文翻译
- 术语评审覆盖率 100%，共修正 3 处术语偏差（sign-off→签批）
- 建立 12 条基线术语表（`translation-log/terminology-glossary.md`）

### 本土化适配层（Phase 5C）— 已完成

- SEC/EDGAR → 巨潮资讯网/年报/季报（20 个文件）
- Bloomberg/FactSet → Wind/iFinD/Choice（17 个文件）
- GAAP → 企业会计准则（5 个文件）
- 百万美元 → 百万元/人民币（32 个文件）
- IRA/401(k)/S&P 500 → 个人养老金/企业年金/沪深300（5 个文件）
- 示例公司全部替换为 A 股/H 股标的（6 个文件）
- sec-filings.md 全文重写为中国上市公司公告数据提取参考
- 5 个 agent prompt 单独修复数据供应商引用
- 51 个 skill 目录通过 sync 脚本同步

### 新增资产

- `docs-zh/TERMS.md` 第七节：7 类本土化适配规则表
- `translation-log/NEXT-SESSION-START-HERE.md`：项目状态总览

### 跳过模块

- partner-built（LSEG、S&P Global）：国内不使用
- 基础设施文件（.gitignore/.githooks/.github/）：不影响运行

---

## V0.1（2026-05-26 ~ 05-28）

### 已完成

- README.md 中文版
- CLAUDE.md 中文版
- docs-zh/TERMS.md 金融 AI 术语表（~150 条，四类处理规则）
- docs-zh/QUICKSTART.md 快速开始指南
- plugins/vertical-plugins/ 全部 7 个垂直插件翻译完成
- plugins/agent-plugins/ 全部 10 个 Agent 翻译完成
- managed-agent-cookbooks/ 全部 10 个 Managed Agent 蓝图翻译完成
- 术语表建库 + 全量盘点 + 补译 4 个缺失文件
- 方案 B 纵向下钻：全量 subagents + support files + Skills 术语评审
