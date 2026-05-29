# 金融服务 Managed Agent 模板

本仓库中的每个 Agent 都以**两种方式**发布：作为分析师今天就能安装的 Cowork 插件（见仓库根目录的垂直目录），以及作为你的平台团队在自己的工作流引擎后面部署的 Claude Managed Agent 模板。**同一个 Agent，同一个 Skill——选择你的界面。** 下面的每个目录都是一个部署清单，引用来自匹配插件的规范系统提示和 Skill，因此只有一个真相来源。

运行 `../scripts/deploy-managed-agent.sh <slug>` 上传 Skill、创建叶子 Worker 并用解析后的配置 `POST /v1/agents`。每个模板都附带 [`steering-examples.json`](./pitch-agent/steering-examples.json) 和涵盖安全等级和交接的按 Agent README。

| Agent | 垂直插件 | Cowork 磁贴 | CMA 转向事件 | 叶子 Worker |
|---|---|---|---|---|
| [`pitch-agent`](./pitch-agent/) | investment-banking | 可比公司、先例、LBO → 品牌 Pitch Deck | `Build pitch book: <target> / <acquirer>, thesis: <text>` | researcher · modeler · **deck-writer** |
| [`market-researcher`](./market-researcher/) | equity-research | 行业或主题 → 概览、竞争格局、同业可比、想法候选 | `Primer: <sector or theme>, angle: <text>` | sector-reader · comps-spreader · **note-writer** |
| [`earnings-reviewer`](./earnings-reviewer/) | equity-research | 财报电话 + 文件 → 模型更新 → 研报草稿 | `Process earnings: <ticker> <period>` | transcript-reader · model-updater · **note-writer** |
| [`meeting-prep-agent`](./meeting-prep-agent/) | wealth-management | 每次客户会议前的简报包 | `Briefing pack for <client-id>, meeting <event-id>` | profiler · news-reader · **pack-writer** |
| [`model-builder`](./model-builder/) | financial-analysis | DCF、LBO、三表、可比公司——作为文件 | `Build <dcf\|lbo\|3-stmt> for <ticker>, assumptions: {...}` | data-puller · **builder** · auditor |
| [`gl-reconciler`](./gl-reconciler/) | financial-analysis | 发现差异、追溯根因、路由签批 | `Reconcile GL vs subledger, trade date <D>, classes: <list>` | reader · critic · **resolver** |
| [`kyc-screener`](./kyc-screener/) | financial-analysis | 解析开户文件、运行规则、标记缺口 | `Screen onboarding packet <id>` | doc-reader · rules-engine · **escalator** |
| [`valuation-reviewer`](./valuation-reviewer/) | private-equity | 接收 GP 包、运行估值、暂存 LP 报告 | `Review portco valuations for fund <X> as of <date>` | package-reader · valuation-runner · **publisher** |
| [`month-end-closer`](./month-end-closer/) | financial-analysis | 计提、滚调、差异说明 | `Close <entity> for period <YYYY-MM>` | ledger-reader · rollforward · **poster** |
| [`statement-auditor`](./statement-auditor/) | private-equity | 分配前审计 LP 报表 | `Tie out statement batch <id> against <fund> NAV pack` | statement-reader · reconciler · **flagger** |

**加粗**的叶子 = 唯一拥有 `Write` 的 Worker。

## 清单 vs API

`agent.yaml` 文件使用真实的 `POST /v1/agents` 字段名，附带一些部署脚本解析的便利写法：

| 清单约定 | 解析为 |
|---|---|
| `system: {file: ../../plugins/agent-plugins/<slug>/agents/<slug>.md, append: "..."}` | `system: "<内联内容 + append>"` |
| `system: {text: "..."}` | `system: "<text>"` |
| `skills: [{from_plugin: ../../plugins/agent-plugins/<slug>}]` | 上传该目录下每个 `skills/*` → `[{type: custom, skill_id: ...}, ...]` |
| `skills: [{path: ../../...}]` | `skills: [{type: custom, skill_id: <uploaded-id>}]` |
| `callable_agents: [{manifest: ./subagents/x.yaml}]` | `callable_agents: [{type: agent, id: <created-id>, version: latest}]` |

> **研究预览：** `callable_agents`（多 Agent 委派）支持**一级委派**。编排器可以调用 Worker；Worker 不能调用更深层的子 Agent。

## 跨 Agent 交接

命名 Agent 从不直接互相调用。当一个 Agent 需要另一个时，它在输出中发出 `handoff_request`；[`../scripts/orchestrate.py`](../scripts/orchestrate.py)（或你的 Temporal/Airflow/Guidewire 事件总线）将其作为新的转向事件路由到目标会话。参考脚本硬编码白名单目标并进行 schema 验证负载——参见其头部注释了解威胁模型。
