---
description: 构建 Bootstrap 端点——按用户配置 MCP 服务器、技能和动态配置
---

# Bootstrap 端点

你托管一个 HTTPS GET 处理器。加载项在启动时用用户的 Entra Token 调用它，你返回用户级 JSON，响应会覆盖该用户的清单文件和扩展属性。这是你推送结构化配置的方式——`mcp_servers`、`skills`——扁平字符串属性无法承载的内容。

## 先确认场景

在走读规范之前，先弄清楚对方处于哪种模式：

- **只想了解？** 从下面的章节回答。常见问题：响应结构是什么、`{{...}}` 如何工作、为什么 CORS 报错。
- **要构建？** 问：新建处理器还是编辑现有的？Lambda、Cloud Function、Express、Python 还是其他？然后跳到[脚手架](#构建处理器脚手架)——中间的章节是你编码所依据的契约。

## 与扩展属性的对比

两者都提供用户级配置。根据你承载的内容选择。

| | [扩展属性](update-user-attrs.md) | Bootstrap 端点 |
|---|---|---|
| 你写入 | 每个用户 `az rest PATCH` | 一个 HTTPS 服务 |
| 承载 | 扁平字符串，≤256 字符 | 任意 JSON——数组、嵌套、base64 |
| 适用场景 | Token 轮换、区域覆盖 | `mcp_servers`、`skills` 等结构化内容 |
| 刷新 | Token 缓存，约 1 小时延迟 | `bootstrap_expires_at`，你控制 |
| 认证 | Entra Token 声明（被动） | 你验证 JWT（主动） |

如果你只需要按用户替换 `gateway_token`，扩展属性更省事。一旦你想让一个团队用 Linear MCP 服务器、另一个用 Jira，就需要用这里了。

## 模板插值

任何字符串值都可以包含 `{{key}}`。加载项会根据**合并配置链**进行替换——清单参数 → 扩展属性 → 本响应，每层覆盖上一层。你不需要回显值让模板能看到它；如果 `gateway_token` 已在清单或属性中，`{{gateway_token}}` 会自动解析。

两个阶段，因为请求必须在响应存在之前发生：

1. **`bootstrap_url` 本身**仅根据清单 + 属性解析。因此清单可以携带 `bootstrap_url=https://config.internal/bootstrap?project={{gcp_project_id}}`，你运行一个端点通过查询参数分支，而不是为每个团队在属性中写入不同 URL。
2. **响应字段**根据完整合并解析——清单 + 属性 + 本响应刚返回的内容。`mcp_servers` 条目可以引用同一 JSON 中三行前的 `gateway_token`。

未解析的 `{{key}}`（拼写错误、键从未在任何地方设置）会原样保留在字符串中——无报错、无空替换。如果 MCP 服务器无法连接，检查加载项实际构造的 URL。

## CORS——每个 URL 都需要

加载项是浏览器。每个 fetch——`bootstrap_url`、每个 `mcp_servers[].url`、每个 `skills[].url`——都从 Office 任务窗格内部以浏览器方式发起。如果响应没有 `Access-Control-Allow-Origin: https://pivot.claude.ai`，浏览器会在加载项看到一个字节之前就拦截它。服务器返回 200，加载项什么也收不到，日志中也没有任何信息告诉你原因。这是最常见的"不工作"原因。

| URL | CORS 配置位置 |
|---|---|
| `bootstrap_url` | 你的处理器响应头。在 API Gateway / Cloud Functions 后面时，还需配置 `OPTIONS` 预检——浏览器在任何带自定义头的请求之前会先发预检。见下方推荐的预检响应。 |
| `mcp_servers[].url` | MCP 服务器本身。公开的（Linear、Atlassian）已允许。内部的几乎肯定没有，需要你添加。 |
| `skills[].url` | **是存储桶，不是 URL。** 预签名 URL 对请求做认证——不授予 CORS。S3 需要存储桶 CORS 配置，GCS 需要 `gsutil cors set`，Azure 需要 Blob 服务 CORS 规则。 |
| `otlp_endpoint` | 你的 OTEL 采集器的 HTTP 接收器。大多数采集器默认只允许同源——在 OTLP/HTTP 接收器上设置 `cors.allowed_origins`。 |

`bootstrap_url` 的推荐预检响应：

```
Access-Control-Allow-Origin:  https://pivot.claude.ai
Access-Control-Allow-Methods: GET
Access-Control-Allow-Headers: Authorization, X-Claude-User-Agent, *
```

允许 `*` 作为请求头是安全的——安全性来自 Entra Token 而非头过滤——并且如果加载项将来添加头也能保持预检工作。`Allow-Origin` 保持固定为 `https://pivot.claude.ai`。

预签名 URL 的问题最严重，因为 `curl` 能工作（curl 忽略 CORS）、签名有效、对象存在，但技能就是不加载。设置一次存储桶 CORS：

```json
// S3 — aws s3api put-bucket-cors --bucket <name> --cors-configuration file://cors.json
{ "CORSRules": [{ "AllowedOrigins": ["https://pivot.claude.ai"], "AllowedMethods": ["GET"], "AllowedHeaders": ["*"] }] }
```

```bash
# GCS — gsutil cors set cors.json gs://<bucket>
[{"origin": ["https://pivot.claude.ai"], "method": ["GET"], "responseHeader": ["*"]}]
```

```bash
# Azure — az storage cors add --services b --methods GET --origins https://pivot.claude.ai --allowed-headers '*' --account-name <name>
```

调试 CORS 失败时：在任务窗格中打开浏览器开发者工具（Windows 右键 → 检查，Mac 通过 Safari 的开发菜单附加），在网络标签页中查找请求。CORS 拦截显示为无响应体的失败请求，控制台错误会指明来源。

## 请求

```
GET <bootstrap_url>                            # 插值后
Authorization: Bearer <entra_token>            # 仅在清单中 entra_sso=1 时
X-Claude-User-Agent: claude-<app>/<version>    # 始终发送
```

`X-Claude-User-Agent` 标识加载项运行在哪个 Office 宿主中。`<app>` 是 `word`、`excel` 或 `powerpoint` 之一；`<version>` 是加载项构建版本（如 `claude-excel/1.4.2`）。用它来按 Office 产品返回不同的技能或 MCP 服务器，或将加载项限制为特定宿主。

没有 `entra_sso=1` 时没有 Authorization 头——从加载项角度看是匿名请求。如果端点在网络隔离、mTLS 或加载项看不到的其他认证层后面，这没问题。

有 `entra_sso=1` 时，在信任前验证 JWT：

| 声明 | 检查 |
|---|---|
| `aud` | `c2995f31-11e7-4882-b7a7-ef9def0a0266`——加载项的默认应用 ID，或你在[清单](manifest.md#entra-sso)中设置的自己的应用 GUID。其他值意味着 Token 不是为此铸造的。 |
| `iss` | `https://login.microsoftonline.com/<YOUR_TENANT_ID>/v2.0`——你的租户。拒绝其他租户。 |
| `exp` | 未过期。库会处理这个；不要手写。 |
| `oid` | 用户的稳定对象 ID。这是你的查找键——邮箱（`upn`/`preferred_username`）可能变化，`oid` 不会。 |

如果在[清单](manifest.md#entra-sso)中设置了 `entra_scope`，Bearer 是**访问 Token** 而非 ID Token。验证 `aud` = 你的 API 的 Application ID URI（`api://<guid>`，不是客户端 GUID）并检查 `scp` 包含你定义的范围——`entra_scope` 命名多个范围时 `scp` 是空格分隔的列表。`iss`、`exp`、`oid` 和签名验证相同。

签名验证需要 Microsoft 的 JWKS（`https://login.microsoftonline.com/<TENANT_ID>/discovery/v2.0/keys`）。使用库——`jose`（Node）、`PyJWT` + `cryptography`（Python）、`Microsoft.IdentityModel.Tokens`（.NET）。手写 JWT 验证是安全漏洞的温床。

## 响应

`200 OK`，`Content-Type: application/json`，CORS 头见[上方](#cors每个-url-都需要)。

响应体是扁平对象。每个字段都是可选的——只返回对此用户不同的内容。未知键会被忽略，因此你可以添加当前加载项版本尚未读取的字段，等它发布时就会生效。

### Provider 键

[清单](manifest.md#按云端分类的键)表中的任何云端配置键——`gateway_url`、`gateway_token`、`aws_role_arn`、`gcp_region` 等。相同名称、相同含义，只是用户级。

如果返回 `gateway_api_format: "vertex"`，还需返回 `gcp_project_id` 和 `gcp_region`（或在更低层级设置）——它们是加载项构造的 Vertex `:rawPredict` URL 中的路径段。`"bedrock"` 不需要额外内容。

### 遥测

```json
"otlp_endpoint": "https://otel-collector.your-domain.com",
"otlp_headers": "Authorization=Bearer {{gateway_token}}",
"otlp_resource_attributes": "team.name={{team}},deployment.environment=prod"
```

`otlp_endpoint` 是你运营的 OpenTelemetry 采集器的基础 HTTPS URL；加载项会附加 `/v1/traces` 并发送 OTLP/HTTP。`otlp_headers` 使用标准 `key1=value1,key2=value2` 格式，像其他值一样插值。`otlp_resource_attributes` 使用相同格式（匹配标准 `OTEL_RESOURCE_ATTRIBUTES` 变量），合并到每个 Span 的 OpenTelemetry Resource 中——当你的采集器需要特定资源属性进行路由或归属时使用。采集器必须允许来自加载项来源的 CORS——见[上方](#cors每个-url-都需要)。

### `inference_headers`

```json
"inference_headers": { "x-application-id": "app123" }
```

附加到加载项发送到你的网关（`gateway_url`）的每个请求的额外 HTTP 头——通常是网关用于成本分配的记账标签。仅适用于网关部署；直连云端时忽略。加载项将它们视为不透明透传；`Authorization`、`x-api-key`、`Content-Type`、`Host`、`Content-Length`、`User-Agent`、`Cookie` 以及任何 `anthropic-*` / `x-amz-*` / `x-goog-*` 头都是保留的，会被静默丢弃。

### `mcp_servers`

此用户连接的 MCP 服务器数组。

```json
"mcp_servers": [
  { "url": "https://mcp.linear.app/sse", "label": "Linear" },
  {
    "url": "https://internal.yourcompany.com/mcp/risk",
    "label": "Risk Dashboard",
    "headers": { "Authorization": "Bearer {{gateway_token}}" }
  }
]
```

| 字段 | |
|---|---|
| `url` | MCP 服务器端点。支持插值。 |
| `label` | 加载项 UI 中的显示名称。 |
| `headers` | 可选。发送到该服务器的每个请求都携带。值支持插值——这是你传递用户级 Token 而端点永远不会看到它的方式。 |

### `skills`

此用户加载的技能数组。每个以内联 base64 或从 URL 获取——设置其中之一。

```json
"skills": [
  {
    "name": "deal-memo",
    "description": "从条款清单起草交易备忘录",
    "url": "https://yourbucket.s3.amazonaws.com/skills/deal-memo.zip?X-Amz-..."
  },
  {
    "name": "compliance-check",
    "content": "IyBDb21wbGlhbmNlIGNoZWNrCgpSZXZpZXcgdGhlIGRvY3VtZW50IGZvci4uLg=="
  }
]
```

| 字段 | |
|---|---|
| `name` | 技能标识符。支持插值。 |
| `description` | 可选。显示在技能选择器中。 |
| `content` | Base64 字节。可以是 zip（包含 `SKILL.md` + 资源的完整技能包）或原始 `SKILL.md` 文本——加载项在解码时自动判断。 |
| `url` | 预签名 URL（S3、GCS、Azure SAS）。裸 GET，不添加认证头——将认证烘焙到签名中。响应体与 `content` 相同方式判断。支持插值。 |

内联 `content` 对小型纯文本技能最简单。当你要发布带图片的 zip 或 base64 开始膨胀响应时使用 `url`。

### `disabled_features`

要为此用户锁定的功能 Slug JSON 数组。与[清单键](manifest.md#disabled-features)相同的词汇——bootstrap 是用户级层。

```json
"disabled_features": ["skills.authoring"]
```

### `bootstrap_expires_at`

此配置过期的纪元时间戳（秒或毫秒——自动检测）。加载项会在过期前重新获取。省略则配置在任务窗格重载前一直有效。

当你下发短期 Token 时设置此项。不要作为保活设置——如果响应中没有过期内容，重新获取是浪费。

## 构建处理器脚手架

可运行的 Python/FastAPI 参考实现（含 `skills` 和 `mcp_servers` 的 RBAC）在 [`examples/python-bootstrap/`](../examples/python-bootstrap/)——如果他们想要可复制的代码，指向那里。

当他们要你构建时，为他们编写。上面的契约就是你编码所依据的规范。这些要正确：

**JWT 验证是安全边界。** 根据 Microsoft 的 JWKS 验证签名，精确检查 `aud` 和 `iss`，拉取 `oid` 用于用户查找。跳过这一步而信任未验证 Token 中的 `preferred_username` 的处理器，就是一个多了几步的开放端点。

**你返回的每个 URL 都需要 CORS，** 不只是处理器——见 [CORS 章节](#cors每个-url-需要)。很容易发布一个返回无 CORS 配置的存储桶中预签名技能 URL 的处理器，然后技能永远加载不了。

**用户查找是他们的业务逻辑。** 在实际工作所在位置留下清晰的 `// TODO: 根据 oid 查找配置`——DynamoDB、Postgres、YAML 文件，无论他们有什么。不要猜测；问他们的数据源是什么。

**返回稀疏内容。** 只返回与清单默认值不同的键。空 `{}` 是有效响应——表示"此用户使用组织级配置。"

写之前先问：Lambda + API Gateway、Cloud Function、纯 Express 还是其他？用户级配置存放在哪——内联在处理器中（试点阶段可以），还是从存储读取？
