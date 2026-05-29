---
description: 通过 Azure AD 扩展属性设置用户级配置（Token、区域覆盖）
---

# 通过扩展属性设置用户级配置

属性已注册在 Anthropic 的应用（`c2995f31-…`）上——你无需创建 schema，只需写入值。加载项从用户的 ID Token 中读取 `extension_c2995f3111e74882b7a7ef9def0a0266_<key>`。

**需要在清单文件中设置 `entra_sso=1`。** 没有它，加载项不会获取 Entra Token，这些属性也不会被读取——它们会静默失效。

任何配置键都可以按用户设置——加载项会将用户级属性合并到清单参数之上，因此这里的值优先。所有值最大 256 字符。

| 键 | 用户级用途 |
|---|---|
| `gateway_token` | 用户级 API 密钥（轮换） |
| `gateway_url` | 将不同团队路由到不同网关 |
| `gateway_api_format` | 网关使用 Bedrock/Vertex 透传格式，而非 Anthropic `/v1/messages` |
| `inference_headers` | 用户级网关记账标签（JSON；注意 256 字符限制） |
| `bootstrap_url` | 用户级凭据下发端点 |
| `gcp_project_id` | 不同团队使用不同 GCP 项目 |
| `gcp_region` | 数据驻留覆盖 |
| `google_client_id` `google_client_secret` | 不同团队使用不同 OAuth 客户端（不常见） |
| `aws_role_arn` `aws_region` | 不同团队使用不同 Bedrock 角色 |
| `otlp_endpoint` `otlp_headers` `otlp_resource_attributes` | 将遥测路由到团队专属的 OTEL 采集器 / 用团队级资源属性标记 Span |

## 单个用户

将 `<key>` 替换为上表中的属性名。对于非机密键（区域、项目 ID），这是常规路径。对于机密（`gateway_token`、`google_client_secret`），值会出现在 Shell 历史记录和本次对话记录中——如有顾虑请使用下方的批量 CSV 路径。

```bash
az rest --method PATCH \
  --uri "https://graph.microsoft.com/v1.0/users/<upn>" \
  --body '{"extension_c2995f3111e74882b7a7ef9def0a0266_<key>":"<value>"}'
```

成功时无输出——PATCH 返回 204 空响应体。验证：

```bash
az rest --method GET --uri "https://graph.microsoft.com/v1.0/users/<upn>?\$select=extension_c2995f3111e74882b7a7ef9def0a0266_<key>"
```

Graph 读取与写入立即一致——无延迟。要导出用户的所有扩展属性（不知道确切键名），使用 `/beta/`：

```bash
az rest --method GET --uri "https://graph.microsoft.com/beta/users/<upn>" | jq 'to_entries | map(select(.key | startswith("extension"))) | from_entries'
```

## 批量（CSV，值不会进入本对话）

让管理员准备 `users.csv`。第一列是 UPN；其余列标题是属性键。空单元格跳过该用户的该属性。

```
upn,gateway_token,gcp_region
alice@acme.com,sk-live-aaa,
bob@acme.com,sk-live-bbb,europe-west4
carol@acme.com,,europe-west4
```

**macOS/Linux** — 将以下内容写入 CSV 旁边的 `apply.sh`（`read -a` 数组语法仅适用于 bash；直接粘贴到 zsh 会出错）。审核后运行 `bash apply.sh`。你只能看到 ✓/✗——不要 `cat` 任一文件。

```bash
#!/bin/bash
EXT=extension_c2995f3111e74882b7a7ef9def0a0266_
{
  IFS=, read -ra keys
  while IFS=, read -ra vals; do
    upn="${vals[0]}"
    for i in "${!keys[@]}"; do
      [ "$i" -eq 0 ] || [ -z "${vals[$i]}" ] && continue
      az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/users/$upn" \
        --body "{\"${EXT}${keys[$i]}\":\"${vals[$i]}\"}" \
        && echo "✓ $upn ${keys[$i]}" || echo "✗ $upn ${keys[$i]}"
    done
  done
} < users.csv
```

**Windows** — 将以下内容写入 CSV 旁边的 `apply.ps1`。`Import-Csv` 直接将标题读取为 schema；在 PowerShell 中运行 `.\apply.ps1`。

```powershell
$EXT = 'extension_c2995f3111e74882b7a7ef9def0a0266_'
Import-Csv users.csv | ForEach-Object {
  $upn = $_.upn
  $_.PSObject.Properties | Where-Object { $_.Name -ne 'upn' -and $_.Value } | ForEach-Object {
    $body = @{ "$EXT$($_.Name)" = $_.Value } | ConvertTo-Json -Compress
    az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/users/$upn" --body $body
    if ($?) { "OK $upn $($_.Name)" } else { "FAIL $upn $($_.Name)" }
  }
}
```

报告 ✓ 和 ✗ 的数量。404 表示 UPN 错误；403 表示 `az login` 缺少 `User.ReadWrite.All` 权限——需要重新授权或使用管理员账号。

## 传播延迟

Graph 写入立即成功，但加载项通过用户在 NAA 登录时的 ID Token 读取这些值——而 Azure 的 STS 会缓存 Token 声明。新值对特定用户生效最多需要**一小时**。如果他们在 PATCH 后立即打开加载项且表现得像未配置一样，那是缓存问题，不是失败。告诉他们等待后重试；完全退出 Office 应用（不只是关闭任务窗格）会在下次启动时强制获取新的 NAA Token。
