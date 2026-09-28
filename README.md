# RelationForge

*Evidence-first reasoning for people, interactions, and risk*
拆事实，看言行，辨风险，不替人定性。

RelationForge 包含两个可独立安装的 Agent Skill，帮助你把具体材料、可能解释和未知分开，并保留自己核验与决定的空间。

当一段聊天让你觉得不对劲，却又说不清问题在哪；当你想理解一份自述，却不想让 AI 凭几句话给人贴标签——可以把相关材料交给它一起梳理。它会指出材料实际支持什么、还有哪些解释，以及哪些事仍然未知。

| Skill | 适合何时使用 | 主要做什么 |
|---|---|---|
| `interaction-risk-analysis`（互动风险识别与解构） | 怀疑诈骗、操控、胁迫、虐待或霸凌，需要梳理互动过程和眼前风险 | 按时间拆解事件、行为效果、信息缺口与诱导动作，比较有依据的解释；应对与核验按需展开 |
| `person-deep-analysis`（人际深度解析） | 想理解自述、个人介绍、征友贴、选取的聊天/互动材料或虚构角色，或明确需要多视角解读 | 区分自我呈现、实际行动、利益流向与有限的候选解释；按材料选用人物、关系、叙事或心理学视角 |

两者都可以处理关系中的可疑互动。若正在被催款、索取凭证、威胁或控制，先处理现实安全和财务风险；不要让人物解读拖延止损。两者都不诊断人格、确认犯罪或隐藏动机，也不替用户决定关系走向。

默认先回答“这人/这段互动怎么看”，不把建议清单当固定结尾。用户问“怎么办”或正面临重要决定时再讨论可选做法；迫近的转账、凭证或人身风险则先简短止损。分析未提及的信息时，“没写”不等于“故意隐瞒”；没有可靠基准数据，不报看似精确的动机概率。

[English](README_EN.md) · [合成场景演示](docs/demos/README.md) · [验收场景](evals/interaction-risk-cases.json) · [贡献指南](CONTRIBUTING.md) · [MIT License](LICENSE)

## 看一个例子

**合成对话：**“今晚把钱转进这个平台，别告诉朋友。错过就没机会；不相信我就是不爱我。”

`interaction-risk-analysis` 会先指出这段话里能直接看到的行为：限时催款、要求保密、阻止外部核实，并把付款和感情绑定。它会解释这些做法怎样压缩独立判断的空间，同时说明：仅凭这句话，还不能核实对方身份或断定其真实动机。你可以先暂停转账，再通过自己找到的官方渠道核验平台和收款方。

**即使还不能确定对方的动机，你也可以先保护自己的钱。**[更多合成场景](docs/demos/README.md)

## 选择并试用

如果一位网恋对象提出投资、阻止你核实公司并催促当晚转账，使用 `interaction-risk-analysis`：它会还原事件顺序，区分身份主张和已核实事实，说明限制核验、保密和催款如何形成风险；迫近付款时先简短提示暂停，再按问题展开核验。

如果你想理解一段自述、个人介绍或几段聊天呈现了哪些需求、选择与互动特点，使用 `person-deep-analysis`：它会依据材料提出有限的候选解释，保留反例和未知；分析虚构角色时，结论只涉及作品如何呈现角色。只有你明确要求时，才展开多视角报告。

两个 Skill 均可直接用自然语言提出问题，也可显式调用：

```text
$interaction-risk-analysis
请按时间拆解这些互动，分清原话、事实主张、可观察行为和推断；说明行为效果、可能解释、反证与未知，并给我可独立核验的选择。
```

```text
$person-deep-analysis
请根据这段材料区分明确表达的内容和可能解释，指出依据、合理替代解释与未知；不要用有限片段给现实人物定型。
```

## 安装

仓库地址：<https://github.com/Liyuk/relation-forge>。按需要选择一个或两个 Skill，分别安装。

| Skill | Codex | Claude Code |
|---|---|---|
| 互动风险识别与解构 | `npx skills add Liyuk/relation-forge --skill interaction-risk-analysis -g -a codex -y` | `npx skills add Liyuk/relation-forge --skill interaction-risk-analysis -g -a claude-code -y` |
| 人际深度解析 | `npx skills add Liyuk/relation-forge --skill person-deep-analysis -g -a codex -y` | `npx skills add Liyuk/relation-forge --skill person-deep-analysis -g -a claude-code -y` |

## 共同边界

Skill 提供可复用的分析方法，不是自动检测器、心理测验、临床诊断、法律裁决、侦查、银行风控或资金追回服务。有限文本不能证明完整人格、犯罪事实或主观动机；心理学视角只用于提出问题和有限解释。遇到迫近的人身、账户或资金风险，先采取现实中的安全措施，并通过自己找到的官方渠道核验。只提供回答问题所需的最少材料，移除不必要的姓名、账号、联系方式和完整私聊；数据如何处理取决于所用宿主平台。

## 场景与检查

[合成场景演示](docs/demos/README.md)展示事件拆解、替代解释、反证更新和安全选择；示例不等于真实世界准确率验证。仓库中的验收案例与检查脚本供贡献者复核行为边界：

```sh
python3 scripts/validate_skill.py
python3 scripts/validate_evals.py
python3 scripts/validate_safety_evals.py
python3 scripts/validate_interaction_risk_evals.py
python3 scripts/check_skill_discovery.py
python3 scripts/check_skill_installation.py
```

许可证：MIT。
