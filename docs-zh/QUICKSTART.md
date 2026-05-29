# 快速上手

> 60 秒完成安装，开始使用中文版金融套件。

## 前置条件

- [Claude Code](https://claude.com/product/claude-code) 已安装
- 或 [Claude Cowork](https://claude.com/product/cowork) 账号

## 方式一：Claude Code 安装

```bash
# 1. 添加市场源
claude plugin marketplace add anthropics/financial-services

# 2. 安装核心 Skill + 连接器（必装）
claude plugin install financial-analysis@claude-for-financial-services

# 3. 安装你需要的 Agent（选装）
claude plugin install valuation-reviewer@claude-for-financial-services
claude plugin install model-builder@claude-for-financial-services
claude plugin install pitch-agent@claude-for-financial-services

# 4. 安装垂直 Skill 包（选装）
claude plugin install investment-banking@claude-for-financial-services
claude plugin install private-equity@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

## 方式二：Cowork 安装

1. 打开 Cowork → Settings → Plugins → Add plugin
2. 粘贴仓库 URL 或上传 zip
3. 选择需要的 Agent 和垂直插件

## 验证安装

安装后，在 Claude Code 中测试：

```
/comps          # 可比公司分析
/dcf            # DCF 估值
/lbo            # 杠杆收购模型
/earnings       # 财报分析
/ic-memo        # 投决会备忘录
```

## 推荐安装顺序

| 优先级 | 插件 | 用途 |
|--------|------|------|
| P0 | financial-analysis | 核心建模 Skill + 所有数据连接器 |
| P1 | valuation-reviewer | 估值审查，直接用于投决会 |
| P1 | model-builder | DCF/LBO/三表模型构建 |
| P2 | market-researcher | 行业研究、可比分析 |
| P2 | pitch-agent | Pitch 材料、投资建议书 |
| P3 | investment-banking | CIM、Teaser、交易执行 |
| P3 | private-equity | 尽调、投决会、投后监控 |

## 常见问题

**Q: 安装后 Skill 没有触发？**
A: Skill 在相关上下文时自动触发。确保已安装 `financial-analysis` 核心包。

**Q: 如何查看已安装的插件？**
A: 运行 `/plugin list` 或在 Cowork Settings 中查看。

**Q: MCP 连接器需要额外配置吗？**
A: 部分连接器需要 API 密钥或订阅。参见 `.mcp.json` 配置。

---

> 详细翻译规范和术语表参见 [`docs-zh/TERMS.md`](./TERMS.md)。
