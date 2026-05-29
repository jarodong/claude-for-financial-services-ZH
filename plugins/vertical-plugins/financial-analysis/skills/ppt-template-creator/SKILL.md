---
name: ppt-template-creator
description: 从用户提供的 PowerPoint 模板创建自包含的 PPT 模板 SKILL（不是演示文稿）。仅当用户想从模板创建可复用 Skill 时使用。创建实际演示文稿请使用 pptx Skill。
---

# PPT 模板创建器

**此 Skill 创建 SKILL，不是演示文稿。** 当用户想把 PowerPoint 模板变成可复用 Skill（以后能生成演示文稿）时使用。如果用户只想创建演示文稿，使用 `pptx` Skill。

生成的 Skill 包含：
- `assets/template.pptx` —— 模板文件
- `SKILL.md` —— 完整指令（无需引用此元 Skill）

**通用 Skill 构建最佳实践**，参见 `skill-creator` Skill。此 Skill 聚焦 PPT 特定模式。

## 工作流

1. **用户提供模板**（.pptx 或 .potx）
2. **分析模板** —— 提取布局、占位符、尺寸
3. **初始化 Skill** —— 使用 `skill-creator` Skill 建立 Skill 结构
4. **添加模板** —— 将 .pptx 复制到 `assets/template.pptx`
5. **编写 SKILL.md** —— 按以下模板填写 PPT 特定细节
6. **创建示例** —— 生成示例演示文稿进行验证
7. **打包** —— 使用 `skill-creator` Skill 打包为 .skill 文件

## 第 2 步：分析模板

**关键：提取精确的占位符位置** —— 这决定内容区域边界。

```python
from pptx import Presentation

prs = Presentation(template_path)
print(f"尺寸: {prs.slide_width/914400:.2f}\" x {prs.slide_height/914400:.2f}\"")
print(f"布局数: {len(prs.slide_layouts)}")

for idx, layout in enumerate(prs.slide_layouts):
    print(f"\n[{idx}] {layout.name}:")
    for ph in layout.placeholders:
        try:
            ph_idx = ph.placeholder_format.idx
            ph_type = ph.placeholder_format.type
            # 重要：提取精确位置（英寸）
            left = ph.left / 914400
            top = ph.top / 914400
            width = ph.width / 914400
            height = ph.height / 914400
            print(f"    idx={ph_idx}, type={ph_type}")
            print(f"        x={left:.2f}\", y={top:.2f}\", w={width:.2f}\", h={height:.2f}\"")
        except:
            pass
```

**需记录的关键尺寸：**
- **标题位置**：标题占位符在哪里？
- **副标题/描述**：副标题行在哪里？
- **页脚占位符**：页脚/来源出现在哪里？
- **内容区域**：副标题和页脚之间的空间是内容区域

### 找到真正的内容起始位置

**关键：** 内容区域并不总是在副标题占位符后立即开始。许多模板在副标题和内容区域之间有视觉边框、线条或保留空间。

**最佳方法：** 查看 Layout 2 或类似的"内容"布局，其中有一个 OBJECT 占位符——该占位符的 `y` 位置指示内容实际应从哪里开始。

```python
# 找到 OBJECT 占位符以确定真正的内容起始位置
for idx, layout in enumerate(prs.slide_layouts):
    for ph in layout.placeholders:
        try:
            if ph.placeholder_format.type == 7:  # OBJECT 类型
                top = ph.top / 914400
                print(f"Layout [{idx}] {layout.name}: OBJECT 起始于 y={top:.2f}\"")
                # 这个 y 值就是内容应开始的位置！
        except:
            pass
```

**示例：** 模板可能有：
- 副标题结束于 y=1.38"
- 但 OBJECT 占位符起始于 y=1.90"
- 间隔（0.52"）保留给边框/线条——**不要在此放置内容**

使用 OBJECT 占位符的 `y` 位置作为内容起始，而非副标题的结束位置。

## 第 5 步：编写 SKILL.md

生成的 Skill 应有此结构：
```
[公司]-ppt-template/
├── SKILL.md
└── assets/
    └── template.pptx
```

### 生成的 SKILL.md 模板

生成的 SKILL.md 必须**自包含**，所有指令嵌入。使用此模板，用分析结果填写括号值：

