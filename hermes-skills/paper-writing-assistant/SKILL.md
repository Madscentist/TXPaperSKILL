---
name: paper-writing-assistant
description: Central hub for academic paper writing with selectable author styles. Use when the user asks to write, revise, evaluate, or distill any section of an academic paper.
---

# Paper Writing Assistant

Use this skill as the central controller whenever the user wants to draft, revise, evaluate, or distill an academic paper section in a specific author's writing style.

## Capabilities
- **Write**: Draft a specific section using a selected author's style.
- **Revise**: Rewrite an existing section to match a selected author's style.
- **Evaluate**: Score a section against the author's style rubric.
- **Distill**: Run the factory pipeline to create a new author style from PDFs.

## Project Base Path

The PaperSkill project is located at:
- WSL: `/mnt/g/project/PaperSkill/`
- Windows: `G:\project\PaperSkill\`

All operations must load `registry.json` from the project base first.

## Workflow

### Step 1: Determine Intent
Parse the user's request into one of:
- `write`
- `revise`
- `evaluate`
- `distill`

If unclear, ask: "你是想写/改/评某个 section，还是蒸馏新文风？"

### Step 2: Determine Author
1. Load `registry.json` from the project base.
2. Check if the user explicitly mentions an author name or ID.
   - Known aliases: "唐旭" → `xu-tang`, "Xu Tang" → `xu-tang`.
3. If no author is specified, use `registry.json["default_author"]`.
4. Validate that the author exists in `registry.json["authors"]`.
   - If not found, list available authors and ask the user to choose.

### Step 3: Determine Section
Attempt to infer the section from the user's message. Supported mappings:

| Section | Keywords |
|---------|----------|
| abstract | abstract, 摘要 |
| introduction | introduction, 引言, 简介 |
| related_work | related work, 相关工作, 文献综述 |
| methods | methods, 方法, 方法论 |
| results | results, 结果, 实验结果 |
| discussion | discussion, 讨论 |
| conclusion | conclusion, 结论, 总结 |

If multiple sections are mentioned, ask which one to proceed with.
If no section is detected and intent is `write`/`revise`/`evaluate`, ask: "请告诉我你要处理的 section（如 introduction / methods / results 等）。"

### Step 4: Load Assets
For the resolved `(author, section)` pair, load:
- Skill rules: `authors/<author_id>/skills/skill_<section>.json`
- Prompt template: `authors/<author_id>/prompts/prompt_<section>.json`
- Rubric (for evaluate): `authors/<author_id>/rubric.json`

If files are missing, fall back to the author-style sub-skill references:
- `hermes-skills/author-styles/<author_id>-paper-style/references/section-skills.md`
- `hermes-skills/author-styles/<author_id>-paper-style/references/prompts-and-rubric.json`

### Step 5a: Write / Revise
1. Summarize the user's provided facts, figures, tables, and claims.
2. If facts are insufficient, mark missing items instead of inventing them.
3. Build a short outline following the loaded skill's `structure` and `logic_pattern`.
4. Output the outline first, then the draft.
5. For revise tasks, highlight what was changed to match the author's style.

### Step 5b: Evaluate
1. Load the rubric JSON.
2. Score the provided text across the 6 dimensions (1-5 scale).
3. Compute the average score.
4. Provide specific improvement suggestions for any dimension scoring ≤3.

### Step 5c: Distill

When the user asks to distill a new author style, use the **two-phase workflow** below. Hermes acts as the LLM for the enrichment phase; no external LLM API configuration is required.

#### Phase 1: Skeleton Generation (terminal)
1. Ask the user for the new author's ID, display name, and domain.
2. Verify that `authors/<new_id>/papers/` contains PDFs or extracted text files.
3. If the aggregation report does not exist yet, instruct the user to run their existing analysis scripts first (e.g., place extracted texts in `authors/<new_id>/extracted_texts/` and run the analyzer).
4. Run the skeleton pipeline:
   ```bash
   python factory/run_pipeline.py --author <new_id> --no-llm
   ```
   This generates stable skill skeletons, prompts, rubric, and Hermes references without LLM enrichment.

#### Phase 2: Hermes Enrichment (Hermes direct)
5. For each of the 7 sections, load:
   - `authors/<new_id>/analysis/aggregation_report.json`
   - `authors/<new_id>/skills/skill_<section>.json`
6. Read the relevant parts of the aggregation report (surface style, syntactic style, rhetorical structure for the section, academic stance).
7. **Use your own reasoning to generate**:
   - `preferred_phrases`: 5-8 complete sentence templates or starter phrases reflecting the author's style
   - `logic_pattern`: 1-3 strings describing the rhetorical flow
8. Write the enriched fields back into each `skill_<section>.json`.

#### Phase 3: Rebuild (terminal)
9. Run:
   ```bash
   python factory/rebuild_after_enrich.py --author <new_id>
   ```
   This rebuilds prompts, rubric, and Hermes references from the enriched skills.

#### Phase 4: Registry Update
10. Append the author metadata to `registry.json["authors"]`.
11. If the user says "设为默认" or "set as default", update `registry.json["default_author"]`.

**Example request:** "我想蒸馏一个新导师的风格，论文已经放在 authors/prof-li/papers/ 里了。"
- Response: "好的。请告诉我这位导师的显示名称和研究领域（例如 prof-li / 计算机视觉）。接下来我会先跑骨架脚本，然后由我直接为每个 section 填充文风特征，最后同步生成 prompts 和 references。"

## Output Discipline for Drafting

1. **Outline first**: Always present the section outline before the body text.
2. **No hallucination**: Do not invent citations, datasets, numbers, or code links.
3. **Section fidelity**: Do not write content belonging to other sections.
4. **Style proximity**: Match rhetoric, progression, and claim strength; do not copy source wording verbatim.
5. **Missing info**: If critical inputs are absent, explicitly list them as `[待补充: ...]` instead of filling them in.

## Registry Update Rule

Whenever a new author style is successfully distilled:
- Append the author metadata to `registry.json["authors"]`.
- If the user says "设为默认" or "set as default", update `registry.json["default_author"]`.

## Example Interactions

**User**: "用唐旭老师的风格帮我写 Introduction，关于遥感变化检测的。"
→ Intent: write, Author: xu-tang, Section: introduction. Load skill, ask for facts if missing, then output outline + draft.

**User**: "把这段 results 改成唐旭风格。"
→ Intent: revise, Author: xu-tang, Section: results. Load skill, rewrite, highlight changes.

**User**: "评估一下这段 abstract 符不符合唐旭的风格。"
→ Intent: evaluate, Author: xu-tang, Section: abstract. Load rubric, score, give feedback.

**User**: "我想蒸馏一个新导师的风格，论文已经放在 authors/prof-li/papers/ 里了。"
→ Intent: distill, Author ID: prof-li. Run pipeline, update registry.
