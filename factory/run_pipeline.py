"""
一键跑完整个 PaperSkill 工厂流程：
analysis → generate_skill → build_prompts → build_rubric

使用方法：
    python factory/run_pipeline.py --author xu-tang
    可选：
    --no-llm    跳过 LLM 增强，仅使用回落值
    --base      指定项目根路径
"""
import sys
import argparse
from pathlib import Path

# Make factory modules importable
sys.path.insert(0, str(Path(__file__).parent))

from generate_skill import SkillGenerator
from build_prompts import build_all_prompts, save_prompts
from build_rubric import build_rubric
from compile_hermes_references import compile_references


def run_pipeline(author_id: str, use_llm: bool = True, base: Path = None):
    if base is None:
        base = Path(__file__).parent.parent

    print(f"=" * 60)
    print(f"PaperSkill Factory Pipeline")
    print(f"Author : {author_id}")
    print(f"Use LLM: {use_llm}")
    print(f"Base   : {base}")
    print(f"=" * 60)

    # Step 3: Generate skills
    print("\n[Step 1/3] Generating section skills...")
    generator = SkillGenerator(author_id, project_base=str(base))
    skills = generator.generate_all_skills(use_llm=use_llm)
    generator.save_skills(skills)

    # Step 4: Build prompts
    print("\n[Step 2/3] Building prompt templates...")
    prompts = build_all_prompts(author_id, base)
    save_prompts(author_id, base, prompts)

    # Step 5: Build rubric
    print("\n[Step 3/4] Building evaluation rubric...")
    build_rubric(author_id, base)

    # Step 6: Compile Hermes references
    print("\n[Step 4/4] Compiling Hermes skill references...")
    compile_references(author_id, base)

    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print(f"Author assets: {base / 'authors' / author_id}")
    print(f"Hermes skill : {base / 'hermes-skills' / 'author-styles' / (author_id + '-paper-style')}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Run the full PaperSkill factory pipeline for an author.")
    parser.add_argument("--author", required=True, help="Author ID (e.g., xu-tang)")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM enrichment")
    parser.add_argument("--base", default=None, help="Project base path")
    args = parser.parse_args()

    base = Path(args.base) if args.base else None
    run_pipeline(args.author, use_llm=not args.no_llm, base=base)


if __name__ == "__main__":
    main()
