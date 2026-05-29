# Statement Auditor — Managed Agent 模板

## 概述

在分发前审计已生成的 LP 报表。与 [`statement-auditor`](../../plugins/agent-plugins/statement-auditor) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export NAV_MCP_URL=...
../../scripts/deploy-managed-agent.sh statement-auditor
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

已生成的报表视为不受信（上游系统不在范围内）。三级隔离：

| 层级 | 是否接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`statement-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| `reconciler` / 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | nav（只读） |
| **`flagger`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`flagger` 生成 `./out/signoff-<batch>.xlsx`。

**不保证：** 本 Agent 推荐通过/暂挂；IR 在人工签批后分发。
