# Meeting Prep Agent — Managed Agent 模板

## 概述

每次客户会议前的简报材料包。与 [`meeting-prep-agent`](../../plugins/agent-plugins/meeting-prep-agent) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CRM_MCP_URL=... CAPIQ_MCP_URL=...
../../scripts/deploy-managed-agent.sh meeting-prep-agent
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。通常由工作流引擎从日历事件触发。

## 安全与交接

客户提供的文档和收到的邮件为不受信来源。三级隔离：

| 层级 | 是否接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| `profiler` | 否 | `Read`、`Grep` | CRM、CapIQ（只读） |
| **`news-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| **`pack-writer`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`pack-writer` 生成 `./out/briefing-<client>.pptx`；从不直接打开客户提供的内容。

**不保证：** 本材料包供顾问使用，非供客户使用。不会直接发送给客户。
