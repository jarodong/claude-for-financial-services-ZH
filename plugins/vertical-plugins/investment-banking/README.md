# 投行插件

投资银行生产力工具，涵盖股票研究、估值、演示文稿和交易材料。

## 功能

- **交易材料** - CIM、Teaser、流程函和买方名单
- **演示文稿** - 公司简介（Strip Profile）、品牌模板推介材料
- **交易支持** - 并购模型、交易跟踪和财务数据包

## 安装

```bash
claude --plugin-dir /path/to/investment-banking
```

或复制到你项目的 `.claude-plugin/` 目录。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/one-pager [公司]` | 推介材料用单页公司简介 |
| `/cim [公司]` | 起草保密信息备忘录 |
| `/teaser [公司]` | 匿名单页公司 Teaser |
| `/buyer-list [公司]` | 战略和财务买方名单 |
| `/merger-model [交易]` | 增厚/稀释 M&A 分析 |
| `/process-letter [交易]` | 报价指引和流程函件 |
| `/deal-tracker` | 跟踪活跃交易、里程碑和待办事项 |

## Skill

### 交易材料
| Skill | 描述 |
|-------|-------------|
| **cim-builder** | 起草保密信息备忘录（CIM） |
| **teaser** | 匿名单页公司 Teaser |
| **process-letter** | 报价指引和流程函件 |
| **buyer-list** | 战略和财务买方名单 |
| **datapack-builder** | 从 CIM 和公告文件构建财务数据包 |

### 演示文稿
| Skill | 描述 |
|-------|-------------|
| **strip-profile** | 推介材料用信息密集型公司简介 |
| **pitch-deck** | 将数据填充到推介材料模板 |

### 交易支持
| Skill | 描述 |
|-------|-------------|
| **merger-model** | 增厚/稀释 M&A 分析 |
| **deal-tracker** | 跟踪活跃交易、里程碑和待办事项 |

## 示例工作流程

### 单页公司简介
```
/one-pager Target

# 生成：
# - 使用 PPT 模板的单页公司简介
# - 4 个象限：概述、业务、财务、股权结构
# - 遵循模板边距和品牌规范
```

### CIM 起草
```
/cim Target

# 生成：
# - 完整 CIM 文档，包含执行摘要、业务概述、
#   财务分析和市场定位
```

### 并购模型
```
/merger-model Acquirer acquiring Target

# 生成：
# - 增厚/稀释分析
# - 资金来源与用途、备考财务数据
# - 购买价格和协同效应敏感性分析
```
