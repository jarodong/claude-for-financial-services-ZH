# GL Reconciler — Managed Agent 模板

## 概述

发现总账与子账之间的差异，追溯根因，生成异常报告供财务主管签批。与 [`gl-reconciler`](../../plugins/agent-plugins/gl-reconciler) Cowork 插件同源——本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export GL_MCP_URL=...           # 只读 GL MCP
export SUBLEDGER_MCP_URL=...    # 只读子账 MCP
../../scripts/deploy-managed-agent.sh gl-reconciler
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。用交易日期和资产类别列表启动会话；后续事件可以重新追溯单个差异。

## 安全与交接

此 Agent 读取交易对手/托管人报表——由外部方编写的文档，可能携带对抗性指令。模板的结构确保这些文档中的载荷无法到达 Shell、写入工具或公司系统：

| 层级 | 接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | 只读 GL + 子账 MCP |
| **`resolver`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`reader` 仅返回长度限制、schema 验证的 JSON（由 `scripts/validate.py` 验证）。`critic` 在编排器将集合交给 `resolver` 之前，独立对每个差异重新验证受信来源。`resolver` 将异常报告写入 `./out/`；它从不打开外部文件。

**交接：** 要将已验证差异输入月结，编排器在最终输出中发出 `handoff_request` 给 `month-end-closer`；`scripts/orchestrate.py`（或你的 Temporal/Airflow Worker）将其作为新的转向事件路由。白名单 + 载荷验证模式见脚本。

**不保证：** 以上任何操作都不会写入记录系统。账务调整需要在 Agent 外部获得人工审批。
