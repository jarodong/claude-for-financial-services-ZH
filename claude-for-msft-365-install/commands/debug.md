---
description: 诊断部署问题——过期配置、连接失败、加载项缺失
---

# 诊断 Claude Office 部署问题

你正在帮助企业管理员认断已部署的加载项为何不正常工作。先问**出了什么问题**，然后路由。

## 分诊

请管理员描述症状。按回答路由：

| 症状 | 章节 |
|---|---|
| 更新了清单但用户仍看到旧配置 | [更新后配置过期](#更新后配置过期) |
| 加载项显示"连接失败" | [读取错误粘贴](#读取错误粘贴) |
| 加载项在 Excel/PowerPoint 中完全不显示 | [加载项不可见](#加载项不可见) |
| 想在部署前本地测试/迭代清单 | [旁加载清单进行本地调试](#旁加载清单进行本地调试) |
| 登录弹窗失败或循环 | [管理员授权](#管理员授权) |
| 需要查看浏览器控制台 | [打开加载项的浏览器开发者工具](#打开加载项的浏览器开发者工具) |

如果他们有来自加载项的错误粘贴（连接失败屏幕上的**复制错误详情**按钮），始终从那里开始。它包含所有信息。

---

## 读取错误粘贴

粘贴结构：

```
Claude for Office connection failed (<Provider>)
Build: <sha>

<friendly message>

Request:
  <key>: <value actually sent>
  ...

Manifest params:
  <key>: <value the deployed manifest carries>
  ...

Raw error:
<SDK/HTTP error>
```

**检查要点：**

- `Request:` 与 `Manifest params:` 的差异。两块中的键是相同的 snake_case 名称，直接对比即可。如果有差异，说明用户在表单中输入了覆盖值。如果匹配，说明清单值原样通过。
- `Manifest params:` 中的 `m` 键是版本标签（如 `unified-1.0.0.11`）。如果低于你上次上传的版本，用户使用的是过期清单。转到[配置过期](#更新后配置过期)。
- `Raw error:` 是根本真相。常见模式：
  - `invalid_client`（401，Google）→ 该 `google_client_id` 对应的 `google_client_secret` 错误。在 GCP 控制台 → 凭据中验证。
  - `Load failed (<host>)` → WebView 层网络被阻止。防火墙需要允许该主机。
  - `STS AssumeRoleWithWebIdentity failed` → AWS IAM OIDC 提供商配置错误或角色信任策略错误。
  - `HTTP 401/403`（网关）→ Token 错误或网关拒绝了密钥。

---

## 更新后配置过期

两层缓存，两个时钟：

| 层级 | 持有者 | TTL | 清除方式 |
|---|---|---|---|
| 服务端 | M365 管理中心 → Exchange Online → 客户端 | 更新最长 **72 小时**（首次部署 24 小时） | 等待，或用新的 `<Id>` 重新部署 |
| 客户端 | 每台机器上 Office 应用的 Wef 文件夹 | 直到应用重启，有时更长 | 清除缓存清单（见下文） |

Microsoft 自己的 FAQ：
> 加载项更新、开启或关闭的更改最长可能需要 72 小时才能对用户生效。
> https://learn.microsoft.com/en-us/microsoft-365/admin/manage/centralized-deployment-faq

### 确认管理中心提供的是什么

管理中心会静默忽略使用相同 `<Version>` 的重新上传。如果你上传了修复但没有递增第四段，它从未生效。打开 M365 管理中心 → 集成应用 → 你的加载项 → 检查列出的版本。

### 强制客户端刷新

过期的**旁加载**清单在不同平台上存储方式不同：

- **macOS** — 每个应用的 `Documents/wef` 文件夹中的 `<addin-id>.manifest-*.xml` 文件，与其他所有加载项并列。
- **Windows** — `HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer` 下的**注册表**值（没有按加载项的文件可删除；清除 `Wef` *文件夹*是另一个更粗暴的操作——见下方注意事项）。

使用辅助脚本。它们只针对你的加载项的 `<Id>`，直接执行 `rm`/注册表编辑——它们**不会**调用 `office-addin-dev-settings`（它的删除路径在客户电话中坑过我们）：

- macOS：[`scripts/clear-addin-cache.sh`](../scripts/clear-addin-cache.sh)
- Windows：[`scripts/clear-addin-cache.ps1`](../scripts/clear-addin-cache.ps1)

先退出 Excel/Word/PowerPoint。脚本是 **ID 优先**的——直接传入加载项 `<Id>`（在跨新/多个 ID 迭代时很方便）；清单路径是一个可选便利，只是帮你读取 `<Id>`。

```bash
# macOS — 列出所有，不执行任何操作：
./scripts/clear-addin-cache.sh

# 按 ID 模拟运行（推荐），或通过清单：
./scripts/clear-addin-cache.sh --id <GUID>
./scripts/clear-addin-cache.sh ~/path/to/manifest.xml

# 实际删除（仅此 ID 的文件）：
./scripts/clear-addin-cache.sh --id <GUID> --apply
```

```powershell
# Windows — 相同流程，注册表范围：
.\scripts\clear-addin-cache.ps1                  # 列出，不执行
.\scripts\clear-addin-cache.ps1 -Id <GUID>       # 模拟运行
.\scripts\clear-addin-cache.ps1 -Id <GUID> -Apply
```

两者**默认模拟运行**——没有 `--apply` / `-Apply` 不会删除任何内容。无参数列出每个已注册的加载项，以便你先确认 ID。其他加载项不受影响。

**清除后必须完全重启 Office 应用。** 删除文件/注册表项在应用启动时重新读取之前不起作用——而*后台运行*的应用算作仍在运行。退出**并重新打开** Excel / Word / PowerPoint，先确认没有残留进程：`pkill -f "Microsoft Excel"`（macOS）/ 检查任务管理器（Windows）。脚本完成时也会打印此提醒。

**按 ID 删除本地/旁加载清单是安全且有效的。** 实际上，只删除一个加载项的文件（macOS）或注册表值（Windows）会干净地移除该加载项，其余加载项正常加载——我们经常这样做。Microsoft 的"不要删除单个文件"警告是关于*另一个*缓存（见下文），不是这些本地开发/旁加载条目；不要让它吓到你放弃这里的精准路径。

> **集中部署（管理中心）在 Windows 上的过期**是*另一个*缓存：`%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\<guid>\…`，以不透明哈希存储，**不是**按加载项 ID。Microsoft 的官方指导是保守的——整体清除该文件夹的内容，因为*"删除单个清单文件可能导致所有加载项停止加载。"* 实际上针对性删除也可以工作，但文件名不是 ID 映射的，所以很难精准操作——这就是这些脚本刻意**不**触碰它的原因。如果集中部署更新过期，优先等待服务端 TTL 过期或用新的 `<Id>` 重新部署（见下文），而不是手动删除该缓存。

重启后仍然过期的话，说明服务端缓存还没赶上。等待，或使用新的 `<Id>`（见下文）。

Microsoft 的缓存清除文档：https://learn.microsoft.com/en-us/office/dev/add-ins/testing/clear-cache

### 终极方案：用新 Id 重新部署

如果 72 小时不可接受，新的 `<Id>` UUID 会强制管理中心和每个客户端将其视为全新加载项（首次部署 SLA 24 小时，通常快得多）。编辑 `manifest.xml`，将 `<Id>` 内的文本替换为新 UUID（mac/linux 用 `uuidgen`，PowerShell 用 `[guid]::NewGuid()`），重新上传。

---

## 加载项不可见

- **不在功能区中：** 检查 M365 管理中心 → 集成应用 → 你的加载项 → 用户选项卡。用户（或其组）是否已分配？不支持嵌套组。
- **显示"我的加载项"但没有功能区按钮：** 清单的 `<Hosts>` 可能不包含此应用。检查两个 `<Hosts>` 列表（顶层和 `<VersionOverrides>` 下的）。
- **首次部署，不到 24 小时：** 正常。Microsoft 对首次部署可见性的 SLA 是 24 小时。

---

## 旁加载清单进行本地调试

要在**不通过管理中心部署**的情况下迭代清单（无 24-72 小时缓存等待），直接将 Office 指向本地清单文件。清单留在磁盘上的原位置；你只需告诉 Office 在哪里找到它。选择客户操作系统对应的方案。

使用辅助脚本——它们从清单中读取 `<Id>` 并按平台正确安装（macOS：每个应用的 `Documents/wef` 中的 `<Id>.manifest.xml` 文件；Windows：`HKCU:\SOFTWARE\Microsoft\Office\16.0\Wef\Developer` 下以 `<Id>` 命名的注册表值）。两者都直接写入文件/注册表——**不是** `office-addin-dev-settings`。

- macOS 安装：[`scripts/sideload-addin.sh`](../scripts/sideload-addin.sh)
- Windows 安装：[`scripts/sideload-addin.ps1`](../scripts/sideload-addin.ps1)
- 移除（任一系统）：`clear-addin-cache.{sh,ps1}` — 见[强制客户端刷新](#强制客户端刷新)

```bash
# macOS — 直接安装：
./scripts/sideload-addin.sh ~/path/to/manifest.xml
```

```powershell
# Windows — 直接安装：
.\scripts\sideload-addin.ps1 C:\path\to\manifest.xml
```

旁加载是增量且幂等的，所以直接安装——**无模拟运行**（与破坏性的 `clear-addin-cache` 不同，后者默认保持模拟运行）。安装按加载项 `<Id>` 命名条目，所以后续移除是完全逆操作：`clear-addin-cache.{sh,ps1} --id <GUID> --apply`（旁加载脚本完成时会打印精确的移除命令）。

然后**完全退出并重新打开** Excel / Word / PowerPoint——先检查任务管理器（Windows）/ `pkill -f "Microsoft Excel"`（macOS）；后台应用不会重新读取注册表或重新扫描文件夹。加载项出现在 **Insert → My Add-ins**（Windows 还会在 **Home** 选项卡 / **Shared Folder** 组中显示）；将其固定。

**注意事项（两个平台）：**
- 这是按用户和按机器的——不涉及租户部署。纯粹用于客户在自己的机器上调试/迭代。
- 本地旁加载的清单**优先于**具有相同 `<Id>` 的集中部署清单，所以这也是在重新上传到管理中心之前快速测试清单修复的方法。
- 将此与[浏览器开发者工具](#打开加载项的浏览器开发者工具)配合使用，在迭代时查看控制台/网络。
- 如果过期副本持续加载，也要清除缓存——见[强制客户端刷新](#强制客户端刷新)。

Microsoft 的旁加载参考：
- Windows：https://learn.microsoft.com/en-us/office/dev/add-ins/testing/create-a-network-shared-folder-catalog-for-task-pane-and-content-add-ins
- macOS：https://learn.microsoft.com/en-us/office/dev/add-ins/testing/sideload-an-office-add-in-on-mac

---

## 管理员授权

如果用户看到登录弹窗立即关闭或循环，说明租户尚未向 Claude 应用授予管理员授权。运行 [`:consent`](consent.md) 生成供全局管理员批准的授权 URL。错误粘贴中的症状：原始错误中的 `user_canceled`（代理将任何无法分类的关闭映射为此）。

---

## 静默 SSO / Entra Token 失败

- **`AADSTS50194: …not configured as a multi-tenant application` / `Use a tenant-specific endpoint`** — 你的 `graph_client_id`（或 `entra_scope` 资源应用）是单租户应用，而加载项构建版本太旧，仍在向 `/common` 权威机构请求 Token。较新的构建在设置了 `graph_client_id` 时会自动解析租户特定权威机构。修复：让用户更新到最新加载项版本。旧构建上没有清单变通方案。
- **`entra_scope requires graph_client_id`** — 设置了 `entra_scope` 但没有 `graph_client_id`。自定义范围的访问 Token 必须由你自己的 Entra 应用签发，而不是默认应用；两者都要设置。构建脚本也会拒绝此配对。
- **静默 SSO 失败，然后交互式弹窗成功** — 在租户中存在服务主体之前的首次运行时是预期行为。一旦管理员授权完成（见上文），静默路径就会成功。

---

## 打开加载项的浏览器开发者工具

当你需要 WebView 的控制台——JS 错误、网络选项卡、加载项的调试日志——你必须附加宿主操作系统的浏览器开发者工具。加载项运行在没有地址栏和内置 F12 的嵌入式 WebView 中，所以每个操作系统有自己的方案。

### macOS（Safari Web Inspector）

三道关卡。**第 3 道是大家都漏掉的。**

1. **Office 开发者扩展** — 先退出应用，然后：
   ```bash
   defaults write com.microsoft.Excel OfficeWebAddinDeveloperExtras -bool true
   defaults write com.microsoft.Powerpoint OfficeWebAddinDeveloperExtras -bool true
   defaults write com.microsoft.Word OfficeWebAddinDeveloperExtras -bool true
   ```
   使右键 → **检查元素**出现在任务窗格内。

2. **Safari 开发菜单** — Safari → 设置 → 高级 → 勾选*显示网页开发者功能*。

3. **macOS 开发者工具白名单**（Sonoma 及更高版本）— 系统设置 → 隐私与安全 → 开发者工具 → 打开 **Terminal** 的开关。没有这个，即使第 1、2 道关卡都打开，Safari 的开发菜单也会显示*"无可检查的应用"*。

任务窗格打开后，要么右键点击其中 → **检查元素**，要么去 Safari → 开发 → *[你的机器名]* → 找到加载项宿主（生产环境是 `pivot.claude.ai`，否则是你配置的域名）。

**陷阱：**
- **Office 更新会静默重置第 1 道关卡。** 如果上周检查正常现在不行了，重新运行 `defaults write`。
- *"无可检查的应用"* = 第 3 道关卡缺失，或 Office 应用在 `defaults write` 之前没有完全退出。`pkill -f "Microsoft Excel"` 然后重新启动。
- 任务窗格必须**打开**（不只是应用）才会出现在 Safari 的开发菜单下。

### Windows（Edge DevTools）

取决于 Office 使用的是哪个 WebView 引擎。当前 Win10/11 上带 WebView2 运行时的 M365 使用 Chromium；较旧的永久版 Office 或没有运行时的机器可能仍在 IE11/Trident 上。

**WebView2（Chromium — 常见情况）：**

右键点击任务窗格内 → **检查**。就这样，没有关卡。如果右键点击不显示"检查"，从 Microsoft Store 安装 **Microsoft Edge DevTools Preview**——它列出所有可附加的 WebView2 目标，包括 Office 加载项。启动它，在目标列表中找到加载项的 URL，点击附加。

**IE11/Trident（旧版 Office 2019/2021 永久版）：**

从管理员 PowerShell 运行 IEChooser：
```powershell
& "C:\Windows\SysWOW64\F12\IEChooser.exe"
```
从列表中选择加载项的页面。如果列表为空，说明任务窗格还没打开——先打开它，然后刷新 IEChooser。

Microsoft 的演练：https://learn.microsoft.com/en-us/office/dev/add-ins/testing/debug-add-ins-using-devtools-edge-chromium
