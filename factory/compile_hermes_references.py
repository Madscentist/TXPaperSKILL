"""
阶段6：将 authors/<author_id>/ 下的技能、提示和评分表
编译为 hermes-skills/author-styles/<author_id>-paper-style/references/ 下的引用文件。
"""
import json
from pathlib import Path


def compile_references(author_id: str, project_base: Path):
    author_dir = project_base / "authors" / author_id
    skill_dir = author_dir / "skills"
    prompt_dir = author_dir / "prompts"
    rubric_path = author_dir / "rubric.json"

    ref_dir = project_base / "hermes-skills" / "author-styles" / f"{author_id}-paper-style" / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Compile section-skills.md
    lines = [f"# Section Skills: {author_id}\n"]
    for section in ["abstract", "introduction", "related_work", "methods", "results", "discussion", "conclusion"]:
        skill_path = skill_dir / f"skill_{section}.json"
        if not skill_path.exists():
            continue
        with open(skill_path, "r", encoding="utf-8") as f:
            skill = json.load(f)
        lines.append(f"## {section}\n")
        lines.append(f"```json\n{json.dumps(skill, indent=2, ensure_ascii=False)}\n```\n")

    with open(ref_dir / "section-skills.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Compiled {ref_dir / 'section-skills.md'}")

    # Compile prompts-and-rubric.json
    prompts_and_rubric = {"prompts": {}, "rubric": {}}
    for section in ["abstract", "introduction", "related_work", "methods", "results", "discussion", "conclusion"]:
        prompt_path = prompt_dir / f"prompt_{section}.json"
        if prompt_path.exists():
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompts_and_rubric["prompts"][section] = json.load(f)

    if rubric_path.exists():
        with open(rubric_path, "r", encoding="utf-8") as f:
            prompts_and_rubric["rubric"] = json.load(f)

    with open(ref_dir / "prompts-and-rubric.json", "w", encoding="utf-8") as f:
        json.dump(prompts_and_rubric, f, indent=2, ensure_ascii=False)
    print(f"Compiled {ref_dir / 'prompts-and-rubric.json'}")

    # Create SKILL.md scaffold if it does not exist
    skill_md = ref_dir.parent / "SKILL.md"
    if not skill_md.exists():
        content = f"""---
name: {author_id}-paper-style
description: Distill and apply the section-specific academic writing style for author '{author_id}'. Use when drafting, revising, or evaluating paper sections in this style.
---

# {author_id.replace('-', ' ').title()} Paper Style

Use this skill to draft, revise, or evaluate academic paper sections in a style distilled from the author's papers. Apply it only from user-provided research facts, data, figures, tables, citations, and section goals. Do not invent facts, numbers, citations, datasets, code links, or author intent.

## Workflow

1. Identify the target section: abstract, introduction, related work, methods, results, discussion, or conclusion.
2. Load the relevant section rules from `references/section-skills.md`.
3. If drafting or revising, load the matching prompt template from `references/prompts-and-rubric.json`.
4. Build a short outline first, then write the section.
5. Verify that every technical claim is supported by the user input.
6. Evaluate the output with the rubric in `references/prompts-and-rubric.json` when quality control is requested.

## Required Output Discipline

For drafting tasks:

1. Output a section-level outline first.
2. Output the draft second.
3. Use only supplied factual content.
4. Mark missing required information instead of filling it in.
5. Keep the style close at the level of rhetoric, section progression, and claim strength; do not imitate source wording verbatim.

## References

- `references/section-skills.md`: full section-specific skill rules.
- `references/prompts-and-rubric.json`: prompt templates and style rubric.
"""
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created scaffold {skill_md}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compile Hermes skill references for an author.")
    parser.add_argument("--author", required=True, help="Author ID (e.g., xu-tang)")
    parser.add_argument("--base", default=None, help="Project base path")
    args = parser.parse_args()

    base = Path(args.base) if args.base else Path(__file__).parent.parent
    compile_references(args.author, base)
    print("Hermes references compilation completed.")


if __name__ == "__main__":
    main()
