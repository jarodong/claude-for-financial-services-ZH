# Pitch Agent — Managed Agent 模板

## 概述

可比公司、先例交易、LBO → 品牌推介材料，端到端。与 [`pitch-agent`](../../plugins/agent-plugins/pitch-agent) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... DALOOPA_MCP_URL=...
../../scripts/deploy-managed-agent.sh pitch-agent
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

任务分解隔离 —— 与不受信输入关系较小（数据来自 CapIQ/Daloopa MCP），重点是并行性和工件隔离。恰好一个 Worker 持有 `Write`：

| 叶子节点 | 工具 | 连接器 |
|---|---|---|
| `researcher` | `Read`、`Grep` | CapIQ、Daloopa（只读） |
| `modeler` | `Read`、`Bash`（沙箱） | CapIQ、Daloopa（只读） |
| **`deck-writer`**（Write 持有者） | `Read`、`Write`、`Edit` | 无 |

工件通过 `pptx-author` / `xlsx-author` 落盘到 `./out/pitch-<target>.pptx` 和 `./out/model.xlsx`。

**交接：** 如需在论点变更后重建模型，编排器发出 `handoff_request` 给 `model-builder`；`scripts/orchestrate.py`（或你的工作流引擎）将其作为新转向事件路由。详见脚本中的白名单和载荷验证模式。
