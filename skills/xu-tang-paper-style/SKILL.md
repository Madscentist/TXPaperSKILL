---
name: xu-tang-paper-style
description: Distill and apply Xu Tang's section-specific academic writing style for remote sensing papers. Use when drafting, revising, evaluating, or converting paper sections into reusable prompts or style rules based on provided facts and evidence.
---

# Xu Tang Paper Style

Use this skill to draft, revise, or evaluate academic paper sections in a style distilled from Xu Tang's recent first-author remote sensing papers. Apply it only from user-provided research facts, data, figures, tables, citations, and section goals. Do not invent facts, numbers, citations, datasets, code links, or author intent.

## Evidence Status

Treat the style model as evidence-weighted:

- High confidence: abstract structure, problem-to-module mapping, conservative experimental claims.
- Medium-high confidence: introduction structure and contribution framing.
- Medium confidence: methods and results narration.
- Low-medium confidence: discussion, because some accessible papers merge discussion into results.

When evidence is insufficient for a section, still produce a conservative draft and explicitly avoid unsupported specifics.

## Global Style

Write in a stable, engineering-oriented academic tone:

- Start from remote sensing task value, then move to specific limitations.
- Acknowledge existing methods before identifying gaps.
- Map each gap to a method component.
- Explain modules by their role, not by promotional language.
- Close claims with experiments, ablations, or clearly marked expected validation.
- Prefer restrained verbs: propose, design, develop, introduce, demonstrate, verify, indicate.
- Prefer hedged interpretation for explanations: may, could, possibly, suggests, indicates.

Avoid:

- Marketing or absolute claims such as revolutionary, perfect, completely solve, universally applicable.
- Unsupported "state-of-the-art" or "significant improvement".
- New references, datasets, formulas, metrics, or code links not supplied by the user.
- Mechanical copying from source papers.

## Workflow

1. Identify the target section: abstract, introduction, related work, methods, results, discussion, or conclusion.
2. Load only the relevant section rules from `references/section-skills.md`.
3. If drafting or revising, load the matching prompt template from `references/prompts-and-rubric.json`.
4. Build a short outline first, then write the section.
5. Verify that every technical claim is supported by the user input.
6. Evaluate the output with the rubric in `references/prompts-and-rubric.json` when quality control is requested.

## Section Selection

- Use `skill_abstract` for one-paragraph summaries that connect task, limitation, method, modules, and experiments.
- Use `skill_introduction` for background-to-gap-to-contribution progression.
- Use `skill_related_work` for taxonomy-based literature organization.
- Use `skill_methods` for framework, notation, module, and loss descriptions.
- Use `skill_results` for experimental settings, comparisons, ablations, and visual/efficiency analysis.
- Use `skill_discussion` for result interpretation, applicability, limitations, and future work.
- Use `skill_conclusion` for compact method and evidence recap.

## Required Output Discipline

For drafting tasks:

1. Output a section-level outline first.
2. Output the draft second.
3. Use only supplied factual content.
4. Mark missing required information instead of filling it in.
5. Keep the style close at the level of rhetoric, section progression, and claim strength; do not imitate source wording verbatim.

For style analysis tasks:

1. Separate high-confidence findings from unstable findings.
2. Identify paragraph functions, such as background, gap, method overview, result report, comparison, limitation, or contribution summary.
3. Convert observations into executable rules.

## References

- `references/section-skills.md`: full section-specific skill rules.
- `references/prompts-and-rubric.json`: example-library schema, prompt templates, and style rubric.