````markdown
---
name: [公司]-ppt-template
description: [公司] PowerPoint 模板，用于创建演示文稿。创建 [公司] 品牌 Pitch Deck、董事会材料或客户演示时使用。
---

# [公司] PPT 模板

模板：`assets/template.pptx`（[宽]" x [高]"，[N] 个布局）

## 创建演示文稿

```python
from pptx import Presentation

prs = Presentation("path/to/skill/assets/template.pptx")

# 先删除所有现有幻灯片
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[0]

# 从布局添加幻灯片
slide = prs.slides.add_slide(prs.slide_layouts[布局索引])
```

## 关键布局

| 索引 | 名称 | 用途 |
|------|------|------|
| [0] | [布局名称] | [封面/标题幻灯片] |
| [N] | [布局名称] | [含要点的内容] |
| [N] | [布局名称] | [双栏布局] |

## 占位符映射

**关键：包含每个占位符的精确位置（x, y 坐标）。**

### 布局 [N]：[名称]
| idx | 类型 | 位置 | 用途 |
|-----|------|------|------|
| [idx] | TITLE (1) | y=[Y]" | 幻灯片标题 |
| [idx] | BODY (2) | y=[Y]" | 副标题/描述 |
| [idx] | BODY (2) | y=[Y]" | 页脚 |
| [idx] | BODY (2) | y=[Y]" | 来源/备注 |

### 内容区域边界

**记录自定义形状/表格/图表的安全内容区域：**

```
内容区域（用于布局 [N]）：
- 左边距：[X]"（内容从此开始）
- 顶部：[Y]"（副标题占位符下方）
- 宽度：[W]"
- 高度：[H]"（页脚前结束）

四象限布局：
- 左列：x=[X]"，宽=[W]"
- 右列：x=[X]"，宽=[W]"
- 上行：y=[Y]"，高=[H]"
- 下行：y=[Y]"，高=[H]"
```

**为什么重要：** 自定义内容（文本框、表格、图表）必须保持在这些边界内，以避免与模板占位符（标题、页脚、来源行）重叠。

## 填充内容

**不要手动添加要点字符** —— 幻灯片母版处理格式。

```python
# 填充标题
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        if shape.placeholder_format.type == 1:  # TITLE
            shape.text = "幻灯片标题"

# 填充带层级的内容（level 0 = 标题，level 1 = 要点）
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == [内容索引]:
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()

            content = [
                ("章节标题", 0),
                ("第一个要点", 1),
                ("第二个要点", 1),
            ]

            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```

## 示例：封面幻灯片

```python
slide = prs.slides.add_slide(prs.slide_layouts[[封面索引]])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        idx = shape.placeholder_format.idx
        if idx == [标题索引]:
            shape.text = "公司名称"
        elif idx == [副标题索引]:
            shape.text = "演示标题 | 日期"
```

## 示例：内容幻灯片

```python
slide = prs.slides.add_slide(prs.slide_layouts[[内容索引]])
for shape in slide.shapes:
    if hasattr(shape, 'placeholder_format'):
        ph_type = shape.placeholder_format.type
        idx = shape.placeholder_format.idx
        if ph_type == 1:
            shape.text = "执行摘要"
        elif idx == [正文索引]:
            tf = shape.text_frame
            for para in tf.paragraphs:
                para.clear()
            content = [
                ("关键发现", 0),
                ("收入同比增长 40% 至 5000万元", 1),
                ("扩展至 3 个新市场", 1),
                ("建议", 0),
                ("推进战略举措", 1),
            ]
            tf.paragraphs[0].text = content[0][0]
            tf.paragraphs[0].level = content[0][1]
            for text, level in content[1:]:
                p = tf.add_paragraph()
                p.text = text
                p.level = level
```
````

## 第 6 步：创建示例输出

生成示例演示文稿以验证 Skill 有效。保存在 Skill 旁边供参考。

## 生成 Skill 的 PPT 特定规则

1. **模板在 assets/** —— 始终打包 .pptx 文件
2. **自包含 SKILL.md** —— 所有指令嵌入，无外部引用
3. **无手动要点** —— 使用 `paragraph.level` 建立层级
4. **先删除幻灯片** —— 添加新幻灯片前始终清除现有幻灯片
5. **按 idx 记录占位符** —— 占位符 idx 值是模板特定的
