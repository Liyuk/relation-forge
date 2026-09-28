# RelationForge

*Evidence-first reasoning for people, interactions, and risk*
Separate facts, behavior, and risk without labeling people.

RelationForge contains two independently installable Agent Skills that help you separate the material at hand, possible explanations, and unknowns while keeping verification and decisions with you.

| Skill | When to use it | What it does |
|---|---|---|
| `interaction-risk-analysis` | You suspect a scam, manipulation, coercion, abuse, or bullying and need to understand an interaction and immediate risks | Builds an event timeline, examines observable effects and repeated patterns, and compares evidence-based explanations; verification and response options are offered when relevant |
| `person-deep-analysis` | You want to understand a self-description, profile, selected chat or interaction excerpts, or a fictional character; you may explicitly request multiple perspectives | Separates quotes and observable behavior from limited interpretations, drawing on relevant person, relationship, narrative, or psychological lenses |

Both can address concerning relationship interactions. If someone is pressuring you for money or credentials, threatening you, or controlling your choices, address immediate financial and personal safety first. Neither Skill diagnoses a person, establishes a crime or hidden motive, or decides a relationship for you.

By default, the Skills explain the person or interaction rather than append a checklist of advice. They discuss options when you ask what to do or face an important decision; imminent payment, credential, or physical danger calls for a brief protective warning first. Missing details alone do not prove intentional concealment, and subjective motives are not assigned precise probabilities without reliable reference data.

[中文](README.md) · [Synthetic scenario demos](docs/demos/README.md) · [Acceptance cases](evals/interaction-risk-cases.json) · [Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)

## Install

Repository: <https://github.com/Liyuk/relation-forge>. Choose either Skill or install both separately.

| Skill | Codex | Claude Code |
|---|---|---|
| Interaction Risk Analysis | `npx skills add Liyuk/relation-forge --skill interaction-risk-analysis -g -a codex -y` | `npx skills add Liyuk/relation-forge --skill interaction-risk-analysis -g -a claude-code -y` |
| Person Deep Analysis | `npx skills add Liyuk/relation-forge --skill person-deep-analysis -g -a codex -y` | `npx skills add Liyuk/relation-forge --skill person-deep-analysis -g -a claude-code -y` |

## Choose a Skill

For a romance-investment offer where someone blocks company verification and demands payment tonight, use `interaction-risk-analysis`. It can lay out the timeline, separate identity claims from verified facts, explain how secrecy and urgency affect your options, and identify what to verify independently.

For a self-description, profile, selected messages, or character in a story, use `person-deep-analysis`. It identifies what the material supports, offers limited alternative interpretations, and names what remains unknown. Fictional-character conclusions stay within the work; a multi-perspective report is used only when explicitly requested.

You can ask in ordinary language or invoke either Skill explicitly:

```text
$interaction-risk-analysis
Build a timeline of this interaction. Separate quotes, claims, observed behavior, and inference; explain practical effects, plausible interpretations, counterevidence, and unknowns, then offer independently verifiable options.
```

```text
$person-deep-analysis
Separate what this material explicitly shows from possible interpretations. Give supporting evidence, reasonable alternatives, and unknowns; do not infer a real person's stable personality from a short excerpt.
```

## Shared limits

These Skills provide repeatable analysis methods, not automatic detection, psychological testing, clinical diagnosis, legal findings, investigation, bank fraud control, or fund recovery. Limited text cannot establish a complete personality, criminal conduct, or subjective intent. Psychological lenses are prompts for questions and limited interpretations. For urgent safety, account, or payment risks, take practical protective steps and verify through official channels you find yourself. Share only the excerpts needed for your question; remove unnecessary names, account details, contact information, and full private chats. Data handling depends on the host platform.

## Scenarios and checks

The [synthetic scenario demos](docs/demos/README.md) illustrate event analysis, alternative explanations, evidence updates, and safety options; they do not establish real-world accuracy. Contributors can check the repository's acceptance cases and behavior boundaries with:

```sh
python3 scripts/validate_skill.py
python3 scripts/validate_evals.py
python3 scripts/validate_safety_evals.py
python3 scripts/validate_interaction_risk_evals.py
python3 scripts/check_skill_discovery.py
python3 scripts/check_skill_installation.py
```

License: MIT.
