# 金融套件插件

Cowork 插件和 Claude Managed Agent 模板，用于金融服务。每个命名 Agent 从同一源以两种方式发布。

## 仓库结构

```
├── plugins/
│   ├── agent-plugins/               #   命名 Agent —— 每个一个自包含插件
│   │   └── <slug>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── agents/<slug>.md     #   ← 规范 System Prompt（单一来源，两种包装）
│   │       └── skills/              #   ← 打包副本，从 vertical-plugins/ 同步
│   ├── vertical-plugins/            #   金融垂直领域 —— Skill 源、Command、MCP
│   │   └── <vertical>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── commands/
│   │       ├── skills/
│   │       └── .mcp.json
│   └── partner-built/               #   合作伙伴插件（LSEG、S&P Global）
├── managed-agent-cookbooks/         #   Managed Agent 蓝图（每个命名 Agent 一个目录）
│   └── <slug>/
│       ├── agent.yaml               #   system + skills → ../../plugins/agent-plugins/<slug>/...
│       ├── subagents/*.yaml         #   一层 leaf worker
│       ├── steering-examples.json
│       └── README.md                #   安全等级 + 交接说明
├── claude-for-msft-365-install/     #   管理员工具，用于部署 Claude Microsoft 365 加载项（与 FSI 插件分开）
└── scripts/                         #   deploy-managed-agent.sh, check.py, validate.py, orchestrate.py, sync-agent-skills.py
```

提交前运行 `python3 scripts/check.py` —— 它会检查每个清单、验证所有 `system.file` / `skills.path` / `callable_agents.manifest` 引用可解析，并在 `agent-plugins/<slug>/skills/` 副本与 `vertical-plugins/` 源不同步时报错。**在 `vertical-plugins/` 中编辑 Skill**，然后运行 `python3 scripts/sync-agent-skills.py` 传播到 Agent 包中。

`check.py` 还会自安装 `pre-commit` hook（`git config core.hooksPath .githooks` —— 无需 Husky/Node）。该 hook 会 patch-bump 任何插件的 `.claude-plugin/plugin.json` `version`，使分支恰好比 `main` 多一个 patch 版本（每个插件只 bump 一次，不是每次提交——插件的 `version` 控制已安装用户的更新推送）。`version-bump` GitHub Action 在 PR 上强制执行相同规则作为后备。用 `git commit --no-verify` 跳过单次提交；bump 逻辑在 `scripts/version_bump.py` 中。

## 关键文件

- `marketplace.json`：市场清单——注册所有插件及其源路径
- `plugin.json`：插件元数据——名称、描述、版本和组件发现设置
- `commands/*.md`：以 `/plugin:command-name` 调用的 Slash Command
- `skills/*/SKILL.md`：特定任务的详细知识和工作流
- `*.local.md`：用户特定配置（gitignore）
- `mcp-categories.json`：跨插件共享的 MCP 类别定义

## 开发工作流

1. 直接编辑 Markdown 文件——更改立即生效
2. 用 `/plugin:command-name` 语法测试 Command
3. Skill 在触发条件匹配时自动调用
