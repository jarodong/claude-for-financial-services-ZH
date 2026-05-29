# KYC Screener — Managed Agent 模板

## 概述

解析开户文档、运行规则引擎、筛查制裁/PEP、标记缺失项。与 [`kyc-screener`](../../plugins/agent-plugins/kyc-screener) Cowork 插件同源 —— 本目录是 `POST /v1/agents` 的 Managed Agent Cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export SCREENING_MCP_URL=...
../../scripts/deploy-managed-agent.sh kyc-screener
```

## 转向事件

参见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

开户文档为不受信来源。三级隔离：

| 层级 | 是否接触不受信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`doc-reader`** | **是** | 仅 `Read`、`Grep` | 无 |
| `rules-engine` / 编排器 | 否 | `Read`、`Grep`、`Glob`、`Agent` | screening（只读） |
| **`escalator`**（Write 持有者） | 否 | `Read`、`Write`、`Edit` | 无 |

`doc-reader` 返回长度受限、经 schema 验证的 JSON。`escalator` 生成 `./out/escalation-<packet>.xlsx`。

**不保证：** 本 Agent 推荐风险评级；最终由合规官决定。
