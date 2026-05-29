---
description: Azure 管理员授权 URL——一次性租户审批，用于 Entra SSO 和 Outlook Graph 访问
---

# Azure 管理员授权

**仅在清单文件中设置了 `entra_sso=1` 时需要。** 使用组织级配置的 Gateway 和 Vertex 设置不使用 Entra，可跳过此步骤。如果你设置了 `graph_client_id`（你自己的 Entra 应用），此页面也不适用——你直接在自己的应用上管理授权。

每个租户只需一次。全局管理员打开此 URL，点击"接受"，完成。在此之前，加载项内的 NAA 登录对租户中的所有用户都会失败。

## URL

所有客户使用同一个 URL——`/organizations/` 会从登录者解析出租户。无需替换。

```
https://login.microsoftonline.com/organizations/adminconsent?client_id=c2995f31-11e7-4882-b7a7-ef9def0a0266&redirect_uri=https://pivot.claude.ai/auth/callback
```

打印此 URL。告诉他们：在浏览器中打开，确保已登录其租户的**全局管理员**账号。他们会看到一个权限屏幕，列出加载项读取的内容（用户配置文件、扩展属性）。点击**接受**后，会跳转到确认页面——"管理员授权已授予，可以关闭此标签页。"

## 验证

```bash
az ad sp show --id c2995f31-11e7-4882-b7a7-ef9def0a0266 --query appId -o tsv
```

如果返回相同的 GUID，说明服务主体已存在于其租户中——授权成功。如果报错"不存在"，说明授权未完成。

## Outlook — Microsoft Graph 授权

**仅在部署 Outlook 清单文件时需要。** 与上述 `entra_sso` 独立；即使 `entra_sso` 关闭也需要。

Claude for Outlook 通过 Microsoft Graph 读取邮件和日历。Graph Token 保留在用户的 Outlook 客户端中，不会发送到网关或 Anthropic，因此无论哪个云端提供模型服务，此授权都是相同的。全局管理员打开 URL，点击"接受"，完成。

```
https://login.microsoftonline.com/organizations/v2.0/adminconsent?client_id=c2995f31-11e7-4882-b7a7-ef9def0a0266&scope=https://graph.microsoft.com/Mail.ReadWrite%20https://graph.microsoft.com/Calendars.Read%20https://graph.microsoft.com/People.Read%20https://graph.microsoft.com/User.Read%20offline_access&redirect_uri=https://pivot.claude.ai/auth/callback
```

如果没有完成此授权，每个用户在 Claude 首次尝试读取邮件时都会遇到"需要管理员批准"的障碍。

**如果其策略禁止授权第三方应用：** 他们可以注册自己的单租户 Entra 应用，配置相同的委托 Graph 权限（Mail.ReadWrite、Calendars.Read、People.Read、User.Read、offline_access），在其上授予管理员授权，并在生成 Outlook 清单时将其 client ID 作为 `graph_client_id` 传入。数据流相同；授权在他们的应用下而非 Anthropic 的应用下。
