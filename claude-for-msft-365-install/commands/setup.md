---
description: 设置向导——配置 Vertex/Bedrock/Foundry/网关、管理员授权、生成清单
---

# Claude in Office — 直连云端设置

你正在引导企业管理员配置 Claude Office 加载项，使其调用他们自己的云端而非 Anthropic 的 API。输出是通过 M365 管理中心部署的自定义 `manifest.xml`。

**首先：** 设置日志位于 `~/Desktop/claude-for-msft-365-install-setup.md`（根据他们的平台解析 `~`）。如果存在，先读取——你可能是在恢复之前的运行，可以跳过已完成的步骤。开始新的 `## Run — <timestamp>` 章节，边做边追加每个命令及其捕获的输出（ID、URL）。

**检查 Node.js** — 步骤 4 和 6 需要调用 `node` 和 `npx`。运行 `node --version`。如果缺失，**先询问再安装**——是他们的机器。如果同意，`brew install node`（Mac）/ `winget install OpenJS.NodeJS`（Win）/ 他们包管理器对应的命令。如果拒绝，到此为止。

**从管理员处获取值**（ID、URL、从控制台粘贴回来的密钥）——不要使用 AskUserQuestion。那是选择器；他们拿着的是字符串。直接说"准备好后粘贴客户端 ID"，从他们的下一条消息读取。仅在实际分支点（网关 vs Vertex、按用户 vs 组织范围）使用 AskUserQuestion。

## 步骤 1 — 加载项如何连接到 Claude？

先问这个，因为这是管理员容易搞错的：**你是否已经在运行 LLM 网关（LiteLLM、Portkey、Kong 等）？**

- **是 → `gateway`。** 即使网关底层路由到 Vertex 或 Bedrock——加载项与*你的网关*通信，不与 Google 或 AWS 通信。你只需要网关 URL。
- **否 → `vertex` 或 `bedrock`。** 加载项直接向云提供商认证。选择你的基础设施所在。

| 路径 | 含义 | 配置 | 清单键 |
|---|---|---|---|
| `gateway` | 加载项 → 你的网关 → （任意） | 无 | `gateway_url`（如果不是 `/v1/messages` 则加 `gateway_api_format`） |
| `vertex` | 加载项 → Google Vertex AI，直接 | Google OAuth 客户端 | `gcp_project_id`、`gcp_region`、`google_client_id`、`google_client_secret` |
| `bedrock` | 加载项 → AWS Bedrock，直接 | IAM OIDC 提供商 + 角色 | `aws_role_arn`、`aws_region` |
| `foundry` | 加载项 → Azure AI Foundry，直接 | Foundry 资源 + API 密钥 | `azure_resource_name`、`azure_api_key` |

Bedrock 和按用户配置（Bootstrap 端点或扩展属性）需要 `entra_sso=1`——加载项获取用户的 Entra ID Token 来认证这些流程。参见 [manifest](manifest.md) 中的 Entra SSO 章节。

## 步骤 1b — 哪些 Office 应用？

问：**Excel/Word/PowerPoint、Outlook，还是都要？** Outlook 是单独的清单，有一个额外的前置条件。

