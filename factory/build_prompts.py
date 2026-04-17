"""
阶段4：从 skill 生成 prompt 模板
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict


def build_prompt_from_skill(skill: Dict) -> str:
    section = skill["section"]
    section_display = section.replace("_", " ").title()

    lines = [
        f"你是一个学术论文写作助手。请根据以下要求撰写论文的{section_display}部分。\n",
        "【写作目标】",
    ]
    for g in skill.get("goal", []):
        lines.append(f"- {g}")

    lines.extend(["\n【结构要求】"])
    for i, s in enumerate(skill.get("structure", []), 1):
        lines.append(f"{i}. {s}")

    lines.extend(["\n【语气要求】"])
    for t in skill.get("tone", []):
        lines.append(f"- {t}")

    if skill.get("preferred_phrases"):
        lines.extend(["\n【常用句式】"])
        for p in skill["preferred_phrases"]:
            lines.append(f"- {p}")

    if skill.get("logic_pattern"):
        lines.extend(["\n【逻辑模式】"])
        for lp in skill["logic_pattern"]:
            lines.append(f"- {lp}")

    if skill.get("avoid"):
        lines.extend(["\n【禁用表达】"])
        for a in skill["avoid"]:
            lines.append(f"- {a}")

    if skill.get("constraints"):
        lines.extend(["\n【写作约束】"])
        for c in skill["constraints"]:
            lines.append(f"- {c}")

    lines.extend([
        "\n【重要提醒】",
        "1. 不要编造事实、数字、引用",
        "2. 不要引入新的实验结果",
        "3. 不要跨section写内容",
        "4. 请先输出提纲，再输出正文",
        "5. 风格要接近导师风格，但不得机械照抄原文\n",
        "【提纲格式】",
        "请先输出以下格式的提纲：",
        "1. [段落功能] 段落主要内容概述",
        "2. [段落功能] 段落主要内容概述",
        "...\n",
        "【正文格式】",
        "然后按照提纲输出完整正文。\n",
        "【输入信息】",
        f"请提供以下信息以生成更准确的{section_display}：",
        "- 论文标题：",
        "- 研究领域：",
        "- 主要方法：",
        "- 关键创新点：",
        "- 主要实验结果：",
        "- 参考文献（如有）：",
    ])

    return "\n".join(lines)


def build_all_prompts(author_id: str, project_base: Path) -> Dict[str, Dict]:
    skills_dir = project_base / "authors" / author_id / "skills"
    prompts: Dict[str, Dict] = {}

    for section in ["abstract", "introduction", "related_work", "methods", "results", "discussion", "conclusion"]:
        skill_path = skills_dir / f"skill_{section}.json"
        if not skill_path.exists():
            print(f"Warning: skill file not found: {skill_path}, skipping.")
            continue
        with open(skill_path, "r", encoding="utf-8") as f:
            skill = json.load(f)
        prompts[section] = {
            "section": section,
            "prompt_template": build_prompt_from_skill(skill)
        }
        print(f"Built prompt for {section}")

    return prompts


def save_prompts(author_id: str, project_base: Path, prompts: Dict[str, Dict]):
    output_dir = project_base / "authors" / author_id / "prompts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save combined
    combined_path = output_dir / "all_prompts.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    print(f"Saved combined prompts: {combined_path}")

    # Save per-section
    for section, prompt in prompts.items():
        path = output_dir / f"prompt_{section}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prompt, f, indent=2, ensure_ascii=False)
        print(f"Saved section prompt: {path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build prompt templates from skills for an author.")
    parser.add_argument("--author", required=True, help="Author ID (e.g., xu-tang)")
    parser.add_argument("--base", default=None, help="Project base path")
    args = parser.parse_args()

    base = Path(args.base) if args.base else Path(__file__).parent.parent
    prompts = build_all_prompts(args.author, base)
    save_prompts(args.author, base, prompts)
    print("\nPrompt generation completed.")


if __name__ == "__main__":
    main()
