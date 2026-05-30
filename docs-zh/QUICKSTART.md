# 快速上手

> 按工具类型安装中文版金融套件。先记住一句话：克隆仓库只是下载文件，不等于安装 Skill 或 Agent。

## 前置条件

- [Claude Code](https://claude.com/product/claude-code) 已安装
- 或 [Claude Cowork](https://claude.com/product/cowork) 账号

## 先分清：在哪里输入？

| 你要做的事 | 在哪里操作 |
|---|---|
| 克隆仓库、进入目录、添加插件市场源、安装插件、查看插件列表 | 系统终端，如 macOS Terminal、iTerm、Windows Terminal，或 AI 助手代你操作的终端 |
| 使用 `/dcf`、`/comps` 等斜杠命令，或输入“帮我做某某分析” | Claude Code 对话界面 |
| 让 AI 助手自动帮你安装 | 把提示词发给能操作本机终端的 AI 助手 |

下面所有 `bash` 代码块里的命令都应在系统终端里执行，不是发到 Claude Code 对话里的聊天内容。

特别注意：即使命令以 `claude` 开头，它仍然是系统终端里的管理命令。如果你已经进入 Claude Code 对话界面，请先回到普通终端提示符后再执行这些安装命令。

## 新手推荐：让 AI 助手帮你安装

如果你不熟悉命令行，推荐把下面这段话复制给能操作本机终端的 AI 助手（例如 Claude Code、Codex 等）：

```text
阅读 https://raw.githubusercontent.com/jarodong/claude-for-financial-services-ZH/main/skill.md ，帮我安装 Claude 金融套件中文版。请优先使用本地仓库路径；如果本机已经下载过仓库，不要重复克隆或覆盖。请安装国企投资人推荐组合：financial-analysis、investment-banking、equity-research、private-equity、market-researcher、model-builder。安装后运行 claude plugin list 验证，并把结果告诉我。
```

注意：普通网页聊天机器人通常不能直接安装本机插件；必须使用具备本机终端权限的 Agent。

如果你是在本地测试、还没有把最新版推送到 GitHub，可以把上面提示词中的链接改成“当前仓库根目录的 `skill.md`”。

## 方式一：Claude Code 插件安装（推荐）

仓库只是“插件来源”，不等于安装本身。你可以直接添加 GitHub 仓库地址，也可以先下载到本地后添加本地路径。

如果网络环境正常，可以直接添加仓库地址：

在系统终端执行：

```bash
claude plugin marketplace add https://github.com/jarodong/claude-for-financial-services-ZH
```

如果国内网络不稳定，建议先下载到本地：

在系统终端执行：

```bash
git clone https://github.com/jarodong/claude-for-financial-services-ZH.git
cd claude-for-financial-services-ZH
claude plugin marketplace add ./
```

如果是下载 zip 文件，解压后进入目录，再执行 `claude plugin marketplace add ./`。注意这里要写 `./`，不要只写 `.`。

推荐先安装下面 6 个插件/Agent：

在系统终端执行：

```bash
# 垂直插件：国企投资和产业投资场景建议先装
claude plugin install financial-analysis@claude-for-financial-services
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
claude plugin install private-equity@claude-for-financial-services

# Agent：建议先装这两个
claude plugin install market-researcher@claude-for-financial-services
claude plugin install model-builder@claude-for-financial-services
```

## 方式二：Cowork 安装

1. 打开 Cowork → Settings → Plugins → Add plugin
2. 粘贴仓库 URL 或上传 zip
3. 选择需要的 Agent 和垂直插件

## 方式三：手动复制 Skill（不推荐，仅作兜底）

这不是推荐安装方式。它受本地路径、工具版本和不同 AI 编程软件 Skill 目录规则影响较大；只有在不能使用 Claude Code 插件安装，或其他 AI 编程工具只支持 Skill 文件夹时，才使用这种方式。

```bash
mkdir -p ~/.claude/skills

# 只复制需要的单个 Skill
cp -R plugins/vertical-plugins/financial-analysis/skills/dcf-model ~/.claude/skills/
cp -R plugins/vertical-plugins/financial-analysis/skills/comps-analysis ~/.claude/skills/
cp -R plugins/vertical-plugins/equity-research/skills/thesis-tracker ~/.claude/skills/
```

手动复制 Skill 不等于安装完整插件。它通常不包含 Agent、斜杠命令、hooks 和 MCP 配置。本节保留，主要是为了完整呈现原仓库的 Skill 文件使用方式。

## 方式四：Claude Managed Agents（不推荐，仅作原仓库能力参考）

这一路径依赖 Anthropic API、网络环境、账号权限和云端 Agent 配置，国内用户通常不建议作为快速开始路径。这里保留命令，仅用于理解原仓库支持的部署形态：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

## 验证安装

先在系统终端确认插件已安装：

```bash
claude plugin list
```

确认列表中至少包含并启用：

```text
financial-analysis
investment-banking
equity-research
private-equity
market-researcher
model-builder
```

然后退出当前 Claude Code 会话并重新打开，再回到 Claude Code 对话界面测试。验证时优先使用带插件命名空间的斜杠命令，不要直接用“帮我计算某某公司的 DCF”这类自然语言做安装验证；如果你同时安装了 Wind 等其他金融 Skill，自然语言可能会触发 Wind 的 `dcf-model`。

```
/financial-analysis:dcf 牧原食品          # DCF 估值
/financial-analysis:comps 牧原食品        # 可比公司分析
/financial-analysis:lbo 牧原食品          # 杠杆收购模型
/earnings       # 财报分析
/ic-memo        # 投决会备忘录
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

如果 Claude Code 提示读取 `/tmp/wind-skills/.../dcf-model/SKILL.md`，说明这次触发的是 Wind 的 Skill，不代表本套件安装失败。请重新打开 Claude Code 后改用 `/financial-analysis:dcf 牧原食品`。

如果输入 `/lb` 时看到多个 `lbo-model`，例如 `lbo-model (model-builder)` 和 `lbo-model (financial-analysis)`，这是正常现象。这说明不同插件里都打包了同名底层 Skill。优先选择 `/financial-analysis:lbo` 这种 Command，而不是 `lbo-model` 这种底层 Skill。

不要用“请使用 financial-analysis 插件”这类说法验证。`financial-analysis` 是插件包名称，不是可直接对话调用的 Agent 名称；这样说可能会让 Claude Code 去搜索外部插件市场，甚至触发 42plugin 等其他插件工具。

## 推荐必装组合

垂直插件不是单个 Skill，而是按金融业务场景打包的一组 Skill、斜杠命令和相关配置。Agent 插件则是一个智能体加它常用的一组 Skill。

| 类型 | 插件/Agent | 用途 |
|------|------|------|
| 垂直插件 | financial-analysis | Comps、DCF、LBO、三表模型、Pitch Deck 质检、Excel 审计 |
| 垂直插件 | investment-banking | CIM、Teaser、流程函、买家列表、并购模型、交易跟踪 |
| 垂直插件 | equity-research | 财报分析、首次覆盖、模型更新、投资论点和催化剂跟踪 |
| 垂直插件 | private-equity | 项目源、筛选、尽调清单、投决会备忘录、投后监控 |
| Agent | market-researcher | 行业研究、竞争格局、同业可比、投资想法候选 |
| Agent | model-builder | DCF、LBO、三表模型、可比公司模型构建 |

## 常见问题

**Q: 安装后 Skill 没有触发？**
A: 先运行 `claude plugin list` 确认插件已安装并启用。验证本套件时优先使用 `/financial-analysis:dcf 牧原食品`、`/financial-analysis:comps 牧原食品` 这类带命名空间的斜杠命令。

**Q: 克隆仓库后是否已经安装？**
A: 没有。克隆只是下载文件，还需要执行 `claude plugin marketplace add ...` 和 `claude plugin install ...`。

**Q: 已经在仓库目录里，为什么 `claude plugin marketplace add .` 报错？**
A: 本地路径要写成 `./` 或 `./path`。如果已经进入本仓库目录，请执行 `claude plugin marketplace add ./`。

**Q: 这些命令是在终端里输入，还是在 Claude Code 里输入？**
A: 安装命令都在系统终端里输入；安装完成后，`/dcf`、`/comps` 和自然语言任务才是在 Claude Code 对话界面里使用。

**Q: 为什么我说“帮我计算 DCF”，Claude Code 反而调用了 Wind 的 Skill？**
A: 这是正常的自动选择结果，不一定说明本套件没装好。你本机如果同时安装了 Wind 的 `dcf-model` 等 Skill，自然语言可能会触发 Wind。验证本套件时，优先使用 `/financial-analysis:dcf 牧原食品`。

**Q: 为什么我说“使用 financial-analysis 插件”，Claude Code 去调用 42plugin 了？**
A: `financial-analysis` 是插件包名称，不是可直接点名调用的 Agent。用自然语言说“使用某插件”可能会让 Claude Code 误以为你要搜索或安装插件，于是触发 42plugin 等外部插件工具。验证时不要这样说，请直接使用 `/financial-analysis:dcf 牧原食品` 这类斜杠命令。

**Q: `/dcf` 还是看不到或不能用怎么办？**
A: 先确认系统终端里 `claude plugin list` 显示 `financial-analysis` 已安装并启用；然后退出当前 Claude Code 会话，重新打开一个新会话，再输入 `/` 查看是否出现 `dcf`、`comps`、`lbo` 等命令。

**Q: 为什么会看到多个同名 Skill，比如 `lbo-model (model-builder)` 和 `lbo-model (financial-analysis)`？**
A: 这是正常的。Agent 插件为了自包含，会打包自己常用的 Skill；垂直插件也会打包同名 Skill，所以同一个底层 Skill 可能出现多次。括号里的 `model-builder`、`financial-analysis` 表示来源插件。做验证和日常使用时，优先用 `/financial-analysis:lbo`、`/financial-analysis:dcf` 这类 Command。

**Q: 怎么判断到底用的是 Wind 的 DCF Skill，还是 Claude 金融套件的 DCF？**
A: 看触发命令和开场说明。使用 `/financial-analysis:dcf 公司名` 时，应该由 Claude 金融套件组织 DCF 流程，并说明 Wind MCP 只是数据源。如果日志显示读取 `/tmp/wind-skills/.../dcf-model/SKILL.md`，或没有出现金融套件的来源说明，就可能触发了 Wind 的 DCF Skill 或其他同名 Skill。注意不要把 `/financial-analysis:dcf` 叫成 Skill；它是 Command。

**Q: 明明显示 `Skill(financial-analysis:dcf)` 加载成功，为什么还是先 Web Search？**
A: 这通常说明插件已安装，但当前会话或插件缓存还没有加载最新版指令。请在系统终端执行 `claude plugin marketplace update`、`claude plugin update financial-analysis@claude-for-financial-services`、`claude plugin update model-builder@claude-for-financial-services`，然后重启 Claude Code 再测。

**Q: DCF 模型生成 Excel 时，怎样才算符合本套件要求？**
A: Excel 里 DCF 折现、终值、权益桥、每股价值和敏感性表应当是可审计的单元格公式，而不是 Python 先算好后写进去的静态数字。Wind 取到的历史财务、行情、Beta、市值、债务和股份数可以作为硬编码输入，但应有单元格来源注释。最终交付时应说明数据来源、文件路径，以及是否完成公式重算/错误检查。

**Q: Claude Code 插件安装和手动复制 Skill 有什么区别？**
A: 插件安装是完整安装路径；手动复制只是兜底，只适合单个 Skill。

**Q: 垂直插件是不是 Skill？**
A: 不是。垂直插件是打包单元，里面通常包含多个 Skill、斜杠命令和配置；Skill 是其中某个具体能力。

**Q: 10 个 Agent 和 7 个垂直插件都要装吗？**
A: 不用一开始全装。国企投资、产业投资、项目尽调和投决材料场景，建议先装推荐必装组合里的 6 个。

**Q: 为什么方式三和方式四不推荐？**
A: 这两种方式更容易受国内网络、账号/API、工具版本和本地路径影响。作为汉化文档可以保留，但新手优先走方式一或方式二。

**Q: 如何查看已安装的插件？**
A: 运行 `claude plugin list` 或在 Cowork Settings 中查看。

**Q: MCP 连接器需要额外配置吗？**
A: 本套件安装不等于安装 Wind MCP。需要 Wind 数据能力时，请前往 [aifinmarket.wind.com.cn](https://aifinmarket.wind.com.cn) 免费注册并获取 Wind MCP API，然后按 Wind MCP 页面说明配置即可。不需要 Wind 金融终端账号，也不需要在本套件中单独配置 `WIND_API_KEY` 环境变量。

**Q: 为什么 DCF 分析没有自动使用 Wind MCP，反而先 Web Search？**
A: 这通常是因为 Wind MCP 是独立 Skill/CLI 形式安装，当前插件指令没有在旧会话中加载到“优先 Wind”的规则。请重新打开 Claude Code，会话中使用 `/financial-analysis:dcf 牧原食品`。对中国上市公司 / A 股，本套件应优先使用 Wind MCP 或 Wind MCP Skill；只有 Wind 数据通道不可用且用户同意时，才使用 Web Search。

建议验证时先让 Claude Code 只做小范围测试，例如“先用 Wind MCP 获取牧原股份核心财务和行情数据，展示数据源和缺口，暂时不要生成 Excel”。确认数据通道正常后，再继续生成完整模型。

---

> 详细翻译规范和术语表参见 [`docs-zh/TERMS.md`](./TERMS.md)。
