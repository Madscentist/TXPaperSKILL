"""
在 Hermes 完成 skill 的 LLM 增强后，一键重新生成 prompts、rubric 和 Hermes references。

使用方法：
    python factory/rebuild_after_enrich.py --author xu-tang
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from build_prompts import build_all_prompts, save_prompts
from build_rubric import build_rubric
from compile_hermes_references import compile_references


def rebuild(author_id: str, base: Path = None):
    if base is None:
        base = Path(__file__).parent.parent

    print(f"Rebuilding assets for {author_id}...")

    print("\n[1/3] Building prompt templates from enriched skills...")
    prompts = build_all_prompts(author_id, base)
    save_prompts(author_id, base, prompts)

    print("\n[2/3] Building evaluation rubric...")
    build_rubric(author_id, base)

    print("\n[3/3] Compiling Hermes skill references...")
    compile_references(author_id, base)

    print("\n" + "=" * 60)
    print("Rebuild completed successfully!")
    print(f"Updated assets: {base / 'authors' / author_id}")
    print(f"Hermes skill : {base / 'hermes-skills' / 'author-styles' / (author_id + '-paper-style')}")
    print("=" * 60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Rebuild prompts, rubric, and Hermes references after manual enrichment.")
    parser.add_argument("--author", required=True, help="Author ID (e.g., xu-tang)")
    parser.add_argument("--base", default=None, help="Project base path")
    args = parser.parse_args()

    base = Path(args.base) if args.base else None
    rebuild(args.author, base)


if __name__ == "__main__":
    main()
