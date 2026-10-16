# RelationForge 贡献指南

欢迎为 RelationForge 补充边界修正、分析流程改进、宿主兼容反馈、翻译和评估案例。两个 Skill 都应依据具体材料说明判断依据和未知，并把决定权留给当事人：`interaction-risk-analysis` 侧重诈骗、操控、胁迫、虐待和霸凌中的互动风险；`person-deep-analysis` 侧重自述、个人介绍、选取的聊天/互动材料及虚构角色的有限解读。

## 提交前

- 先搜索已有 issue/文档，说明具体场景、预期行为和当前问题。
- 改动 `skills/interaction-risk-analysis/` 或 `skills/person-deep-analysis/` 时，保持各自运行时包自包含，文件引用使用所在 Skill 目录内的相对路径，不要链接到包外。
- 两个 Skill 里内容相同的参考文件只在 `shared/common/` 修改；根目录 `LICENSE` 是许可证原文。改完后运行 `python3 scripts/sync_shared_copies.py --write`，不要手改副本。两个包里内容不同的文件留在各自目录。
- 修改任一 Skill 的分析或安全行为时，更新相关验收案例与说明；互动风险相关场景见 `evals/interaction-risk-cases.json` / `evals/interaction-risk-acceptance.md`，安全场景见 `evals/safety-scenarios.json` / `evals/safety-regression.md`。
- 诈骗和心理学术语的事实主张应有可靠来源；区分研究证据、观察线索和项目假设。不要以仓库自述或单个例子宣称有效。
- 涉及诈骗、胁迫或控制的行为边界时，检查两个 Skill 是否都优先处理当下安全与财务风险；人物解读不得替代独立核验。

## 案例隐私

只提交合成案例，或已取得明确授权且无法识别当事人的材料。默认按合成案例处理。不要提交真实私密聊天、照片、社交账号、姓名、联系方式、位置、病史或可拼接识别身份的细节。删除信息不等于匿名；若不确定，请用虚构文本重写场景。

## 验证

```sh
python3 scripts/validate_skill.py
python3 scripts/sync_shared_copies.py --check
python3 -m unittest discover -s tests -v
python3 scripts/validate_evals.py
python3 scripts/validate_safety_evals.py
python3 scripts/validate_interaction_risk_evals.py
```

评估文档用于行为复核，不是自动心理评分或效果证明。如果校验器或宿主运行与预期不符，请记录准确环境、合成输入、差异和复现步骤，不提交真实私人材料。

## Pull request 内容

请说明改了什么、为什么、影响哪些使用场景、运行了哪些检查，以及仍有哪些限制。行为规则改动应至少覆盖一个正常场景和一个容易越界的反例。
