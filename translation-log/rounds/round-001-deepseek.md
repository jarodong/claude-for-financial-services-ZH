# Round 001 — 译文 B（DeepSeek）

> 原文：anthropics/financial-services/blob/main/CLAUDE.md
> 翻译员：DeepSeek TUI
> 日期：2026-05-19
> 等级：A 类（双译 + 裁判 + 定稿）

---

# 金融服务（Financial Services）插件

面向金融服务的 Cowork 插件和 Claude Managed Agent 模板。每个命名 Agent 从同一源文件以两种方式发布。

## 仓库（Repository）结构

```
├── plugins/
│   ├── agent-plugins/               #   命名 Agent —— 每个一个自包含插件
│   │   └── <slug>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── agents/<slug>.md     #   ← 标准 System Prompt（一份源，两种包装）
│   │       └── skills/              #   ← 打包副本，从 vertical-plugins/ 同步
│   ├── vertical-plugins/            #   FSI（金融服务行业）垂类 —— Skill 源、命令、MCP
│   │   └── <vertical>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── commands/
│   │       ├── skills/
│   │       └── .mcp.json
│   └── partner-built/               #   合作伙伴插件（LSEG、S&P Global）
├── managed-agent-cookbooks/         # CMA Cookbook（每个命名 Agent 一个目录）
│   └── <slug>/
│       ├── agent.yaml               #   system + skills → ../../plugins/agent-plugins/<slug>/...
│       ├── subagents/*.yaml         #   一级子工作器（depth-1 leaf workers）
│       ├── steering-examples.json
│       └── README.md                #   安全等级（security tier）+ 交接说明
├── claude-for-msft-365-install/     # Microsoft 365 插件的管理工具（独立于 FSI 插件）
└── scripts/                         # deploy-managed-agent.sh、check.py、validate.py、orchestrate.py、sync-agent-skills.py
```

提交前运行 `python3 scripts/check.py` —— 它会对每个 manifest 做 lint 检查，验证所有 `system.file` / `skills.path` / `callable_agents.manifest` 引用均可解析，并在任何 `agent-plugins/<slug>/skills/` 副本与其 `vertical-plugins/` 源发生偏移时报错。**请在 `vertical-plugins/` 中编辑 Skill**，然后运行 `python3 scripts/sync-agent-skills.py` 将其同步传播到 Agent 捆绑包中。

`check.py` 还会自行安装一个 `pre-commit` hook（通过 `git config core.hooksPath .githooks` —— 无需 Husky/Node）。该 hook 会对任何插件的 `.claude-plugin/plugin.json` 中的 `version` 做补丁号递增（patch-bump），使分支恰好比 `main` 领先一个补丁版本（仅递增一次，非每次提交递增 —— 插件的 `version` 控制着已安装用户的更新推送）。`version-bump` GitHub Action 作为兜底机制在 PR（Pull Request，拉取请求）上强制执行相同规则。可通过 `git commit --no-verify` 跳过单次提交；版本递增逻辑位于 `scripts/version_bump.py`。

## 关键文件

- `marketplace.json`：Marketplace manifest —— 注册所有插件及其源路径
- `plugin.json`：Plugin 元数据 —— 名称、描述、版本和组件发现设置
- `commands/*.md`：Slash Command，通过 `/plugin:command-name` 调用
- `skills/*/SKILL.md`：针对特定任务的详细知识和 Workflow
- `*.local.md`：用户特定配置（已 gitignore）
- `mcp-categories.json`：跨插件共享的 MCP（Model Context Protocol，模型上下文协议）类别规范定义

## 开发 Workflow

1. 直接编辑 Markdown 文件 —— 修改即时生效
2. 使用 `/plugin:command-name` 语法测试命令
3. Skill 在满足触发条件时自动调用
