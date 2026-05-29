# Earnings Reviewer — Managed Agent 模板

## 概述

财报电话 + 文件 → 模型更新 → 研报草稿。与 [`earnings-reviewer`](../../plugins/agent-plugins/earnings-reviewer) Cowork 插件同源——本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export FACTSET_MCP_URL=... DALOOPA_MCP_URL=...
../../scripts/deploy-managed-agent.sh earnings-reviewer
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。从编排层对覆盖列表进行扇出——每个 Ticker 一个会话。

## 安全与交接

财报电话和新闻稿是不受信的。三层隔离：

| 层级 | 接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`transcript-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| `model-updater` / 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | FactSet、Daloopa（只读） |
| **`note-writer`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`transcript-reader` 返回长度限制、schema 验证的 JSON。`note-writer` 生成 `./out/note-<ticker>.docx` 和更新后的模型 `./out/model-<ticker>.xlsx`。

**交接：** 如需在财报驱动的论点变更后重建 DCF，发出 `handoff_request` 给 `model-builder`；`scripts/orchestrate.py` 将其作为新的转向事件路由。
