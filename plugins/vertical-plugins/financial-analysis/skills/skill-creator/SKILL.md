---
name: skill-creator
description: 创建有效 Skill 的指南。当用户希望创建新 Skill（或更新现有 Skill）以通过专业知识、工作流或工具集成扩展 Claude 能力时使用此 Skill。
license: Complete terms in LICENSE.txt
---

# Skill 创建器

本 Skill 提供创建有效 Skill 的指导。

## 关于 Skill

Skill 是模块化、自包含的包，通过提供专业知识、工作流和工具来扩展 Claude 的能力。可以将其视为特定领域或任务的"入门指南"——它们将 Claude 从通用 Agent 转变为配备任何模型都无法完全拥有的程序性知识的专业 Agent。

### Skill 提供的内容

1. 专业工作流 - 特定领域的多步骤流程
2. 工具集成 - 处理特定文件格式或 API 的指令
3. 领域专业知识 - 公司特定知识、Schema、业务逻辑
4. 捆绑资源 - 用于复杂和重复任务的脚本、参考和资产

## 核心原则

### 简洁为王

上下文窗口是公共资源。Skill 与 Claude 需要的一切共享上下文窗口：System Prompt、对话历史、其他 Skill 的元数据以及实际的用户请求。

**默认假设：Claude 已经非常聪明。** 只添加 Claude 没有的上下文。对每条信息质疑："Claude 真的需要这个解释吗？"和"这段文字值得消耗 Token 吗？"

优先使用简洁示例而非冗长解释。

### 设置适当的自由度

根据任务的脆弱性和可变性匹配具体程度：

**高自由度（纯文本指令）**：当多种方法都有效、决策取决于上下文或启发式方法指导时使用。

**中等自由度（伪代码或带参数的脚本）**：当存在首选模式、允许一定变化或配置影响行为时使用。

**低自由度（特定脚本，少量参数）**：当操作脆弱且容易出错、一致性至关重要或必须遵循特定序列时使用。

将 Claude 想象为探索路径：有悬崖的窄桥需要具体护栏（低自由度），而开阔田野允许多条路线（高自由度）。

### Skill 的结构

每个 Skill 由一个必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML Frontmatter 元数据（必需）
│   │   ├── name:（必需）
│   │   └── description:（必需）
│   └── Markdown 指令（必需）
└── 捆绑资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 按需加载到上下文的文档
    └── assets/           - 输出中使用的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

每个 SKILL.md 包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。这些是 Claude 读取以决定何时使用 Skill 的唯一字段，因此清晰全面地描述 Skill 是什么以及何时使用非常重要。
- **正文**（Markdown）：使用 Skill 的指令和指导。仅在 Skill 触发后加载（如果有的话）。

#### 捆绑资源（可选）

##### 脚本（`scripts/`）

可执行代码（Python/Bash 等），用于需要确定性可靠性或反复重写的任务。

- **何时包含**：当相同代码被反复重写或需要确定性可靠性时
- **示例**：`scripts/rotate_pdf.py` 用于 PDF 旋转任务
- **优点**：Token 高效、确定性、可执行而无需加载到上下文
- **注意**：Claude 可能仍需读取脚本以进行修补或环境特定调整

##### 参考资料（`references/`）

文档和参考材料，旨在按需加载到上下文中以指导 Claude 的流程和思考。

- **何时包含**：当 Claude 工作时应参考的文档
- **示例**：`references/finance.md` 用于金融 Schema、`references/mnda.md` 用于公司 NDA 模板、`references/policies.md` 用于公司政策、`references/api_docs.md` 用于 API 规范
- **使用场景**：数据库 Schema、API 文档、领域知识、公司政策、详细工作流指南
- **优点**：保持 SKILL.md 精简，仅在 Claude 判断需要时加载
- **最佳实践**：如果文件较大（>10k 字），在 SKILL.md 中包含 Grep 搜索模式
- **避免重复**：信息应只存在于 SKILL.md 或参考文件中，而非两者。对于详细信息优先使用参考文件，除非它确实是 Skill 的核心——这保持 SKILL.md 精简，同时使信息可发现而不占用上下文窗口。SKILL.md 中仅保留必要的流程指令和工作流指导；将详细参考材料、Schema 和示例移至参考文件。

##### 资产（`assets/`）

不打算加载到上下文的文件，而是在 Claude 生成的输出中使用。

- **何时包含**：当 Skill 需要在最终输出中使用的文件时
- **示例**：`assets/logo.png` 用于品牌资产、`assets/slides.pptx` 用于 PowerPoint 模板、`assets/frontend-template/` 用于 HTML/React 样板、`assets/font.ttf` 用于字体
- **使用场景**：模板、图片、图标、样板代码、字体、会被复制或修改的示例文档
- **优点**：将输出资源与文档分离，使 Claude 能够使用文件而无需加载到上下文

#### Skill 中不应包含的内容

