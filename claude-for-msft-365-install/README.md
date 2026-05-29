# Claude for Office — 直连云端配置

管理工具，用于将 Claude Office 加载项配置为调用你自己的云端
（Vertex AI、Bedrock 或 LLM 网关），而非 Anthropic 的 API。

## 安装

```bash
claude plugin marketplace add anthropics/financial-services
claude plugin install claude-for-msft-365-install@claude-for-financial-services
```

然后在会话中执行：`/claude-for-msft-365-install:setup`

## 更新

拉取插件最新版本：

```bash
claude plugin update claude-for-msft-365-install@claude-for-financial-services
```

重启会话以应用更新。仅在需要用新选项重新生成清单文件时，才需要重新执行 `/claude-for-msft-365-install:setup`。

## Bootstrap

如果需要按用户配置 MCP 服务器、技能或动态配置，可托管一个 Bootstrap 端点并将加载项指向它：

```bash
claude plugin marketplace add anthropics/financial-services   # 如尚未添加
claude plugin install claude-for-msft-365-install@claude-for-financial-services
```

然后在会话中执行：`/claude-for-msft-365-install:bootstrap`

## 命令

| 命令 | 功能 |
|---|---|
| `/claude-for-msft-365-install:setup` | 交互式向导——配置云端资源、管理员授权、写入清单文件 |
| `/claude-for-msft-365-install:manifest` | 生成自定义加载项清单 XML |
| `/claude-for-msft-365-install:consent` | 生成加载项应用注册的 Azure 管理员授权 URL |
| `/claude-for-msft-365-install:update-user-attrs` | 通过 Microsoft Graph 扩展属性写入用户级配置 |
| `/claude-for-msft-365-install:bootstrap` | 构建 Bootstrap 端点——按用户配置 MCP 服务器、技能和动态配置 |
| `/claude-for-msft-365-install:debug` | 诊断部署问题——过期配置、连接失败、加载项缺失 |
