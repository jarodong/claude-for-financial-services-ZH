# Month-End Closer — Managed Agent 模板

## 概述

应计、滚动结转、差异说明。与 [`month-end-closer`](../../plugins/agent-plugins/month-end-closer) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export GL_MCP_URL=...
../../scripts/deploy-managed-agent.sh month-end-closer
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

支持性发票和供应商对账单为不受信来源。三级隔离：

| 层级 | 是否接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`ledger-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| `rollforward` / 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | internal-gl（只读） |
| **`poster`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`poster` 生成 `./out/close-package-<entity>-<period>.xlsx`。分录草稿为暂存状态，不会过账到总账。

**交接：** 接收来自 `gl-reconciler` 的 `handoff_request` 事件，将已验证差异纳入结账说明。
