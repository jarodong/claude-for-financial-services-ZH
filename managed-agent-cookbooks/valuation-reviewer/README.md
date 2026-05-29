# Valuation Reviewer — Managed Agent 模板

## 概述

接收 GP 资料包、运行估值模板、暂存 LP 报告。与 [`valuation-reviewer`](../../plugins/agent-plugins/valuation-reviewer) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export PORTFOLIO_MCP_URL=...
../../scripts/deploy-managed-agent.sh valuation-reviewer
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

GP 提供的估值资料包为不受信来源。三级隔离：

| 层级 | 是否接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`package-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| `valuation-runner` / 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | portfolio（只读） |
| **`publisher`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`package-reader` 返回长度受限、经 schema 验证的 JSON。`publisher` 生成 `./out/lp-pack-<fund>.xlsx`。

**交接：** 如需将标记的被投企业送入 GL Reconciler，发出 `handoff_request` 给 `gl-reconciler`；`scripts/orchestrate.py` 路由。

**不保证：** LP 报告需要 IR 和 CCO 在本 Agent 之外签批。
