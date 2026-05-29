---
description: 生成加载项清单 XML——将你的云端配置烘焙进去
---

# 生成加载项清单

脚本获取规范清单并将你的配置作为 URL 查询参数附加。加载项在启动时读取它们。Outlook 使用单独的模板，因为 Microsoft 的 `MailApp` schema 与 Excel/Word/PowerPoint 共享的 `TaskPaneApp` schema 不同，所以要问他们部署哪些应用，然后为每个宿主生成一个文件。

| 宿主参数 | 应用 | 模板 |
|---|---|---|
| `office` | Excel、Word、PowerPoint | `pivot.claude.ai/manifest.xml` |
| `outlook` | Outlook（邮件 + 日历） | `pivot.claude.ai/manifest-outlook-3p.xml` |

## 按云端分类的键

只提示他们云端路径需要的键。不要问全部八个。

| 云端 | 键 |
|---|---|
| Vertex | `gcp_project_id` `gcp_region` `google_client_id` `google_client_secret` |
| Bedrock | `aws_role_arn` `aws_region` |
| Foundry | `azure_resource_name` `azure_api_key` |
| Gateway | `gateway_url` `gateway_token` `gateway_auth_header` `gateway_api_format` |
| Gateway（`gateway_api_format=vertex`） | 还需 `gcp_project_id` `gcp_region` |

Amazon Bedrock **目前不支持 `outlook` 宿主**；如果你传入 `aws_*` 键和 `outlook`，脚本会报错退出。

## Outlook — Microsoft Graph

