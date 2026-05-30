# Claude 金融套件（中文版）

基于 [Anthropic `financial-services`](https://github.com/anthropics/financial-services) 仓库的中文汉化+本土化版本。

为最常见的金融工作流——投行、权益研究、私募股权和财富管理——提供参考 Agent（智能体）、Skill（技能）和 MCP（模型上下文协议）数据连接器。

> [!IMPORTANT]
> 本仓库不构成投资、法律、税务或会计建议。这些 Agent 起草分析师工作成果——模型、备忘录、研究报告、对账表——供专业人士审查。它们不做出投资建议、执行交易、承担风险、记入账簿或审批准入；所有输出均需人工签字确认。你有责任验证输出内容，并确保符合你所在公司适用的法律法规。

## 与原仓库的关系

本仓库是 `anthropics/financial-services` 的中文汉化+本土化版本：

- **原仓库结构不变**——所有文件路径、目录名、plugin.json 配置保持一致
- **全部 markdown 内容已翻译为中文**
- **已完成本土化适配**——SEC→巨潮资讯网、Bloomberg→Wind/iFinD、GAAP→企业会计准则、美元→人民币等
- **跳过 partner-built 插件**（LSEG、S&P Global）——国内基本用不上

## 快速开始

### 先说明：是否需要下载本仓库？

本套件不是一个需要双击运行或 `pip install` 的普通软件项目，而是一组给 Claude Code 使用的插件、Agent 和 Skill。

所以，**不一定需要先克隆或下载仓库**。真正的安装动作是：

1. 先安装并打开 Claude Code；
2. 把本仓库添加为 Claude Code 的插件市场源；
3. 再从这个市场源里安装需要的插件。

仓库只是“插件来源”。你可以直接用 GitHub 仓库地址作为来源，也可以先把仓库下载到本地，再用本地路径作为来源。

| 情况 | 是否需要先下载仓库 | 建议做法 |
|---|---:|---|
| 能稳定访问 GitHub | 不需要 | 直接添加 GitHub 仓库地址 |
| 国内网络不稳定 | 建议下载 | 先克隆或下载 zip，再添加本地路径 |
| 想先查看或修改文件 | 建议下载 | 在本地目录中添加插件市场源 |

如果你是第一次使用 Claude Code，或者不确定选哪种方式，**建议先把仓库下载到本地，再按本地路径安装**。这样更容易排查问题。

### 先分清：系统终端和 Claude Code 对话界面

安装时会同时看到“终端”和“Claude Code”，新手很容易混淆。请先记住：

| 你要做的事 | 在哪里操作 |
|---|---|
| 克隆仓库、进入目录、添加插件市场源、安装插件、查看插件列表 | **系统终端**，如 macOS Terminal、iTerm、Windows Terminal，或 AI 助手代你操作的终端 |
| 使用 `/dcf`、`/comps` 等斜杠命令，或输入“帮我做某某分析” | **Claude Code 对话界面** |
| 让 AI 助手自动帮你安装 | 把提示词发给**能操作本机终端的 AI 助手** |

下面所有 `bash` 代码块里的命令，例如 `git clone`、`cd`、`claude plugin marketplace add ./`、`claude plugin install ...`，都应在**系统终端**里执行，不是发到 Claude Code 对话里的聊天内容。

特别注意：即使命令以 `claude` 开头，它仍然是系统终端里的管理命令。如果你已经进入 Claude Code 对话界面，请先回到普通终端提示符后再执行这些安装命令。

### 新手推荐：让 AI 助手帮你安装

如果你不熟悉命令行，推荐把下面这段话复制给能操作本机终端的 AI 助手（例如 Claude Code、Codex 等），让它按指引自动完成安装：

```text
阅读 https://raw.githubusercontent.com/jarodong/claude-for-financial-services-ZH/main/skill.md ，帮我安装 Claude 金融套件中文版。请优先使用本地仓库路径；如果本机已经下载过仓库，不要重复克隆或覆盖。请安装国企投资人推荐组合：financial-analysis、investment-banking、equity-research、private-equity、market-researcher、model-builder。安装后运行 claude plugin list 验证，并把结果告诉我。
```

注意：普通网页聊天机器人通常不能直接安装本机插件；必须使用具备本机终端权限的 Agent。

如果你是在本地测试、还没有把最新版推送到 GitHub，可以把上面提示词中的链接改成“当前仓库根目录的 `skill.md`”。

### 方式一：Claude Code 插件安装（推荐）

#### 第 1 步：确认 Claude Code 可用

在系统终端执行：

```bash
claude --version
```

如果这一步没有版本号输出，说明 Claude Code 还没有安装好。请先完成 Claude Code 的安装、登录和基础配置。

#### 第 2 步：添加插件市场源

选择下面一种方式即可。

**A. 直接使用 GitHub 仓库地址**

适合网络环境正常的用户：

在系统终端执行：

```bash
claude plugin marketplace add <本仓库 GitHub 地址>
```

**B. 使用本地仓库路径**

适合国内网络不稳定、想先查看文件，或已经下载本仓库的用户。先用下面任意一种方式把仓库文件放到本地：

在系统终端执行：

```bash
# 如果你熟悉 git，可以克隆仓库
git clone <本仓库 GitHub 地址>
cd claude-for-financial-services-ZH
```

如果你是从网页下载 zip 文件，则先解压，然后进入解压后的目录。

进入本仓库目录后，执行：

在系统终端执行：

```bash
claude plugin marketplace add ./
```

注意：这里要写 `./`，不要只写 `.`。Claude Code 要求本地路径使用 `./path` 这种格式。

#### 第 3 步：先看推荐安装组合

本仓库里有两类常见安装对象：

- **垂直插件**：不是单个 Skill，而是按金融业务场景打包的一组 Skill、斜杠命令、hooks 和相关配置。例如 `financial-analysis` 里包含 DCF、Comps、LBO、三表模型、Excel 审计等多个能力。
- **Agent 插件**：以一个智能体为中心，通常包含一个 Agent 说明和它常用的一组 Skill。例如 `market-researcher` 负责行业研究，`model-builder` 负责模型构建。

如果你是国企投资人、产业投资人员，或者主要做项目研究、尽调、投决材料和领导汇报，建议先安装下面 6 个。可以把它理解为本中文版的**推荐必装组合**：

| 类型 | 插件/Agent | 为什么建议先装 |
|---|---|---|
| 垂直插件 | `financial-analysis` | 核心财务分析能力：Comps、DCF、LBO、三表模型、Pitch Deck 质检、Excel 审计 |
| 垂直插件 | `investment-banking` | 交易和项目材料能力：CIM、Teaser、流程函、买家列表、并购模型、交易跟踪 |
| 垂直插件 | `equity-research` | 研究分析能力：财报分析、首次覆盖、模型更新、投资论点和催化剂跟踪 |
| 垂直插件 | `private-equity` | 股权投资工作流：项目源、筛选、尽调清单、投决会备忘录、投后监控 |
| Agent | `market-researcher` | 行业研究、竞争格局、同业可比、投资想法候选 |
| Agent | `model-builder` | DCF、LBO、三表模型、可比公司模型构建 |

其他 Agent 和插件可以后续按工作需要再安装；新手不用一开始全部装完。

#### 第 4 步：安装推荐必装组合

在系统终端执行：

```bash
# 垂直插件：建议国企投资和产业投资场景先装
claude plugin install financial-analysis@claude-for-financial-services
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
claude plugin install private-equity@claude-for-financial-services

# Agent：建议先装这两个
claude plugin install market-researcher@claude-for-financial-services
claude plugin install model-builder@claude-for-financial-services
```

#### 第 5 步：检查是否安装成功

在系统终端执行：

```bash
claude plugin list
```

确认列表中至少包含并启用下面 6 个：

```text
financial-analysis
investment-banking
equity-research
private-equity
market-researcher
model-builder
```

#### 第 6 步：在 Claude Code 对话界面验证

如果你是在安装插件之前就已经打开了 Claude Code 会话，请先退出当前会话并重新打开 Claude Code。新安装的插件和斜杠命令通常需要在新会话中加载。

验证时请优先使用带插件命名空间的斜杠命令，不要直接用“帮我计算某某公司的 DCF”这类自然语言做安装验证。因为如果你同时安装了 Wind 等其他金融 Skill，Claude Code 可能会自动触发 Wind 的 `dcf-model`，而不是本套件的命令。

在 Claude Code 对话界面输入：

```text
/financial-analysis:dcf 牧原食品
/financial-analysis:comps 牧原食品
/financial-analysis:lbo 牧原食品
```

正常情况下，`/financial-analysis:dcf` 开始时应说明：

```text
本次使用的是 Claude 金融套件中文版的 `/financial-analysis:dcf` 命令来组织 DCF 估值流程；Wind MCP / Wind MCP Skill 仅作为财务和行情数据源使用，不是使用 Wind 的 DCF Skill。
```

这句话用于区分“DCF 分析框架”和“数据来源”：金融套件负责 DCF 方法、模型结构和交叉验证；Wind MCP 只负责提供数据。

注意：`/financial-analysis:dcf` 是斜杠命令 / Command，不是一个独立 Skill。它可以调用本套件内部的 `dcf-model` Skill 和 `comps-analysis` Skill。

如果已经显示 `Skill(financial-analysis:dcf) Successfully loaded skill`，但开场没有上面这句说明，且第一步就去 `Web Search`，通常不是安装失败，而是当前 Claude Code 会话或已安装插件缓存仍在使用旧版本指令。请在系统终端里更新插件，然后重启 Claude Code：

```bash
claude plugin marketplace update
claude plugin update financial-analysis@claude-for-financial-services
claude plugin update model-builder@claude-for-financial-services
```

如果你的 Claude Code 中也能看到短命令 `/dcf`、`/comps`、`/lbo`，也可以使用；但在存在多个同名 Skill 时，带命名空间的命令更清楚。

不要用“请使用 claude-for-financial-services-ZH 的 financial-analysis 插件”这类说法来验证。`financial-analysis` 是插件包名称，不是可直接对话调用的 Agent 名称；这样说可能会让 Claude Code 去搜索外部插件市场，甚至触发其他插件工具。

如果 Claude Code 提示读取 `/tmp/wind-skills/.../dcf-model/SKILL.md`，说明这次触发的是 Wind 的 Skill，不是本套件的 DCF 命令。此时不代表本套件安装失败，应退出并重新打开 Claude Code 后，再用 `/financial-analysis:dcf 牧原食品` 这类斜杠命令验证。

如果输入 `/lb` 时看到多个 `lbo-model`，例如 `lbo-model (model-builder)` 和 `lbo-model (financial-analysis)`，这是正常现象。这说明不同插件里都打包了同名底层 Skill。优先选择 `/financial-analysis:lbo` 这种 Command，而不是 `lbo-model` 这种底层 Skill。

日常使用时，也可以用自然语言触发其他场景：

```text
帮我研究一下中国精神神经类药物行业
帮我做恩华药业和人福医药的可比分析
```

### 方式二：Cowork 插件安装

在 Cowork 中，打开 **Settings → Plugins → Add plugin**，然后：

- **粘贴本仓库 URL**：从列表中选择需要的 Agent 或垂直插件。
- **上传 zip**：将 `plugins/` 下任意插件目录（如 `plugins/agent-plugins/pitch-agent/`）压缩后上传。

### 方式三：手动复制 Skill（不推荐，仅作兜底）

这一路径不作为推荐安装方式。它受本地路径、工具版本和不同 AI 编程软件 Skill 目录规则影响较大；只有在暂时不能使用插件安装，或使用的工具只支持 Skill 文件夹时，才考虑手动复制。

以 Claude Code 传统 Skill 目录为例：

```bash
# 先创建 Skill 目录
mkdir -p ~/.claude/skills

# 只复制你确实需要的单个 Skill
cp -R plugins/vertical-plugins/financial-analysis/skills/dcf-model ~/.claude/skills/
cp -R plugins/vertical-plugins/financial-analysis/skills/comps-analysis ~/.claude/skills/
cp -R plugins/vertical-plugins/equity-research/skills/thesis-tracker ~/.claude/skills/
```

注意：手动复制 Skill 不等于安装完整插件。若要使用完整 Agent、斜杠命令或 MCP 连接器，优先使用方式一或方式二。本节保留，主要是为了完整呈现原仓库的 Skill 文件使用方式。

### 方式四：Claude Managed Agents（不推荐，仅作原仓库能力参考）

这一路径依赖 Anthropic API、网络环境、账号权限和云端 Agent 配置，国内用户通常不建议作为快速开始路径。这里保留命令，仅用于理解原仓库支持的部署形态：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

### 新手常见问题

**Q：有必要克隆仓库吗？**
A：不是必须。能稳定访问 GitHub 时，可以直接添加仓库地址；国内网络不稳定时，建议先克隆或下载到本地，再添加本地路径。

**Q：克隆以后是不是 Agent 和 Skill 就自动安装了？**
A：不是。克隆只是获取文件，安装还需要执行 `claude plugin marketplace add ...` 和 `claude plugin install ...`。

**Q：我已经在仓库目录里，为什么 `claude plugin marketplace add .` 报错？**
A：本地路径要写成 `./` 或 `./path`。如果已经进入本仓库目录，请执行 `claude plugin marketplace add ./`。

**Q：这些命令是在终端里输入，还是在 Claude Code 里输入？**
A：安装命令都在系统终端里输入；安装完成后，`/dcf`、`/comps` 和自然语言任务才是在 Claude Code 对话界面里使用。

**Q：为什么我说“帮我计算 DCF”，Claude Code 反而调用了 Wind 的 Skill？**
A：这是正常的自动选择结果，不一定说明本套件没装好。你本机如果同时安装了 Wind 的 `dcf-model` 等 Skill，自然语言可能会触发 Wind。验证本套件时，优先使用 `/financial-analysis:dcf 牧原食品`、`/financial-analysis:comps 牧原食品` 这类带命名空间的斜杠命令。

**Q：为什么我说“使用 financial-analysis 插件”，Claude Code 去调用 42plugin 了？**
A：`financial-analysis` 是插件包名称，不是一个可直接点名调用的 Agent。用自然语言说“使用某插件”可能会让 Claude Code 误以为你要搜索或安装插件，于是触发 42plugin 等外部插件工具。验证时不要这样说，请直接使用 `/financial-analysis:dcf 牧原食品` 这类斜杠命令。

**Q：`/dcf` 还是看不到或不能用怎么办？**
A：先确认系统终端里 `claude plugin list` 显示 `financial-analysis` 已安装并启用；然后退出当前 Claude Code 会话，重新打开一个新会话，再输入 `/` 查看是否出现 `dcf`、`comps`、`lbo` 等命令。

**Q：为什么会看到多个同名 Skill，比如 `lbo-model (model-builder)` 和 `lbo-model (financial-analysis)`？**
A：这是正常的。Agent 插件为了自包含，会打包自己常用的 Skill；垂直插件也会打包同名 Skill，所以同一个底层 Skill 可能出现多次。括号里的 `model-builder`、`financial-analysis` 表示来源插件。做验证和日常使用时，优先用 `/financial-analysis:lbo`、`/financial-analysis:dcf` 这类 Command。

**Q：怎么判断到底用的是 Wind 的 DCF Skill，还是 Claude 金融套件的 DCF？**
A：看触发命令和开场说明。使用 `/financial-analysis:dcf 公司名` 时，应该由 Claude 金融套件组织 DCF 流程，并说明 Wind MCP 只是数据源。如果日志显示读取 `/tmp/wind-skills/.../dcf-model/SKILL.md`，或没有出现金融套件的来源说明，就可能触发了 Wind 的 DCF Skill 或其他同名 Skill。注意不要把 `/financial-analysis:dcf` 叫成 Skill；它是 Command。

**Q：明明显示 `Skill(financial-analysis:dcf)` 加载成功，为什么还是先 Web Search？**
A：这通常说明插件已安装，但当前会话或插件缓存还没有加载最新版指令。请在系统终端执行 `claude plugin marketplace update`、`claude plugin update financial-analysis@claude-for-financial-services`、`claude plugin update model-builder@claude-for-financial-services`，然后重启 Claude Code 再测。

**Q：DCF 模型生成 Excel 时，怎样才算符合本套件要求？**
A：Excel 里 DCF 折现、终值、权益桥、每股价值和敏感性表应当是可审计的单元格公式，而不是 Python 先算好后写进去的静态数字。Wind 取到的历史财务、行情、Beta、市值、债务和股份数可以作为硬编码输入，但应有单元格来源注释。最终交付时应说明数据来源、文件路径，以及是否完成公式重算/错误检查。

**Q：为什么不能直接说“先下载仓库”？**
A：因为下载仓库不是安装插件的必要条件。它只是获取插件来源的一种方式。真正的安装是在 Claude Code 里完成的。

**Q：垂直插件是不是 Skill？**
A：不是一个概念。垂直插件是一个打包单元，里面通常包含多个 Skill、斜杠命令和配置；Skill 是其中某个具体能力。

**Q：10 个 Agent 和 7 个垂直插件都要装吗？**
A：不用一开始全装。国企投资、产业投资、项目尽调和投决材料场景，建议先装 `financial-analysis`、`investment-banking`、`equity-research`、`private-equity`、`market-researcher`、`model-builder` 这 6 个。

**Q：方式一和手动复制 Skill 有什么区别？**
A：方式一安装的是 Claude Code 插件包，能包含 Agent、Skill、斜杠命令、hooks 和 MCP 配置；手动复制只适合复制单个 Skill，能力不完整。

**Q：这几种方式应该怎么理解？**
A：方式一是 Claude Code 插件安装；方式二是 Cowork 图形界面安装；方式三和方式四不推荐作为国内新手安装路径，只作为兜底或原仓库能力参考保留。

## 数据源配置

本套件可以配合 Wind 万得 MCP 获取金融数据，但 **Wind MCP 的安装和 API 获取是 Wind 自己的配置事项，不是本套件安装的一部分**。

如果你需要使用 Wind 数据能力，请前往 [aifinmarket.wind.com.cn](https://aifinmarket.wind.com.cn) 免费注册并获取 Wind MCP API，然后按 Wind MCP 页面中的安装说明配置即可。

不需要拥有 Wind 金融终端账号，也不需要在本套件中单独配置 `WIND_API_KEY` 环境变量。

对中国上市公司 / A 股进行 DCF、Comps 等分析时，本套件应优先使用 Wind MCP 或 Wind MCP Skill 获取财务和行情数据；只有 Wind 数据通道不可用，且用户明确同意时，才使用 Web Search 或公开网页数据作为后备。

如果你已经安装了 Wind MCP，但分析过程中仍然先进行 Web Search，请先重新打开 Claude Code 会话，确保最新插件和 Skill 指令已加载；然后使用 `/financial-analysis:dcf 牧原食品` 这类命名空间命令重新测试。

建议验证时先让 Claude Code 只做小范围测试，例如“先用 Wind MCP 获取牧原股份核心财务和行情数据，展示数据源和缺口，暂时不要生成 Excel”。确认数据通道正常后，再继续生成完整模型。这样更容易发现到底是数据源问题、插件指令问题，还是 Excel 模型生成问题。

如使用其他数据源（如 iFinD、Choice），可按对应数据源的 MCP 或接口说明另行适配。

## 仓库内容

### Agent（10 个）

| 职能 | Agent | 功能 |
|---|---|---|
| **覆盖与咨询** | **Pitch Agent（推介材料智能体）** | Comps（可比公司分析）、Precedents（可比交易分析）、LBO（杠杆收购模型）→ 品牌化 Pitch Deck（推介材料），端到端 |
| | **Meeting Prep Agent（会议准备智能体）** | 每次客户会议前生成简报包 |
| **研究与建模** | **Market Researcher（市场研究智能体）** | 行业或主题 → 行业概览、竞争格局、同行可比、投资想法候选 |
| | **Earnings Reviewer（财报复核智能体）** | 财报电话会 + 公告 → 模型更新 → 研报草稿 |
| | **Model Builder（模型构建智能体）** | DCF（折现现金流估值法）、LBO（杠杆收购模型）、三表模型、Comps（可比公司分析）——在 Excel 中实时构建 |
| **基金行政与财务运营** | **Valuation Reviewer（估值复核智能体）** | 接收 GP（普通合伙人）材料包，运行估值模板，生成 LP（有限合伙人）报告 |
| | **GL Reconciler（总分类账对账智能体）** | 发现差异，追溯根因，发起签批流程 |
| | **Month-End Closer（月末结账智能体）** | 计提、结转、差异分析 |
| | **Statement Auditor（报表审阅智能体）** | 分配前审阅 LP（有限合伙人）报表 |
| **运营与准入** | **KYC Screener（客户身份识别筛查智能体）** | 解析准入文件，运行规则引擎，标记缺失 |

### 垂直插件（7 个）

| 插件 | 功能 |
|---|---|
| **financial-analysis** *（核心）* | Comps（可比公司分析）、DCF（折现现金流估值法）、LBO（杠杆收购模型）、三表模型、Pitch Deck（推介材料）质检、Excel 审计 |
| **investment-banking** | CIM（保密信息备忘录）、Teaser（匿名推介材料）、流程函、买家列表、并购模型、交易跟踪 |
| **equity-research** | 财报分析、首次覆盖、模型更新、投资论点和催化剂跟踪 |
| **private-equity** | 项目源、筛选、尽调清单、投决会备忘录（Investment Committee Memo）、投后监控 |
| **wealth-management** | 客户回顾、财务规划、再平衡、报告、TLH（税损收割） |
| **fund-admin** | GL（总分类账）对账、差异追溯、计提、结转、差异分析、NAV（净资产值）勾稽 |
| **operations** | KYC（客户身份识别/了解你的客户）文件解析和规则网格评估 |

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

**李向东｜国资投融资与产业投资实践者**

长期从事银行对公金融、产业投资、股权投资、项目论证、投后管理、企业纾困、资产盘活和地方国资平台项目管理工作。曾在国有银行、股份制银行从事对公金融与业务管理，现主要关注产业投资、项目研判、国资风控合规、企业经营分析与 AI 工作流应用。

维护本中文版，并不只是做界面翻译，而是希望让更多金融、投资、国资平台、企业管理和项目研究人员，能够更低门槛地使用 AI 工具，提高资料整理、项目分析、报告生成、知识管理和工作流沉淀的效率。

我长期关注如何把一线投融资经验、项目研究方法、风控判断和知识管理工具结合起来，沉淀为可复用的方法、模板和系统。

本项目为个人学习、研究和开源维护工作，不代表本人所在单位意见。

交流方向：AI 工具汉化、投融资工作流、项目研究方法、国资风控合规、知识管理工具应用。

如需交流，可通过 GitHub Issue、公众号「向东 思齐行记」或微信联系。

微信：jarodong（请注明来意，仅限 AI 工具、金融套件、项目研究方法、投融资工作流等专业交流）