如果他们部署 Outlook：
- **Bedrock 目前不支持 Outlook。** 如果他们在步骤 1 选择了 `bedrock`，Outlook 暂时不可用——只生成 `office` 清单。
- **需要 Microsoft Graph 管理员授权。** 运行 [consent](consent.md#outlook--microsoft-graph-authorization)——全局管理员打开一个 URL 并点击接受。在生成清单之前完成，这样你可以问他们使用 Anthropic 的应用（不需要 `graph_client_id`）还是自己的 Entra 应用（获取 `graph_client_id`）。

转到匹配的章节。

---

## Vertex AI

### 1a. 前置条件

与管理员确认：
- GCP 项目 ID（他们应该知道）
- 有 Claude 模型配额的区域（通常是 `us-east5`）

### 1b. 创建 OAuth 客户端

没有 `gcloud` 命令可以完成此操作。打开控制台链接（替换他们的项目 ID），引导他们操作，他们粘贴回客户端 ID 和密钥。

> 打开：`https://console.cloud.google.com/apis/credentials?project=<PROJECT_ID>`
> → **创建凭据** → **OAuth 客户端 ID**
> - 应用类型：**Web 应用**
> - 名称：`Claude for Office`
> - 已授权的重定向 URI：`https://pivot.claude.ai/auth/callback`
> → **创建** → 复制**客户端 ID** 和**客户端密钥**

趁他们在的时候启用 Vertex API：

```bash
gcloud services enable aiplatform.googleapis.com --project=<PROJECT_ID>
```

获取：`gcp_project_id`、`gcp_region`、`google_client_id`、`google_client_secret`。

继续到[步骤 3](#步骤-3--决定哪些是组织范围-vs-按用户)。Vertex 使用 Google OAuth，不是 Entra，所以除非你也选择按用户配置（如果是，在步骤 3 决定后回到步骤 2），否则不需要管理员授权。

---

## Bedrock

### 1a. 前置条件

与管理员确认：
- AWS 账户 ID 和有 Claude 模型访问权限的区域（通常是 `us-east-1`）
- 他们的 Azure 租户 ID（从 Entra 管理中心，或 `az account show --query tenantId`）
- `aws` CLI 已配置到目标账户

### 1b. 创建 OIDC 提供商 + 角色

三个 `aws iam` 调用。信任策略的 `aud` 条件是安全边界——只有 Azure 为 Claude 加载项签发的 Token 才能承担此角色。

替换他们的租户 ID 和区域：

```bash
TENANT_ID="<their-azure-tenant-guid>"
CLAUDE_APP_ID="c2995f31-11e7-4882-b7a7-ef9def0a0266"
AWS_REGION="us-east-1"
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
ISSUER="login.microsoftonline.com/${TENANT_ID}/v2.0"

# OIDC 身份提供商。指纹是 API 要求的；AWS 通过自己的信任存储验证主要 IdP，
# 但参数不能省略。
THUMBPRINT=$(openssl s_client -servername login.microsoftonline.com \
  -connect login.microsoftonline.com:443 </dev/null 2>/dev/null \
  | openssl x509 -fingerprint -sha1 -noout | cut -d= -f2 | tr -d ':')

aws iam create-open-id-connect-provider \
  --url "https://${ISSUER}" \
  --client-id-list "${CLAUDE_APP_ID}" \
  --thumbprint-list "${THUMBPRINT}"

PROVIDER_ARN="arn:aws:iam::${ACCOUNT}:oidc-provider/${ISSUER}"

# 带有基于 aud 门控的信任策略的角色。
aws iam create-role --role-name ClaudeBedrockAccess \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Federated": "'"${PROVIDER_ARN}"'"},
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {"'"${ISSUER}"':aud": "'"${CLAUDE_APP_ID}"'"}
      }
    }]
  }'

# Bedrock 调用权限。
aws iam put-role-policy --role-name ClaudeBedrockAccess \
  --policy-name BedrockInvoke \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.*",
        "arn:aws:bedrock:*:'"${ACCOUNT}"':inference-profile/us.anthropic.*"
      ]
    }]
  }'

echo "aws_role_arn: arn:aws:iam::${ACCOUNT}:role/ClaudeBedrockAccess"
```

如果 `create-open-id-connect-provider` 报错 `EntityAlreadyExists`，说明该发行者已有提供商——没关系，角色会信任它。ARN 是确定性的（`arn:aws:iam::<account>:oidc-provider/<issuer>`）。

获取：`aws_role_arn`、`aws_region`。生成清单时添加 `entra_sso=1`——Bedrock 需要 Entra ID Token 作为 STS Web 身份。

继续到[步骤 2](#步骤-2--azure-管理员授权)。

---

## 网关

无需配置。获取网关基础 URL（LiteLLM、Portkey 等）和 Token。如果 Token 按用户不同，它去[步骤 5](#步骤-5--按用户配置)而非清单。

获取：`gateway_url`、`gateway_token`。

**API 格式。** 问：网关暴露的是 Anthropic `/v1/messages` API，还是到 Bedrock（`/model/{id}/invoke…`）或 Vertex（`…:rawPredict`）的透传？几乎总是 Anthropic——LiteLLM/Portkey/Kong 默认就是它，运行网关的意义就是统一的 `/v1/messages` 路由。仅当网关是保留上游线路格式的薄代理时，才将 `gateway_api_format` 设为 `bedrock` 或 `vertex`。如果是 `vertex`，还需获取 `gcp_project_id`（他们的 GCP 项目）和 `gcp_region`（通常是 `us-east5`）——它们是加载项构造的 URL 中的路径段。将 `gateway_url` 指向透传路径，如 `https://litellm.acme.com/bedrock` 或 `…/vertex_ai/v1`。

**认证头方案。** 加载项默认以 `x-api-key: <token>` 发送 Token——这是 LiteLLM、Portkey 和 Kong 开箱即用接受的。如果你的网关期望 `Authorization: Bearer <token>`（自定义/企业网关常见），设置 `gateway_auth_header=authorization`。如果不确定，先用 `x-api-key` 运行步骤 6 的冒烟测试——网关日志中出现 401 并提示"no Authorization header"意味着你需要 `authorization`。

继续到[步骤 3](#步骤-3--决定哪些是组织范围-vs-按用户)。网关认证是基于 Token 的，不是 Entra，所以除非你也选择按用户配置（如果是，在步骤 3 决定后回到步骤 2），否则不需要管理员授权。

---

## Azure AI Foundry

### 1a. 前置条件

与管理员确认：
- 一个至少部署了一个 Claude 模型的 Azure AI Foundry 资源
- 资源名称（端点 URL 的子域——如 `https://contoso-foundry.services.ai.azure.com` 中的 `contoso-foundry`）

### 1b. 获取 API 密钥

在 Azure Portal 中打开该资源，然后**密钥和端点** → 复制**密钥 1**。加载项自动检测资源中部署了哪些 Claude 模型，所以这里不需要模型配置。

获取：`azure_resource_name`、`azure_api_key`。

继续到[步骤 3](#步骤-3--决定哪些是组织范围-vs-按用户)。Foundry 认证是基于密钥的，不是 Entra，所以除非你也选择按用户配置（如果是，在步骤 3 决定后回到步骤 2），否则不需要管理员授权。

---

## 步骤 2 — Azure 管理员授权

**仅在 `entra_sso=1` 时需要**——即 Bedrock（Entra Token 是 STS Web 身份）或通过扩展属性/Bootstrap 的按用户配置。如果都不适用，跳到步骤 3。

读取 `${CLAUDE_PLUGIN_ROOT}/commands/consent.md` 并按其操作。

## 步骤 3 — 决定哪些是组织范围 vs 按用户

加载项先读取按用户的扩展属性，回退到清单参数。任何键都可以在任一层。所以问题是：**步骤 1 获取的值中，哪些按用户不同？**

具体地问——不要让他们自己映射：
- 网关：所有人一个 URL？一个 Token，还是每用户一个 Token？
- Vertex：所有人一个项目？一个区域，还是部分用户需要不同区域以满足数据驻留？
- Bedrock：所有人一个角色，还是团队特定角色？

| 答案 | 分配 |
|---|---|
| 没有不同 | 全部 → 清单。跳过步骤 5。 |
| 按用户唯一（如网关 Token） | 唯一键 → 步骤 5，其余 → 清单。 |

将分配写入设置日志，以便步骤 4 和步骤 5 各知道自己的子集。

## 步骤 4 — 生成清单

读取 `${CLAUDE_PLUGIN_ROOT}/commands/manifest.md` 并使用步骤 3 的**组织范围**值按其操作。为步骤 1b 的每个宿主生成一个文件：

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/build-manifest.mjs" office  manifest.xml         <key>=<value> ...
node "${CLAUDE_PLUGIN_ROOT}/scripts/build-manifest.mjs" outlook manifest-outlook.xml <key>=<value> ...
```

然后验证每个：

```bash
npx -y office-addin-manifest validate manifest.xml
npx -y office-addin-manifest validate manifest-outlook.xml
```

## 步骤 5 — 按用户配置

除非步骤 3 有内容路由到这里，否则跳过。否则根据你携带的内容选择机制：

| 携带内容 | 使用 | 读取 |
|---|---|---|
| 一两个字符串——Token、区域 | 扩展属性 | `${CLAUDE_PLUGIN_ROOT}/commands/update-user-attrs.md` |
| `mcp_servers`、`skills`、任何结构化内容 | Bootstrap 端点 | `${CLAUDE_PLUGIN_ROOT}/commands/bootstrap.md` |

属性是每用户一次 `az rest PATCH`——工作量少，但仅限扁平字符串 ≤256 字符。Bootstrap 是你构建的 HTTPS 服务——工作量多，但无形状限制。

## 步骤 6 — 验证模型可达

在他们部署之前，确认 **Claude Sonnet 4.5** 或 **Claude Opus 4.5**（或更新版本）中至少有一个能实际响应。指向未启用模型的清单部署正常，然后在用户首条消息时静默失败。

**网关：** 用 1 Token 请求探测。200 表示成功。404 表示网关不路由该模型名——试另一个，或让他们检查网关配置。429 表示认证成功但该模型无配额——试另一个。401/403 表示 Token 错误，这是步骤 1 的问题。

选择匹配 `gateway_api_format` 的 curl。（Windows：将 `/dev/null` 换成 `NUL`。如果 `gateway_auth_header=x-api-key`，将认证头行换成 `-H 'x-api-key: <token>'`。）

`gateway_api_format=anthropic`（默认）：
```bash
curl -s -o /dev/null -w '%{http_code}\n' "<gateway_url>/v1/messages" \
  -H 'content-type: application/json' -H 'authorization: Bearer <token>' \
  -d '{"model":"claude-sonnet-4-5","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'
```

`gateway_api_format=bedrock` — 模型在路径中，**不在**请求体中：
```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  "<gateway_url>/model/anthropic.claude-sonnet-4-5-v1:0/invoke" \
  -H 'content-type: application/json' -H 'authorization: Bearer <token>' \
  -d '{"anthropic_version":"bedrock-2023-05-31","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'
```

`gateway_api_format=vertex` — 模型、项目和区域都在路径中：
```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  "<gateway_url>/projects/<gcp_project_id>/locations/<gcp_region>/publishers/anthropic/models/claude-sonnet-4-5:rawPredict" \
  -H 'content-type: application/json' -H 'authorization: Bearer <token>' \
  -d '{"anthropic_version":"vertex-2023-10-16","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'
```

**Vertex：** 模型启用是手动操作——EULA 接受没有 API。打开 Model Garden 页面，确认至少一个模型在他们的区域显示**已启用**（不是"请求访问"）：

> `https://console.cloud.google.com/vertex-ai/publishers/anthropic?project=<PROJECT_ID>`

如果显示"请求访问"，他们点击进入，接受条款，等待启用。在他们确认之前不进行 API 调用。

**Bedrock：** 同样的约束——模型访问授权没有 API。打开模型访问页面，确认至少一个 Claude 4.5+ 模型显示**已授权访问**（不是"可请求"）：

> `https://console.aws.amazon.com/bedrock/home?region=<aws_region>#/modelaccess`

如果显示"可请求"，他们请求，接受条款，等待授权（通常几分钟，有时更长）。

将验证过的模型名称记录到设置日志。在获得 200、确认"已启用"或确认"已授权访问"之前不要继续——以匹配他们路径的为准。

## 步骤 7 — 部署

引导他们完成上传——有几个屏幕，用户分配那个是真正的决策点。

> 打开：`https://admin.cloud.microsoft/?#/Settings/IntegratedApps`
> → **上传自定义应用**
> - 应用类型：**Office 加载项**
> - 选择方式：**从设备上传清单文件 (.xml)** → 选择 `manifest.xml`
> - 上传时验证。如果这里报错，步骤 4 的 `npx office-addin-manifest validate` 应该已经捕获——重新运行。

**用户屏幕** — 决策点：
- 如果步骤 5 跳过了（没有按用户不同的内容）→ **整个组织** 没问题。
- 如果步骤 5 写入了按用户属性 → 分配给与 PATCH 的人完全匹配的**特定用户/组**。其他人会打开没有配置的加载项。
- 首次部署？从**仅限我**或试点组开始，确认有效，然后扩大。之后可以更改分配而无需重新部署。

> → **接受权限** → **完成部署**

传播到用户最长 24 小时（通常快得多）。加载项到达后，出现在 Excel/Word/PowerPoint 的 **Home → Add-ins** 中。

将最终清单路径和分配范围追加到设置日志。完成。