Skill 应只包含直接支持其功能的必要文件。不要创建多余文档或辅助文件，包括：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 等等

Skill 应只包含 AI Agent 完成手头工作所需的信息。不应包含创建过程的辅助上下文、设置和测试流程、面向用户的文档等。创建额外的文档文件只会增加混乱。

### 渐进式披露设计原则

Skill 使用三级加载系统来高效管理上下文：

1. **元数据（name + description）** - 始终在上下文中（约 100 词）
2. **SKILL.md 正文** - Skill 触发时（<5k 词）
3. **捆绑资源** - Claude 按需使用（无限制，因为脚本可以执行而无需读入上下文窗口）

#### 渐进式披露模式

保持 SKILL.md 正文精简，不超过 500 行以最小化上下文膨胀。接近此限制时将内容拆分为单独文件。将内容拆分到其他文件时，必须从 SKILL.md 中引用它们并清楚描述何时读取，以确保 Skill 读者知道它们存在以及何时使用。

**关键原则：** 当 Skill 支持多个变体、框架或选项时，SKILL.md 中仅保留核心工作流和选择指导。将变体特定的细节（模式、示例、配置）移至单独的参考文件。

**模式 1：带参考的高级指南**

```markdown
# PDF 处理

## 快速开始

使用 pdfplumber 提取文本：
[代码示例]

## 高级功能

- **表单填充**：参见 [FORMS.md](FORMS.md) 获取完整指南
- **API 参考**：参见 [REFERENCE.md](REFERENCE.md) 获取所有方法
- **示例**：参见 [EXAMPLES.md](EXAMPLES.md) 获取常见模式
```

Claude 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

**模式 2：按领域组织**

对于有多个领域的 Skill，按领域组织内容以避免加载无关上下文：

```
bigquery-skill/
├── SKILL.md（概览和导航）
└── reference/
    ├── finance.md（收入、计费指标）
    ├── sales.md（商机、管线）
    ├── product.md（API 使用、功能）
    └── marketing.md（营销活动、归因）
```

当用户询问销售指标时，Claude 只读取 sales.md。

类似地，对于支持多个框架或变体的 Skill，按变体组织：

```
cloud-deploy/
├── SKILL.md（工作流 + 供应商选择）
└── references/
    ├── aws.md（AWS 部署模式）
    ├── gcp.md（GCP 部署模式）
    └── azure.md（Azure 部署模式）
```

当用户选择 AWS 时，Claude 只读取 aws.md。

**模式 3：条件详情**

显示基本内容，链接到高级内容：

```markdown
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

简单编辑直接修改 XML。

**修订追踪**：参见 [REDLINING.md](REDLINING.md)
**OOXML 详情**：参见 [OOXML.md](OOXML.md)
```

Claude 仅在用户需要这些功能时读取 REDLINING.md 或 OOXML.md。

**重要指导：**

- **避免深层嵌套引用** - 从 SKILL.md 保持引用一层深度。所有参考文件应直接从 SKILL.md 链接。
- **结构化较长的参考文件** - 对于超过 100 行的文件，在顶部包含目录，以便 Claude 在预览时看到完整范围。

## Skill 创建流程

Skill 创建包括以下步骤：

1. 通过具体示例理解 Skill
2. 规划可复用的 Skill 内容（脚本、参考资料、资产）
3. 初始化 Skill（运行 init_skill.py）
4. 编辑 Skill（实现资源并编写 SKILL.md）
5. 打包 Skill（运行 package_skill.py）
6. 基于实际使用迭代

按顺序遵循这些步骤，仅在有明确理由时跳过。

### 第一步：通过具体示例理解 Skill

仅在 Skill 的使用模式已清楚理解时跳过此步骤。即使处理现有 Skill，此步骤仍有价值。

要创建有效的 Skill，需要清楚理解 Skill 将如何使用的具体示例。这种理解可以来自直接的用户示例，也可以来自经用户反馈验证的生成示例。

例如，构建图片编辑器 Skill 时，相关问题包括：

- "图片编辑器 Skill 应支持什么功能？编辑、旋转，还有其他吗？"
- "能给出一些此 Skill 如何使用的示例吗？"
- "我能想象用户会问类似'去除此图片的红眼'或'旋转此图片'的事情。你还能想象此 Skill 的其他使用方式吗？"
- "用户会说什么来触发此 Skill？"

为避免让用户不知所措，避免在单条消息中询问过多问题。从最重要的问题开始，根据需要跟进以获得更好的效果。

当对 Skill 应支持的功能有清晰认识时结束此步骤。

### 第二步：规划可复用的 Skill 内容

要将具体示例转化为有效的 Skill，通过以下方式分析每个示例：

1. 考虑如何从零开始执行示例
2. 识别反复执行这些工作流时有帮助的脚本、参考资料和资产

示例：构建处理"帮我旋转此 PDF"查询的 `pdf-editor` Skill 时，分析表明：

