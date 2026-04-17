"""
阶段5：生成评分表
从项目根目录的基础 rubric 复制到作者目录。未来可扩展为根据文风特征动态添加维度。
"""
import json
from pathlib import Path


def build_rubric(author_id: str, project_base: Path):
    # Base rubric path (in project root, fallback to authors if already migrated)
    base_rubric = project_base / "rubrics" / "style_rubric.json"
    if not base_rubric.exists():
        # If base was already migrated, use the author's existing one
        base_rubric = project_base / "authors" / author_id / "rubric.json"

    if not base_rubric.exists():
        raise FileNotFoundError(f"Base rubric not found at {base_rubric}")

    with open(base_rubric, "r", encoding="utf-8") as f:
        rubric = json.load(f)

    output_path = project_base / "authors" / author_id / "rubric.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rubric, f, indent=2, ensure_ascii=False)
    print(f"Built rubric for {author_id}: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build evaluation rubric for an author.")
    parser.add_argument("--author", required=True, help="Author ID (e.g., xu-tang)")
    parser.add_argument("--base", default=None, help="Project base path")
    args = parser.parse_args()

    base = Path(args.base) if args.base else Path(__file__).parent.parent
    build_rubric(args.author, base)
    print("Rubric generation completed.")


if __name__ == "__main__":
    main()
