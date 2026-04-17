"""
阶段3：通用写作 SKILL 生成器（混合模式）
- 骨架（goal/structure/tone/avoid/constraints）使用硬编码模板保证稳定
- preferred_phrases 和 logic_pattern 从 aggregation_report.json 经 LLM 提取后动态注入
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# Ensure factory modules are importable
sys.path.insert(0, str(Path(__file__).parent))
from llm_client import llm_extract_phrases_and_logic


SECTION_TEMPLATES: Dict[str, Dict] = {
    "abstract": {
        "goal": [
            "简洁概括论文的核心贡献",
            "说明研究问题和动机",
            "简要描述方法创新",
            "突出主要实验结果",
            "吸引读者兴趣"
        ],
        "structure": [
            "研究背景与问题（1-2句）",
            "方法创新（1-2句）",
            "技术特点（1-2句）",
            "实验结果（1-2句）",
            "意义与贡献（1句）"
        ],
        "tone": [
            "客观、简洁、准确",
            "避免主观评价",
            "使用专业术语",
            "一般现在时描述方法",
            "一般过去时描述实验"
        ],
        "avoid": [
            "主观评价：excellent, outstanding, best, superior",
            "夸大词汇：revolutionary, groundbreaking, state-of-the-art",
            "模糊表达：maybe, perhaps, might be",
            "口语化表达：缩写、俚语",
            "过度承诺：解决所有问题、完美方案"
        ],
        "constraints": [
            "长度：150-250词",
            "结构：单一段落或2-3个短段落",
            "术语：使用领域标准术语",
            "数据：包含关键实验结果数据",
            "创新点：明确说明主要创新",
            "不编造事实、数字、引用",
            "不引入新实验结果"
        ]
    },
    "introduction": {
        "goal": [
            "介绍研究领域和背景",
            "指出现有方法的不足和问题",
            "提出本文的方法和创新",
            "说明论文的主要贡献",
            "引导读者理解论文结构"
        ],
        "structure": [
            "研究背景（2-3段）",
            "现有方法的局限性（1-2段）",
            "本文方法的提出（1-2段）",
            "主要贡献（1段）",
            "论文结构说明（可选）"
        ],
        "tone": [
            "客观、严谨、有说服力",
            "使用文献支持观点",
            "避免过度批评现有方法",
            "强调创新性和必要性"
        ],
        "avoid": [
            "过度批评现有方法",
            "夸大研究意义",
            "使用第一人称过多",
            "缺乏文献支持",
            "逻辑不连贯"
        ],
        "constraints": [
            "长度：800-1200词",
            "引用：至少15-20篇参考文献",
            "结构：背景→问题→方法→贡献",
            "贡献：明确列出2-4个主要贡献",
            "不编造研究背景",
            "不夸大方法创新性"
        ]
    },
    "related_work": {
        "goal": [
            "全面回顾相关领域的研究",
            "分类整理现有方法",
            "指出现有方法的优缺点",
            "为本文方法提供理论依据",
            "突出本文方法的创新点"
        ],
        "structure": [
            "研究领域概述（1段）",
            "方法分类（2-4个类别）",
            "各类方法详细分析（每类2-3段）",
            "现有方法的总结（1段）",
            "本文方法的定位（1段）"
        ],
        "tone": [
            "客观、全面、有条理",
            "使用文献综述的语气",
            "避免主观评价",
            "强调分类和比较"
        ],
        "avoid": [
            "简单罗列文献",
            "缺乏分类和比较",
            "主观评价现有方法",
            "遗漏重要文献",
            "与introduction重复"
        ],
        "constraints": [
            "长度：1000-1500词",
            "引用：至少30-40篇参考文献",
            "分类：至少2-3个主要类别",
            "比较：突出各类方法的优缺点",
            "不遗漏重要相关工作",
            "不重复introduction内容"
        ]
    },
    "methods": {
        "goal": [
            "详细描述提出的方法",
            "说明方法的技术细节",
            "解释方法的创新点",
            "提供方法的理论依据",
            "使读者能够理解和复现"
        ],
        "structure": [
            "方法概述（1-2段）",
            "整体架构（1-2段）",
            "各个模块详细描述（每个模块2-3段）",
            "技术细节和公式（根据需要）",
            "训练和优化策略（1-2段）"
        ],
        "tone": [
            "技术性、精确、清晰",
            "使用被动语态描述过程",
            "避免主观评价",
            "强调技术细节"
        ],
        "avoid": [
            "过于简略的描述",
            "缺乏技术细节",
            "使用模糊表达",
            "缺乏公式和图表",
            "重复related work内容"
        ],
        "constraints": [
            "长度：1500-2500词",
            "图表：至少3-5个图表",
            "公式：关键算法需要公式描述",
            "细节：足够详细的描述以支持复现",
            "不遗漏关键技术细节",
            "不引入未定义术语"
        ]
    },
    "results": {
        "goal": [
            "展示实验结果和性能",
            "与现有方法进行比较",
            "分析方法的有效性",
            "验证方法的创新点",
            "提供定量的结果分析"
        ],
        "structure": [
            "实验设置（1-2段）",
            "数据集和评估指标（1段）",
            "定量结果（2-3段）",
            "定性结果（1-2段）",
            "消融实验（1-2段）",
            "与现有方法比较（2-3段）"
        ],
        "tone": [
            "客观、准确、有说服力",
            "使用数据和图表支持",
            "避免主观评价",
            "强调性能提升"
        ],
        "avoid": [
            "选择性展示结果",
            "缺乏比较和分析",
            "使用模糊描述",
            "缺乏统计显著性",
            "过度解释结果"
        ],
        "constraints": [
            "长度：1500-2000词",
            "表格：至少3-5个结果表格",
            "图表：至少2-4个可视化结果",
            "比较：与至少5-8个现有方法比较",
            "消融实验：验证各模块有效性",
            "不编造实验结果",
            "不遗漏重要比较方法"
        ]
    },
    "discussion": {
        "goal": [
            "解释实验结果的意义",
            "分析方法的优缺点",
            "讨论方法的局限性",
            "提出未来改进方向",
            "总结研究的主要发现"
        ],
        "structure": [
            "结果分析（2-3段）",
            "方法优势（1-2段）",
            "方法局限性（1-2段）",
            "未来工作（1段）",
            "总结（1段）"
        ],
        "tone": [
            "客观、分析性、反思性",
            "使用hedge词表达谨慎",
            "避免过度承诺",
            "强调学习和改进"
        ],
        "avoid": [
            "重复results内容",
            "缺乏深度分析",
            "忽略局限性",
            "过度承诺",
            "缺乏未来方向"
        ],
        "constraints": [
            "长度：800-1200词",
            "分析：深入解释结果原因",
            "局限：诚实承认方法不足",
            "未来：提出具体改进方向",
            "不重复results数据",
            "不夸大方法意义"
        ]
    },
    "conclusion": {
        "goal": [
            "总结论文的主要贡献",
            "强调方法的创新点",
            "说明研究的意义",
            "提出未来工作方向",
            "给读者留下深刻印象"
        ],
        "structure": [
            "研究总结（1-2段）",
            "主要贡献（1段）",
            "研究意义（1段）",
            "未来工作（1段）",
            "结束语（1句）"
        ],
        "tone": [
            "简洁、有力、有说服力",
            "使用现在完成时总结",
            "避免引入新信息",
            "强调实际应用价值"
        ],
        "avoid": [
            "重复abstract内容",
            "引入新信息",
            "过度承诺",
            "缺乏未来方向",
            "过于简略"
        ],
        "constraints": [
            "长度：300-500词",
            "贡献：明确列出主要贡献",
            "意义：说明实际应用价值",
            "未来：提出具体改进方向",
            "不引入新实验结果",
            "不重复详细内容"
        ]
    }
}


class SkillGenerator:
    def __init__(self, author_id: str, project_base: Optional[str] = None):
        self.author_id = author_id
        self.project_base = Path(project_base) if project_base else Path(__file__).parent.parent
        self.report = {}
        self.report_path = self.project_base / "authors" / author_id / "analysis" / "aggregation_report.json"
        self.load_aggregation_report()

    def load_aggregation_report(self):
        if self.report_path.exists():
            with open(self.report_path, "r", encoding="utf-8") as f:
                self.report = json.load(f)
            print(f"Loaded aggregation report: {self.report_path}")
        else:
            print(f"Warning: aggregation report not found at {self.report_path}; using generic fallbacks.")

    def _build_report_summary_for_section(self, section: str) -> str:
        """Build a concise summary of the aggregation report relevant to this section."""
        parts = []
        # Surface style
        ss = self.report.get("surface_style_aggregate", {})
        if ss:
            parts.append(f"Sentence length: {ss.get('sentence_length_stats', {})}")
            parts.append(f"Voice: {ss.get('voice_stats', {})}")
            parts.append(f"First person: {ss.get('first_person_stats', {})}")
            top_conj = ss.get("top_conjunctions", [])[:5]
            if top_conj:
                parts.append(f"Top conjunctions: {top_conj}")
        # Syntactic style
        syn = self.report.get("syntactic_style_aggregate", {})
        if syn:
            parts.append(f"Concession preference: {syn.get('concession_pref')}")
            parts.append(f"Causal preference: {syn.get('causal_pref')}")
            parts.append(f"Nominalization preference: {syn.get('nominalization_pref')}")
        # Rhetorical structure for this section
        rs = self.report.get("rhetorical_structure_aggregate", {}).get(section, {})
        if rs:
            parts.append(f"Rhetorical patterns: {rs}")
        # Academic stance
        ac = self.report.get("academic_stance_aggregate", {})
        if ac:
            parts.append(f"Academic stance: {ac}")
        return "\n".join(parts)

    def generate_section_skill(self, section: str, use_llm: bool = True) -> Dict:
        base = dict(SECTION_TEMPLATES[section])
        base["section"] = section

        if use_llm:
            try:
                summary = self._build_report_summary_for_section(section)
                extracted = llm_extract_phrases_and_logic(section, summary)
                base["preferred_phrases"] = extracted.get("preferred_phrases", base.get("preferred_phrases", []))
                base["logic_pattern"] = extracted.get("logic_pattern", base.get("logic_pattern", []))
                print(f"  [{section}] LLM enrichment succeeded.")
            except Exception as e:
                print(f"  [{section}] LLM enrichment failed: {e}. Using fallback phrases/patterns.")
                # Fallback logic pattern from report if available
                rs = self.report.get("rhetorical_structure_aggregate", {}).get(section, {})
                pattern = rs.get("most_common_pattern")
                if pattern:
                    base["logic_pattern"] = [pattern]
                if "preferred_phrases" not in base:
                    base["preferred_phrases"] = []
        else:
            rs = self.report.get("rhetorical_structure_aggregate", {}).get(section, {})
            pattern = rs.get("most_common_pattern")
            if pattern:
                base["logic_pattern"] = [pattern]
            if "preferred_phrases" not in base:
                base["preferred_phrases"] = []

        return base

    def generate_all_skills(self, use_llm: bool = True) -> Dict[str, Dict]:
        skills = {}
        for section in SECTION_TEMPLATES.keys():
            skills[section] = self.generate_section_skill(section, use_llm=use_llm)
        return skills

    def save_skills(self, skills: Dict[str, Dict]):
        output_dir = self.project_base / "authors" / self.author_id / "skills"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save combined
        combined_path = output_dir / "all_skills.json"
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(skills, f, indent=2, ensure_ascii=False)
        print(f"Saved combined skills: {combined_path}")

        # Save per-section
        for section, skill in skills.items():
            path = output_dir / f"skill_{section}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(skill, f, indent=2, ensure_ascii=False)
            print(f"Saved section skill: {path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate section-specific writing skills for an author.")
    parser.add_argument("--author", required=True, help="Author ID (e.g., xu-tang)")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM enrichment and use fallback values only")
    parser.add_argument("--base", default=None, help="Project base path (default: parent of factory/)")
    args = parser.parse_args()

    generator = SkillGenerator(args.author, project_base=args.base)
    skills = generator.generate_all_skills(use_llm=not args.no_llm)
    generator.save_skills(skills)
    print("\nSkill generation completed.")


if __name__ == "__main__":
    main()
