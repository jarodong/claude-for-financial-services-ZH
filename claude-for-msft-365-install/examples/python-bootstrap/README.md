# Bootstrap 端点 — Python 参考实现

Claude in Office `/bootstrap` 端点的最小 FastAPI 实现。它验证调用者的 Entra ID Token，并基于简单的首次匹配 RBAC 表返回按员工的 `skills` 和 `mcp_servers`。

## 对接你的真实 Entra 租户运行

```bash
pip install -r requirements.txt
# 查找你的租户 ID：
python get_tenant_id.py you@yourcompany.com
export TENANT_ID=<your-tenant-guid>
python app.py
```

## 使用假 Token 本地运行

```bash
pip install -r requirements.txt
export TENANT_ID=dev-tenant
TOKEN=$(python mint_dev_token.py --oid alice --group investment-banking)
DEV_JWKS_PATH=dev_jwks.json python app.py &
curl -H "Authorization: Bearer $TOKEN" \
     -H "X-Claude-User-Agent: claude-word/1.0.0" \
     http://127.0.0.1:8080/bootstrap
```

## 自定义

你需要修改的一切都在 **`config.py`** 中——`app.py` 不需要编辑。

- 编辑 `SKILLS` 和 `MCP_SERVERS` — 你可以分发的完整目录。
- 编辑 `RULES` — 首个匹配的规则生效；底部的空 `when: {}` 是默认规则。
- 将 `RULES` 中的占位符组/用户名替换为你真实的 Entra 对象 ID（GUID）。
- 组成员从 Token 的 `groups` 声明读取。如果你的租户不发送它，将 `app.py` 中的 `groups = ...` 行替换为对你内部目录的查找。
- 规则可以通过 `"app": "word" | "excel" | "powerpoint"` 按 Office 宿主限定范围，从加载项发送的 `X-Claude-User-Agent` 头解析。
- `groups` 声明**默认不在** Entra Token 中。在你的应用的*应用注册 → Token 配置 → 添加 groups 声明*下启用。
- 将内存中的 `RULES` 替换为你的真实数据源（数据库、配置服务等）。

## 安全

`DEV_JWKS_PATH` 让服务器信任自签发的签名密钥而非 Microsoft 的。除非绑定到 `127.0.0.1`，否则拒绝启动。**永远不要**在部署环境中设置它。
