# Claude 金融套件中文版安装指引

你正在帮助用户安装 `claude-for-financial-services-ZH`。请按本文件执行，不要让用户手动猜命令。

## 安装目标

为 Claude Code 安装本中文版金融套件的推荐组合：

1. `financial-analysis`
2. `investment-banking`
3. `equity-research`
4. `private-equity`
5. `market-researcher`
6. `model-builder`

这 4 个垂直插件和 2 个 Agent 适合国企投资、产业投资、项目研究、尽调、投决材料和领导汇报等场景。

## 执行前提

你必须能操作用户本机终端。若你无法运行终端命令，应直接告诉用户：需要换到 Claude Code、Codex 或其他具备本机终端权限的 Agent 中执行。

请向用户说明：本文件中的 `claude --version`、`git clone`、`cd`、`claude plugin marketplace add ./`、`claude plugin install ...`、`claude plugin list` 都是在系统终端里执行的命令，不是发送到 Claude Code 对话界面的聊天内容。即使命令以 `claude` 开头，它仍然是系统终端里的管理命令。安装完成后，用户才回到 Claude Code 对话界面使用 `/dcf`、`/comps` 或自然语言任务。

## 执行原则

- 不要删除或覆盖用户已有仓库。
- 不要重复克隆到同名目录。
- 国内用户优先使用本地仓库路径安装。
- 如果命令失败，保留报错原文，并说明下一步怎么处理。
- 不要使用 `sudo`。
- 不要修改仓库文件，除非用户明确要求。

## 第 1 步：确认 Claude Code 可用

运行：

```bash
claude --version
```

如果没有版本号输出，说明 Claude Code 尚未安装或未配置好。请先让用户完成 Claude Code 安装、登录和基础配置。

## 第 2 步：确定插件市场源

优先使用本地仓库路径。

如果当前目录就是本仓库根目录，并且存在 `.claude-plugin/marketplace.json`，执行：

```bash
claude plugin marketplace add ./
```

注意：必须写 `./`，不要写 `.`。

如果当前目录不是本仓库，请先询问用户本仓库所在路径，或检查用户是否已经下载到类似下面的位置：

```text
~/Documents/claude-for-financial-services-ZH
```

进入实际仓库目录后，再执行：

```bash
claude plugin marketplace add ./
```

如果用户尚未下载仓库，且网络环境可以访问 GitHub，可选择添加远程仓库源：

```bash
claude plugin marketplace add jarodong/claude-for-financial-services-ZH
```

如果远程方式失败，建议用户先下载或克隆仓库到本地，再用本地路径安装。

## 第 3 步：安装推荐组合

运行：

```bash
claude plugin install financial-analysis@claude-for-financial-services
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
claude plugin install private-equity@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services
claude plugin install model-builder@claude-for-financial-services
```

如果提示某个插件已经安装，通常可以继续安装后面的插件。

如果用户已经安装过旧版本，先更新本地插件市场和关键插件：

```bash
claude plugin marketplace update
claude plugin update financial-analysis@claude-for-financial-services
claude plugin update model-builder@claude-for-financial-services
```

## 第 4 步：验证安装

先在系统终端运行：

```bash
claude plugin list
```

确认列表中至少包含：

- `financial-analysis`
- `investment-banking`
- `equity-research`
- `private-equity`
- `market-researcher`
- `model-builder`

然后请提醒用户：如果是在安装插件之前就已经打开了 Claude Code 会话，请先退出当前会话并重新打开 Claude Code。新安装的插件和斜杠命令通常需要在新会话中加载。

回到 Claude Code 对话界面验证时，优先使用带插件命名空间的斜杠命令，不要直接用“帮我计算某某公司的 DCF”作为验证方式。若用户同时安装了 Wind 等其他金融 Skill，自然语言可能触发 Wind 的 `dcf-model`。

建议用户在 Claude Code 对话界面输入：

```text
/financial-analysis:dcf 牧原食品
/financial-analysis:comps 牧原食品
```

如果 Claude Code 提示读取 `/tmp/wind-skills/.../dcf-model/SKILL.md`，说明这次触发的是 Wind 的 Skill，不代表本套件安装失败。请建议用户重新打开 Claude Code 后，改用 `/financial-analysis:dcf 牧原食品`。

不要建议用户用“请使用 financial-analysis 插件”这类自然语言做验证。`financial-analysis` 是插件包名称，不是可直接对话调用的 Agent 名称；这样说可能会让 Claude Code 去搜索外部插件市场，甚至触发 42plugin 等其他插件工具。

如果用户看到多个同名 Skill，例如 `lbo-model (model-builder)` 和 `lbo-model (financial-analysis)`，请说明这是正常现象：Agent 插件和垂直插件可能都打包同名底层 Skill。建议用户优先使用 `/financial-analysis:lbo`、`/financial-analysis:dcf` 这类 Command。

请提醒用户用开场说明判断能力来源。`/financial-analysis:dcf` 正常开始时应说明：本次使用 Claude 金融套件中文版的 `/financial-analysis:dcf` 命令组织 DCF 流程，Wind MCP / Wind MCP Skill 仅作为数据源，不是使用 Wind 的 DCF Skill。

请注意表述：`/financial-analysis:dcf` 是斜杠命令 / Command，不要称为 `financial-analysis:dcf skill`。可以说它会调用本套件内部的 `dcf-model` Skill。区分 Wind 时，只说明“本次未触发 `/tmp/wind-skills/.../dcf-model/SKILL.md`”，不要在未核实 Wind Skill 内容时评价 Wind 的 DCF Skill 定位。

如果已经显示 `Skill(financial-analysis:dcf) Successfully loaded skill`，但开场没有说明能力来源，且第一步就去 `Web Search`，通常是旧会话或旧插件缓存仍在生效。请让用户在系统终端更新插件并重启 Claude Code。

对 A 股 DCF 验证，建议先做小范围测试：让 Claude Code “先用 Wind MCP 获取牧原股份核心财务和行情数据，展示数据源和缺口，暂时不要生成 Excel”。确认 Wind 数据通道正常后，再继续完整 DCF 模型。

## 第 5 步：向用户回报结果

请用简短中文说明：

1. Claude Code 是否可用；
2. 插件市场源是否添加成功；
3. 6 个推荐插件/Agent 是否安装成功；
4. 验证时应使用 `/financial-analysis:dcf 牧原食品` 等带命名空间的斜杠命令，不要用泛泛的自然语言 DCF 请求；
5. `/financial-analysis:dcf` 开始时应主动说明金融套件负责 DCF 流程、Wind 只负责数据源；
6. 是否需要重启 Claude Code 或重新开启会话；
7. 如果失败，下一步应处理什么问题。