Outlook 通过 Microsoft Graph 读取用户的邮箱和日历，这需要一次性的租户范围管理员授权，无论哪个云端提供模型服务。在部署前运行 [consent](consent.md#outlook--microsoft-graph-authorization)——否则每个用户首次打开时都会遇到"需要管理员批准"。

如果他们的策略禁止授权第三方应用，提示输入 `graph_client_id`（他们自己的单租户 Entra 应用的客户端 ID，具有 Mail.ReadWrite、Calendars.Read、People.Read、User.Read、offline_access 委托权限且已授予管理员授权）。否则不设置，加载项使用 Anthropic 的多租户应用。

## Entra SSO

`entra_sso=1` 使加载项在启动时获取 Entra ID Token。当你的部署需要用户的 Microsoft 身份时设置——Bedrock 将其用作 STS Web 身份，Bootstrap 端点将其用作 Bearer 认证，按用户属性（[update-user-attrs](update-user-attrs.md)）作为 `extn.*` 声明承载其中。

**管理员授权是前置条件。** 没有它，每个用户首次打开时都会看到 Microsoft 授权对话框。先运行 [consent](consent.md)，这样 `entra_sso=1` 对你的用户就是静默的。

如果你不需要 Entra——静态网关配置、使用 Google OAuth 的 Vertex——不设置。用户不会看到与 Microsoft 无关的设置的 Microsoft 提示。

**自带 Entra 应用。** 默认情况下，Token 作为 Anthropic 的多租户应用（`c2995f31-…`）请求，因此其 `aud` 声明是该 GUID。如果你的 Bootstrap 端点或 Token 交换服务要求 `aud` 匹配在*你的*租户中注册的应用，设置 `graph_client_id=<your-app-guid>`。在 Entra 中将应用注册为单租户**单页应用**，重定向 URI 为 `https://pivot.claude.ai/msal-redirect.html`。你在自己的应用上处理授权——[consent](consent.md) 仅涵盖默认应用。

**发送访问 Token 而非 ID Token。** 仅设置 `graph_client_id` 时，加载项仍向你的 Bootstrap 端点发送*ID Token*——`aud` 是你应用的 GUID，但没有 `scp` 声明。如果你的端点是验证 `aud` + `scp` 的标准 OAuth2 受保护资源，或是 RFC 8693 Token 交换服务，设置 `entra_scope=api://<your-app-guid>/<scope>`，加载项会改为请求该范围的*访问 Token*。它发送的 Bearer 携带 `aud` = 你 API 的 App ID URI 和 `scp` = 授予的范围。在 Entra 中，在你的应用注册上：**公开 API**（Application ID URI `api://<guid>`），添加一个范围如 `access_as_user`，并向同一应用授予委托权限，然后为租户授予管理员授权。在应用清单中，设置 `accessTokenAcceptedVersion: 2` 使签发的 Token 使用 v2.0 声明（`iss = login.microsoftonline.com/<tid>/v2.0`、`azp`、`preferred_username`）；不设置则获得 v1.0 Token，你的验证器可能会拒绝。`/.default`（请求所有已授权范围）也可以。

**多个范围。** `entra_scope` 接受逗号或空格分隔的列表——`entra_scope=api://<guid>/use_llm,api://<guid>/admin`。所有范围必须指向**同一资源**：一个访问 Token 只有一个 `aud`，所以 MSAL 无法签发跨越两个 API 的 Token（`api://torii/x,api://other/y` 会失败或静默只执行一个）。Bearer 的 `scp` 声明是空格连接的列表。如果你需要所有已授权范围，优先用 `/.default` 而非逐一枚举。

`entra_scope` 需要 `graph_client_id`——构建脚本强制*这对配对*但不强制范围字符串本身：任何非空值都被接受，Entra 在登录时验证语法（格式错误的范围表现为 `AADSTS` 错误，而非构建失败）。两个键都是清单专用的：加载项需要它们在读取扩展属性或调用 Bootstrap 端点*之前*初始化 NAA，所以都不能通过这些层传递。不设置 `entra_scope` 则发送 ID Token。

## Bootstrap 端点

`bootstrap_url` 指向你托管的 HTTPS 端点。启动时，加载项从中获取按用户的 JSON——Provider 键、`mcp_servers`、`skills`——响应覆盖该用户的清单值。URL 本身在获取前根据清单 + 属性进行[插值](bootstrap.md#模板插值)，因此一个端点可以通过查询参数分支。

参见 [bootstrap](bootstrap.md) 了解请求/响应契约、JWT 验证和处理器脚手架。

## MCP 服务器

`mcp_servers` 是加载项直接连接的客户托管 MCP 服务器的 JSON 数组。每个条目是 `{url, label, headers?, discover?}`——`headers` 存在表示静态认证；不存在触发 OAuth 发现。值通过 `{{gateway_url}}` 风格的模板插值其他配置键。

在此处设置适用于整个组织的一个列表；按用户列表属于 [bootstrap](bootstrap.md#mcp_servers)，那里也有完整 schema。值是 shell 参数内的 JSON——用单引号包裹：

```bash
mcp_servers='[{"url":"{{gateway_url}}/deepwiki/mcp","label":"DeepWiki","headers":{"Authorization":"Bearer {{gateway_token}}"}}]'
```

## 遥测

`otlp_endpoint` 将加载项的 OpenTelemetry Traces 路由到你运营的采集器。设置为采集器的基础 HTTPS URL——加载项附加 `/v1/traces` 并发送 OTLP/HTTP。不支持 gRPC（加载项运行在浏览器 WebView 中）。不设置则不配置自定义采集器。

`otlp_headers` 为该采集器提供认证头，使用与标准 `OTEL_EXPORTER_OTLP_HEADERS` 变量相同的 `key1=value1,key2=value2` 格式。在清单中对值进行 URL 编码。

`otlp_resource_attributes` 向每个 Span 的 OpenTelemetry Resource 添加属性，使用与标准 `OTEL_RESOURCE_ATTRIBUTES` 变量相同的 `key1=value1,key2=value2` 格式。当你的采集器需要特定资源属性进行路由或归属时使用（如 `team.name=platform,deployment.environment=prod`）。加载项已设置 `service.name`、`service.version` 和 `git.sha`；你在此提供的值在其上合并。

在此处设置适用于整个组织的一个采集器；按用户路由属于 [bootstrap](bootstrap.md#telemetry) 或扩展属性。

## 推理头

`inference_headers` 是加载项附加到发送到你的网关（`gateway_url`）的每个请求的额外 HTTP 头的 JSON 对象。用于你的网关期望的记账或成本分配标签——例如内部应用 ID——这样你就不需要在网关前面放一个头注入代理。仅在使用网关时适用；直连云端时忽略。

```bash
inference_headers='{"x-application-id":"app123"}'
```

加载项将值视为不透明。`Authorization`、`x-api-key`、`Content-Type`、`Host`、`Content-Length`、`User-Agent`、`Cookie` 以及任何 `anthropic-*` / `x-amz-*` / `x-goog-*` 头都是保留的，会被静默丢弃——它们承载加载项自身的认证和协议协商。

在此处设置适用于整个组织的一组头；按用户值属于 [bootstrap](bootstrap.md#inference_headers)。

## 自动连接

默认：当一个 Provider 的所有字段都设置时，用户跳过连接表单直接进入聊天。问：他们是否应该先看到表单（预填充，一次点击）？是 → `auto_connect=0`。

## 允许 Claude.ai 登录

当任何企业配置键存在时，用户进入企业连接屏幕，**返回** Claude.ai 登录的按钮被隐藏（`allow_1p=0`，默认）。设置 `allow_1p=1` 保留**返回**按钮。

## 禁用功能

`disabled_features` 是管理员要锁定的功能 Slug 的逗号分隔列表。Slug 使用 `<domain>.<action>` 形式。当前已强制执行：

| Slug | 效果 |
|---|---|
| `skills.authoring` | 阻止创建、编辑和上传技能（create/update 工具、`/skillify`、`.skill` 上传 + 拖放、技能编辑 UI）。运行管理员配置的技能不受影响。 |

```bash
disabled_features='skills.authoring'
```

未知 Slug 被忽略（前向兼容）。在此处设置适用于整个组织的一个策略；按用户策略属于 [bootstrap](bootstrap.md#disabled_features)（JSON 数组）或扩展属性（逗号分隔）。

## 版本

M365 管理中心按 `<Id>` + `<Version>` 缓存——用相同版本重新上传会被静默忽略。脚本写入 `manifest.xml` 后，问这是否替换现有部署；如果是，编辑 `<Version>` 递增第四段超过上次部署的值。首次部署可以保留模板的版本不变。

## 运行

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/build-manifest.mjs" office manifest.xml \
  gcp_project_id=<value> \
  gcp_region=<value> \
  auto_connect=0 \
  ...

# 如果他们还部署 Outlook：
node "${CLAUDE_PLUGIN_ROOT}/scripts/build-manifest.mjs" outlook manifest-outlook.xml \
  <same provider keys as above> \
  graph_client_id=<value>   # 仅在不通过授权 URL 使用 Anthropic 应用时
```

脚本验证键名（未知键硬失败）并对值进行形状提示（警告但不阻止——他们的基础设施可能不同）。

## 验证

```bash
npx --yes office-addin-manifest validate manifest.xml
```

如果验证通过但 M365 管理中心仍拒绝或忽略上传，匹配下方的症状。直接编辑 `manifest.xml`，然后重新验证。

| 症状 | 修复 |
|---|---|
| "An add-in with this ID already exists" | 将 `<Id>` 内的文本替换为新的 UUID。模板携带市场安装的 ID。 |
| 重新上传被接受但没有变化 | M365 按 ID + 版本缓存。编辑 `<Version>` 为更高的第四段（如 `1.0.0.9` → `1.0.0.10`）并重新验证。 |
| 只要 Excel（不要 PowerPoint） | 移除 `Presentation` 的 `<Host>` 元素。**两个并行列表：** 顶层 `<Hosts>` 使用 `Name="Presentation"`，`<VersionOverrides>` 下的使用 `xsi:type="Presentation"`——两者都必须移除，否则清单不一致。`xsi:type` 块是多行的，删除整个 `<Host xsi:type="Presentation">...</Host>`。 |
| 只要 Excel/PPT，不要 Outlook | 不需要移除——Outlook 是单独的文件。不生成即可。 |
