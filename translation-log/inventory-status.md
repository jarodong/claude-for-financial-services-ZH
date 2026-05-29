# 金融套件中文化 · 全量盘点表

**日期**:2026-05-27
**执行人**:李向东 + Claude Code
**方法**:中英双版本逐文件比对

---

## 一、总览

| 指标 | 数值 |
|---|---|
| 英文原版总文件数 | ~250+ |
| 中文版已存在文件数 | ~230+ |
| 已翻译(markdown/含中文) | ~200+ |
| 缺失文件(需翻译) | **0** ✅ 已全部补完 |
| 部分翻译(需补完) | **0** ✅ 已全部补完 |
| 缺失文件(代码/脚本,无需翻译) | 21 |
| 缺失文件(基础设施,可选) | 6 |
| 整体翻译覆盖率 | **~98%** |

---

## 二、需要处理的文件(按优先级)

### ~~P0 · 缺失文件(必须补)~~ ✅ 已完成

| 文件 | 位置 | 状态 |
|---|---|---|
| `report-template.md` | `vertical-plugins/equity-research/skills/initiating-coverage/assets/` | ✅ 2026-05-27 全文翻译完成 |

### ~~P1 · 部分翻译(需补完正文)~~ ✅ 已完成

| 文件 | 位置 | 状态 |
|---|---|---|
| `proposal.md` | `vertical-plugins/wealth-management/commands/` | ✅ 2026-05-27 正文补译完成 |
| `rebalance.md` | `vertical-plugins/wealth-management/commands/` | ✅ 2026-05-27 正文补译完成 |
| `tlh.md` | `vertical-plugins/wealth-management/commands/` | ✅ 2026-05-27 正文补译完成 |

### P2 · 未做语义评审的初译文件(已翻译但未核对术语)

#### Agent 主提示词(7 个未评审)

| Agent | 路径 | 说明 |
|---|---|---|
| earnings-reviewer | `agent-plugins/earnings-reviewer/agents/` | 已初译,未做术语评审 |
| market-researcher | `agent-plugins/market-researcher/agents/` | 同上 |
| meeting-prep-agent | `agent-plugins/meeting-prep-agent/agents/` | 同上 |
| model-builder | `agent-plugins/model-builder/agents/` | 同上 |
| month-end-closer | `agent-plugins/month-end-closer/agents/` | 同上 |
| pitch-agent | `agent-plugins/pitch-agent/agents/` | 同上 |
| statement-auditor | `agent-plugins/statement-auditor/agents/` | 同上 |

#### subagents YAML(30+ 个,全部未评审)

每个 Agent 有 3 个 subagents,共 30 个 YAML 文件。这些是真正执行任务的叶子节点,包含 system prompt 等关键文本。**全部未做语义评审。**

| Agent | subagents |
|---|---|
| earnings-reviewer | transcript-reader, model-updater, note-writer |
| gl-reconciler | reader, critic, resolver |
| kyc-screener | doc-reader, escalator, rules-engine |
| market-researcher | comps-spreader, note-writer, sector-reader |
| meeting-prep-agent | news-reader, pack-writer, profiler |
| model-builder | auditor, builder, data-puller |
| month-end-closer | ledger-reader, poster, rollforward |
| pitch-agent | deck-writer, modeler, researcher |
| statement-auditor | flagger, reconciler, statement-reader |
| valuation-reviewer | package-reader, publisher, valuation-runner |

#### vertical-plugins Skills(SKILL.md,全部未做语义评审)

| 垂直领域 | Skill 数量 | 状态 |
|---|---|---|
| financial-analysis | 14 | 已初译,未评审 |
| equity-research | 10 | 已初译,未评审 |
| investment-banking | 10 | 已初译,未评审 |
| private-equity | 10 | 已初译,未评审 |
| wealth-management | 6 | 已初译,未评审 |
| fund-admin | 6 | 已初译,未评审 |
| operations | 2 | 已初译,未评审 |

---

## 三、无需处理的文件

| 类别 | 文件数 | 说明 |
|---|---|---|
| 代码脚本(.py/.sh/.mjs/.ps1) | ~15 | 无需翻译 |
| 配置文件(.json/.mcp.json/hooks.json) | ~25 | 无可翻译文本 |
| LICENSE/.txt | ~10 | 法律文本,不翻译 |
| partner-built(LSEG/S&P Global) | 36 | 按 README 说明,国内不使用,已跳过 |
| 基础设施(.gitignore/.githooks/.github/) | 6 | 可选,不影响运行 |

---

## 四、语义评审完成度(与翻译覆盖度的区别)

**翻译覆盖率 ~98%** 只代表"有中文",不代表"中文对"。

昨天 Phase 5A 只做了 3 个 Agent 主提示词的术语精修(10 处修正),说明初译存在明显业务术语偏差。

**真正的风险在三层未评审的叶子节点:**

| 层级 | 文件数 | 评审状态 | 风险等级 |
|---|---|---|---|
| Agent 主提示词 | 10 | 3 个已评审,7 个未评审 | 中 |
| subagents YAML | 30 | **全部未评审** | 高 |
| vertical-plugins Skills | 58 | **全部未评审** | 高 |
| vertical-plugins Commands | ~40 | **全部未评审** | 中 |
| managed-agent-cookbooks README | 10 | 已初译,未评审 | 低 |
| steering-examples.json | 10 | JSON,不需要评审 | 无 |

---

## 五、关键判断

1. **翻译广度已到位**:所有 markdown 文件都有中文版,覆盖率 ~98%。
2. **翻译深度严重不足**:真正决定运行效果的 subagents 和 Skill 层,全部只做了初译,没有一个经过术语评审。
3. **唯一的结构缺失**:`report-template.md` 需要补译。
4. **3 个 command 需要补完正文**:wealth-management 的 proposal/rebalance/tlh。

**结论**:盘点印证了昨天的判断——"10 个主提示词都译完了"是进度假象。下一步要么横向铺评审(方案 A),要么纵向打通一个 Agent(方案 B),取决于你的优先级。
