"""
最终版论文结构分析脚本
"""
import os
import re
import json
from typing import Dict, List, Tuple

class FinalPaperAnalyzer:
    def __init__(self, text_dir: str):
        self.text_dir = text_dir
        self.papers = []
        
    def load_paper(self, filename: str) -> str:
        """加载论文文本"""
        filepath = os.path.join(self.text_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def identify_sections(self, text: str) -> Dict[str, str]:
        """识别论文的主要section"""
        sections = {}
        
        # 更灵活的section标题模式
        heading_patterns = [
            # I. INTRODUCTION 格式（允许空格）
            r'(?:^|\n)\s*(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s*([A-Z](?:\s*[A-Z])+)',
            # I. Introduction 格式
            r'(?:^|\n)\s*(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            # INTRODUCTION 格式（全大写）
            r'(?:^|\n)\s*([A-Z](?:\s*[A-Z]){2,})\s*(?:\n|$)',
            # Introduction 格式（首字母大写）
            r'(?:^|\n)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:\n|$)',
            # A. CNN-Based CD Models 格式
            r'(?:^|\n)\s*[A-Z]\.\s*([A-Z][a-z]+(?:[-\s][A-Z][a-z]+)*)',
            # Abstract 格式
            r'(?i)(?:^|\n)\s*(abstract)\s*[-—]',
        ]
        
        # 找到所有可能的标题位置
        headings = []
        for pattern in heading_patterns:
            for match in re.finditer(pattern, text):
                heading_text = match.group(1).strip().upper()
                start_pos = match.start()
                
                # 标准化标题名称
                if 'ABSTRACT' in heading_text:
                    section_name = 'abstract'
                elif 'INTRODUCTION' in heading_text:
                    section_name = 'introduction'
                elif 'RELATED' in heading_text or 'LITERATURE' in heading_text or 'PREVIOUS' in heading_text:
                    section_name = 'related_work'
                elif 'METHOD' in heading_text or 'PROPOSED' in heading_text or 'APPROACH' in heading_text or 'ARCHITECTURE' in heading_text:
                    section_name = 'methods'
                elif 'EXPERIMENT' in heading_text or 'RESULT' in heading_text or 'EVALUATION' in heading_text or 'PERFORMANCE' in heading_text:
                    section_name = 'results'
                elif 'DISCUSSION' in heading_text:
                    section_name = 'discussion'
                elif 'CONCLUSION' in heading_text:
                    section_name = 'conclusion'
                else:
                    continue  # 跳过未识别的标题
                
                headings.append((section_name, start_pos, match.group(0)))
        
        # 按位置排序
        headings.sort(key=lambda x: x[1])
        
        # 提取每个section的内容
        for i, (section_name, start_pos, heading_text) in enumerate(headings):
            if i < len(headings) - 1:
                next_start = headings[i + 1][1]
                content = text[start_pos:next_start]
            else:
                content = text[start_pos:]
            
            # 清理内容
            content = self.clean_section_content(content)
            sections[section_name] = content
        
        return sections
    
    def clean_section_content(self, content: str) -> str:
        """清理section内容"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 跳过页眉
            if re.match(r'IEEE\s+TRANSACTIONS\s+ON', line, re.IGNORECASE):
                continue
            # 跳过页码
            if re.match(r'^\d+\s*$', line.strip()):
                continue
            # 跳过授权信息
            if 'Authorized licensed use limited to' in line:
                continue
            if 'Downloaded on' in line:
                continue
            if 'Restrictions apply' in line:
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def split_into_paragraphs(self, section_content: str) -> List[str]:
        """将section内容切分为段落"""
        # 按空行分割段落
        paragraphs = re.split(r'\n\s*\n', section_content)
        
        # 清理每个段落
        cleaned_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            # 过滤太短的段落和明显不是正文的段落
            if para and len(para) > 100 and not re.match(r'^(Fig|Table|Figure|Equation)', para):
                cleaned_paragraphs.append(para)
        
        return cleaned_paragraphs
    
    def label_paragraph_function(self, paragraph: str, section_name: str) -> str:
        """为段落标注功能标签"""
        paragraph_lower = paragraph.lower()
        
        # 定义关键词映射
        keyword_mapping = {
            'background': ['recently', 'in the past', 'traditional', 'existing', 'previous', 'studies have shown'],
            'problem_statement': ['however', 'but', 'although', 'despite', 'nevertheless', 'limitation', 'challenge', 'issue'],
            'gap': ['however', 'but', 'although', 'despite', 'nevertheless', 'few', 'little', 'lack', 'missing'],
            'motivation': ['therefore', 'thus', 'hence', 'consequently', 'as a result', 'motivate', 'inspire'],
            'method_overview': ['propose', 'introduce', 'develop', 'present', 'design', 'our method', 'our approach', 'framework', 'architecture'],
            'technical_detail': ['specifically', 'in detail', 'consist of', 'comprise', 'module', 'block', 'layer', 'operation'],
            'experiment_setup': ['dataset', 'evaluation', 'metric', 'implementation', 'training', 'testing', 'validation', 'setting'],
            'result_report': ['achieve', 'obtain', 'show', 'demonstrate', 'performance', 'accuracy', 'improvement', 'outperform'],
            'comparison': ['compare', 'comparison', 'baseline', 'state-of-the-art', 'existing method', 'previous work'],
            'result_explanation': ['reason', 'because', 'since', 'due to', 'explain', 'analyze', 'observation', 'interpret'],
            'limitation': ['limit', 'weakness', 'drawback', 'challenge', 'issue', 'problem', 'difficulty'],
            'implication': ['future', 'extend', 'improve', 'suggest', 'imply', 'potential', 'direction'],
            'contribution_summary': ['contribution', 'main', 'firstly', 'secondly', 'thirdly', 'finally', 'summary', 'conclude']
        }
        
        # 根据section和内容判断功能
        if section_name == 'abstract':
            if any(word in paragraph_lower for word in keyword_mapping['method_overview']):
                return 'method_overview'
            elif any(word in paragraph_lower for word in keyword_mapping['result_report']):
                return 'result_report'
            else:
                return 'background'
        
        elif section_name == 'introduction':
            if any(word in paragraph_lower for word in keyword_mapping['problem_statement'] + keyword_mapping['gap']):
                return 'gap'
            elif any(word in paragraph_lower for word in keyword_mapping['method_overview']):
                return 'method_overview'
            elif any(word in paragraph_lower for word in keyword_mapping['contribution_summary']):
                return 'contribution_summary'
            else:
                return 'background'
        
        elif section_name == 'related_work':
            if any(word in paragraph_lower for word in keyword_mapping['comparison']):
                return 'comparison'
            else:
                return 'background'
        
        elif section_name == 'methods':
            if any(word in paragraph_lower for word in keyword_mapping['method_overview']):
                return 'method_overview'
            else:
                return 'technical_detail'
        
        elif section_name == 'results':
            if any(word in paragraph_lower for word in keyword_mapping['comparison']):
                return 'comparison'
            elif any(word in paragraph_lower for word in keyword_mapping['result_report']):
                return 'result_report'
            elif any(word in paragraph_lower for word in keyword_mapping['result_explanation']):
                return 'result_explanation'
            else:
                return 'result_report'
        
        elif section_name == 'discussion':
            if any(word in paragraph_lower for word in keyword_mapping['limitation']):
                return 'limitation'
            elif any(word in paragraph_lower for word in keyword_mapping['implication']):
                return 'implication'
            else:
                return 'result_explanation'
        
        elif section_name == 'conclusion':
            if any(word in paragraph_lower for word in keyword_mapping['contribution_summary']):
                return 'contribution_summary'
            elif any(word in paragraph_lower for word in keyword_mapping['implication']):
                return 'implication'
            else:
                return 'contribution_summary'
        
        return 'background'  # 默认
    
    def analyze_paper(self, filename: str) -> Dict:
        """分析单篇论文"""
        print(f"分析论文: {filename}")
        
        # 加载文本
        text = self.load_paper(filename)
        
        # 识别section
        sections = self.identify_sections(text)
        
        # 分析每个section
        paper_analysis = {
            'filename': filename,
            'sections': {}
        }
        
        for section_name, content in sections.items():
            # 切分段落
            paragraphs = self.split_into_paragraphs(content)
            
            # 分析每个段落
            paragraph_analysis = []
            for para in paragraphs:
                function_label = self.label_paragraph_function(para, section_name)
                paragraph_analysis.append({
                    'text': para[:500] + "..." if len(para) > 500 else para,
                    'function': function_label,
                    'length': len(para),
                    'word_count': len(para.split())
                })
            
            paper_analysis['sections'][section_name] = {
                'content_preview': content[:1000] + "..." if len(content) > 1000 else content,
                'paragraphs': paragraph_analysis,
                'paragraph_count': len(paragraphs)
            }
        
        return paper_analysis
    
    def analyze_all_papers(self):
        """分析所有论文"""
        # 获取所有文本文件
        txt_files = [f for f in os.listdir(self.text_dir) if f.endswith('.txt')]
        
        for txt_file in txt_files:
            try:
                analysis = self.analyze_paper(txt_file)
                self.papers.append(analysis)
            except Exception as e:
                print(f"分析{txt_file}时出错: {e}")
    
    def save_analysis(self, output_path: str):
        """保存分析结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.papers, f, indent=2, ensure_ascii=False)
        print(f"分析结果已保存到: {output_path}")


# 使用示例
if __name__ == "__main__":
    analyzer = FinalPaperAnalyzer("/mnt/g/project/PaperSkill/extracted_texts")
    analyzer.analyze_all_papers()
    analyzer.save_analysis("/mnt/g/project/PaperSkill/analysis/final_papers_analysis.json")