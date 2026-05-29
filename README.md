# Claude 金融套件（中文版）

基于 [Anthropic `financial-services`](https://github.com/anthropics/financial-services) 仓库的中文汉化+本土化版本。

为最常见的金融工作流——投行、权益研究、私募股权和财富管理——提供的参考 Agent、Skill 和数据连接器。

> [!IMPORTANT]
> 本仓库不构成投资、法律、税务或会计建议。这些 Agent 起草分析师工作成果——模型、备忘录、研究报告、对账表——供专业人士审查。它们不做出投资建议、执行交易、承担风险、记入账簿或审批准入；所有输出均需人工签字确认。你有责任验证输出内容，并确保符合你所在公司适用的法律法规。

## 与原仓库的关系

本仓库是 `anthropics/financial-services` 的中文汉化+本土化版本：

- **原仓库结构不变**——所有文件路径、目录名、plugin.json 配置保持一致
- **全部 markdown 内容已翻译为中文**
- **已完成本土化适配**——SEC→巨潮资讯网、Bloomberg→Wind/iFinD、GAAP→企业会计准则、美元→人民币等
- **跳过 partner-built 插件**（LSEG、S&P Global）——国内基本用不上

## 快速开始

### 方式一：Claude Code（推荐）

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/claude-for-financial-services-ZH.git
cd claude-for-financial-services-ZH

# 安装依赖（如需运行脚本）
pip install -r requirements.txt  # 如有
```

在 Claude Code 中使用已安装的 Skill：

```
# 直接使用已注册的 Skill（需先将 skill 目录复制到 ~/.claude/skills/）
# 示例：搭建 DCF 模型
帮我搭一个贵州茅台的 DCF 模型

# 示例：行业研究
帮我研究一下中国精神神经类药物行业

# 示例：可比分析
帮我做恩华药业和人福医药的可比分析
```

### 方式二：手动安装 Skill

将需要的 Agent/Skill 复制到 Claude Code 的 skills 目录：

```bash
# 复制 model-builder（财务建模）
cp -r plugins/agent-plugins/model-builder/skills/* ~/.claude/skills/model-builder/
cp plugins/agent-plugins/model-builder/agents/model-builder.md ~/.claude/skills/model-builder/SKILL.md

# 复制 market-researcher（行业研究）
cp -r plugins/agent-plugins/market-researcher/skills/* ~/.claude/skills/market-researcher/
cp plugins/agent-plugins/market-researcher/agents/market-researcher.md ~/.claude/skills/market-researcher/SKILL.md

# 复制 thesis-tracker（投资论点管理）
cp -r plugins/vertical-plugins/equity-research/skills/thesis-tracker ~/.claude/skills/

# 复制 catalyst-calendar（催化剂日历）
cp -r plugins/vertical-plugins/equity-research/skills/catalyst-calendar ~/.claude/skills/
```

### 方式三：Cowork 插件

在 Cowork 中，打开 **Settings → Plugins → Add plugin**，然后：

- **粘贴本仓库 URL** —— 然后从市场列表中选择你需要的 Agent 和垂直插件，或
- **上传 zip** —— 将 `plugins/` 下任意目录（如 `plugins/agent-plugins/pitch-agent/`）压缩后拖入。

### 方式四：Claude Managed Agents

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

## 数据源配置

本套件的金融数据获取依赖 Wind 万得 MCP。使用前请确保：

1. 拥有 Wind 金融终端账号
2. 获取 Wind API Key（登录 [aifinmarket.wind.com.cn](https://aifinmarket.wind.com.cn) 开发者中心）
3. 配置 `WIND_API_KEY` 环境变量

如使用其他数据源（如 iFinD、Choice），需修改 Skill 中的数据获取逻辑。

## 仓库内容

### Agent（10 个）

| 职能 | Agent | 功能 |
|---|---|---|
| **覆盖与咨询** | **Pitch Agent** | Comps、Precedents、LBO → 品牌化 Pitch Deck，端到端 |
| | **Meeting Prep Agent** | 每次客户会议前的简报包 |
| **研究与建模** | **Market Researcher** | 行业或主题 → 行业概览、竞争格局、同行可比、投资想法候选 |
| | **Earnings Reviewer** | 财报电话会 + 公告 → 模型更新 → 研报草稿 |
| | **Model Builder** | DCF、LBO、三表、Comps —— 在 Excel 中实时构建 |
| **基金行政与财务运营** | **Valuation Reviewer** | 接收 GP 材料包，运行估值模板，生成 LP 报告 |
| | **GL Reconciler** | 发现差异，追溯根因，路由签批 |
| | **Month-End Closer** | 计提、结转、差异分析 |
| | **Statement Auditor** | 分配前审计 LP 报表 |
| **运营与准入** | **KYC Screener** | 解析准入文件，运行规则引擎，标记缺失 |

### 垂直插件（7 个）

| 插件 | 功能 |
|---|---|
| **financial-analysis** *（核心）* | Comps、DCF、LBO、三表、Deck 质检、Excel 审计 |
| **investment-banking** | CIM、Teaser、流程函、买家列表、并购模型、交易跟踪 |
| **equity-research** | 财报分析、首次覆盖、模型更新、投资论点和催化剂跟踪 |
| **private-equity** | 项目源、筛选、尽调清单、投决会备忘录、投后监控 |
| **wealth-management** | 客户回顾、财务规划、再平衡、报告、TLH |
| **fund-admin** | GL 对账、差异追溯、计提、结转、差异分析、NAV 勾稽 |
| **operations** | KYC 文件解析和规则网格评估 |

## 仓库结构

```
plugins/
  agent-plugins/               # 命名 Agent —— 每个一个自包含插件
  vertical-plugins/            # 按金融细分领域打包的 Skill + Command + MCP 连接器
  partner-built/               # 合作伙伴插件（LSEG、S&P Global，未翻译）
managed-agent-cookbooks/       # Claude Managed Agent 蓝图
scripts/                       # deploy-managed-agent.sh · check.py · validate.py · sync-agent-skills.py
docs-zh/                       # 中文专属文档（术语表、翻译规范、中国适配指南）
translation-log/               # 翻译过程记录
```

## 中文专属文档

| 文档 | 说明 |
|------|------|
| [`docs-zh/TERMS.md`](./docs-zh/TERMS.md) | 金融 AI 术语表（含本土化适配规则） |
| [`docs-zh/QUICKSTART.md`](./docs-zh/QUICKSTART.md) | 中文快速上手 |
| [`translation-log/terminology-glossary.md`](./translation-log/terminology-glossary.md) | 已确认术语对照表 |
| [`translation-log/NEXT-SESSION-START-HERE.md`](./translation-log/NEXT-SESSION-START-HERE.md) | 项目状态总览 |

## 自定义

这些是参考模板——当你根据公司方式调整时效果会更好。

- **更换连接器** —— 将 `.mcp.json` 指向你的数据提供商和内部系统。
- **添加公司上下文** —— 将你的术语、流程和格式标准放入 Skill 文件。
- **使用你的模板** —— `/ppt-template` 教 Claude 你的品牌 PowerPoint 布局。
- **调整 Agent 范围** —— 编辑 `agents/<slug>.md` 以匹配你团队的实际工作方式。

## 贡献

这里的一切都是 Markdown 和 YAML。Fork、编辑、PR。新增内容：

- 新 Skill → 添加到 `plugins/vertical-plugins/<vertical>/skills/`，然后运行 `python3 scripts/sync-agent-skills.py` 传播到打包它的所有 Agent。
- 新 Agent → `plugins/agent-plugins/<slug>/`（含 `agents/<slug>.md` + `skills/`）和对应的 `managed-agent-cookbooks/<slug>/`。
- 推送前运行 `python3 scripts/check.py` —— 它会检查每个清单、验证所有跨文件引用，并在打包 Skill 与垂直插件源不同步时报错。

## 许可证

[Apache License 2.0](./LICENSE)

---

> 本中文版基于 [anthropics/financial-services](https://github.com/anthropics/financial-services) 汉化并本土化。原仓库采用 Apache License 2.0 许可。

## 中文版维护者

**李向东**
地级市AAA国资平台市场化高管，分管投资条线、金融和康养业务板块。
微信（请注明来意）：18537762699
