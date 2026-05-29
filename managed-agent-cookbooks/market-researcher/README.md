# Market Researcher — Managed Agent 模板

## 概述

行业或主题 → 行业概览 → 竞争格局 → 可比公司 → 想法候选清单 → 研究简报。与 [`market-researcher`](../../plugins/agent-plugins/market-researcher) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... FACTSET_MCP_URL=...
../../scripts/deploy-managed-agent.sh market-researcher
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。从研究队列事件启动，或在覆盖图谱上扇出。

## 安全与交接

第三方报告和发行人材料为不受信来源。三级隔离：

| 层级 | 是否接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`sector-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| `comps-spreader` / 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | CapIQ、FactSet（只读） |
| **`note-writer`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`sector-reader` 返回长度受限、经 schema 验证的 JSON。`note-writer` 生成 `./out/primer-<sector>.docx`（如需幻灯片则同时生成 `.pptx`）。

**交接：** 如需对候选清单中出现的单个名称建模，发出 `handoff_request` 给 `model-builder`；`scripts/orchestrate.py` 将其作为新转向事件路由。
