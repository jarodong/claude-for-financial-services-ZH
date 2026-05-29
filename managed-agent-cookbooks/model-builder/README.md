# Model Builder — Managed Agent 模板

## 概述

DCF、LBO、三表模型、可比分析 —— 以文件形式构建。与 [`model-builder`](../../plugins/agent-plugins/model-builder) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... DALOOPA_MCP_URL=...
../../scripts/deploy-managed-agent.sh model-builder
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

任务分解隔离 —— 输入来自受信 MCP，因此隔离的重点是工件隔离和重新验证。恰好一个 Worker 持有 `Write`：

| 叶子节点 | 工具 | 连接器 |
|---|---|---|
| `data-puller` | `Read`、`Grep` | CapIQ、Daloopa（只读） |
| **`builder`**（Write 持有者） | `Read`、`Write`、`Edit`、`Bash`（沙箱） | 无 |
| `auditor` | `Read`、`Grep` | 无 |

`auditor` 在 `builder` 写入 `./out/model.xlsx` 后重新检查勾稽和余额。

**交接：** 当从 `earnings-reviewer` 或 `pitch-agent` 调用时，调用方的 `handoff_request` 由 `scripts/orchestrate.py` 路由至此。