1. 旋转 PDF 每次都需要重写相同代码
2. `scripts/rotate_pdf.py` 脚本有助于存储在 Skill 中

示例：设计处理"为我构建一个待办应用"或"构建一个追踪步数的仪表板"查询的 `frontend-webapp-builder` Skill 时，分析表明：

1. 编写前端 Web 应用每次都需要相同的样板 HTML/React
2. 包含样板 HTML/React 项目文件的 `assets/hello-world/` 模板有助于存储在 Skill 中

示例：构建处理"今天有多少用户登录？"查询的 `big-query` Skill 时，分析表明：

1. 查询 BigQuery 每次都需要重新发现表 Schema 和关系
2. 记录表 Schema 的 `references/schema.md` 文件有助于存储在 Skill 中

为确定 Skill 的内容，分析每个具体示例以创建要包含的可复用资源列表：脚本、参考资料和资产。

### 第三步：初始化 Skill

此时，是实际创建 Skill 的时候了。

仅在正在开发的 Skill 已存在且需要迭代或打包时跳过此步骤。此时继续下一步。

从零创建新 Skill 时，始终运行 `init_skill.py` 脚本。该脚本方便地生成新的模板 Skill 目录，自动包含 Skill 所需的一切，使 Skill 创建过程更高效可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

脚本会：

- 在指定路径创建 Skill 目录
- 生成带有正确 Frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 SKILL.md 和示例文件。

### 第四步：编辑 Skill

编辑（新生成或现有的）Skill 时，记住 Skill 是为另一个 Claude 实例使用的。包含对 Claude 有益且非显而易见的信息。考虑什么程序性知识、领域特定细节或可复用资产能帮助另一个 Claude 实例更有效地执行这些任务。

#### 学习成熟的设计模式

根据 Skill 需求参考这些有用的指南：

- **多步骤流程**：参见 references/workflows.md 了解顺序工作流和条件逻辑
- **特定输出格式或质量标准**：参见 references/output-patterns.md 了解模板和示例模式

这些文件包含有效 Skill 设计的成熟最佳实践。

#### 从可复用 Skill 内容开始

要开始实现，从上面确定的可复用资源开始：`scripts/`、`references/` 和 `assets/` 文件。注意此步骤可能需要用户输入。例如，实现 `brand-guidelines` Skill 时，用户可能需要提供品牌资产或模板存储在 `assets/` 中，或文档存储在 `references/` 中。

添加的脚本必须通过实际运行进行测试，确保没有 Bug 且输出符合预期。如果有许多类似脚本，只需测试代表性样本以确保它们都能工作，同时平衡完成时间。

不需要的示例文件和目录应删除。初始化脚本在 `scripts/`、`references/` 和 `assets/` 中创建示例文件以演示结构，但大多数 Skill 不需要所有这些。

#### 更新 SKILL.md

**写作指南：** 始终使用祈使/不定式形式。

##### Frontmatter

编写包含 `name` 和 `description` 的 YAML Frontmatter：

- `name`：Skill 名称
- `description`：这是 Skill 的主要触发机制，帮助 Claude 理解何时使用 Skill。
  - 包含 Skill 做什么以及使用它的具体触发条件/上下文。
  - 所有"何时使用"信息放在这里——不要放在正文中。正文仅在触发后加载，因此正文中的"何时使用此 Skill"部分对 Claude 没有帮助。
  - `docx` Skill 的描述示例："全面的文档创建、编辑和分析，支持修订追踪、批注、格式保留和文本提取。当 Claude 需要处理专业文档（.docx 文件）时使用：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理修订追踪，(4) 添加批注，或任何其他文档任务"

YAML Frontmatter 中不包含其他字段。

##### 正文

编写使用 Skill 及其捆绑资源的指令。

### 第五步：打包 Skill

Skill 开发完成后，必须打包为可分发的 .skill 文件，与用户共享。打包过程会自动先验证 Skill 以确保满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

可选输出目录指定：

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本将：

1. **自动验证** Skill，检查：

   - YAML Frontmatter 格式和必填字段
   - Skill 命名约定和目录结构
   - 描述完整性和质量
   - 文件组织和资源引用

2. 如果验证通过则**打包** Skill，创建以 Skill 命名的 .skill 文件（如 `my-skill.skill`），包含所有文件并维护正确的目录结构以便分发。.skill 文件是具有 .skill 扩展名的 Zip 文件。

如果验证失败，脚本将报告错误且不创建包。修复所有验证错误后重新运行打包命令。

### 第六步：迭代

测试 Skill 后，用户可能要求改进。通常这发生在使用 Skill 后，拥有 Skill 表现的新鲜上下文。

**迭代工作流：**

1. 在真实任务上使用 Skill
2. 注意困难或低效之处
3. 确定应如何更新 SKILL.md 或捆绑资源
4. 实现更改并再次测试
