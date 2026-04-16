"""
论文结构分析脚本
阶段1：结构解析
"""
import os
import re
import json
from typing import Dict, List, Tuple

class PaperAnalyzer:
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
        
        # 常见的section标题模式
        section_patterns = {
            'abstract': r'(?i)abstract',
            'introduction': r'(?i)introduction',
            'related_work': r'(?i)(related\s+work|literature\s+review|previous\s+work)',
            'methods': r'(?i)(method|proposed\s+method|approach|architecture|model)',
            'results': r'(?i)(experiment|result|evaluation|performance|ablation)',
            'discussion': r'(?i)discussion',
            'conclusion': r'(?i)conclusion'
        }
        
        # 尝试找到每个section的开始位置
        for section_name, pattern in section_patterns.items():
            matches = list(re.finditer(pattern, text))
            if matches:
                # 取第一个匹配
                start_pos = matches[0].start()
                sections[section_name] = start_pos
        
        # 按位置排序
        sorted_sections = sorted(sections.items(), key=lambda x: x[1])
        
        # 提取每个section的内容
        section_contents = {}
        for i, (section_name, start_pos) in enumerate(sorted_sections):
            if i < len(sorted_sections) - 1:
                next_start = sorted_sections[i + 1][1]
                content = text[start_pos:next_start]
            else:
                content = text[start_pos:]
            
            # 清理内容（移除页眉页脚等）
            content = self.clean_section_content(content)
            section_contents[section_name] = content
        
        return section_contents
    
    def clean_section_content(self, content: str) -> str:
        """清理section内容，移除页眉页脚等"""
        # 移除页眉（如"IEEE TRANSACTIONS ON..."）
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 跳过页眉行
            if re.match(r'IEEE\s+TRANSACTIONS\s+ON', line, re.IGNORECASE):
                continue
            # 跳过页码行
            if re.match(r'^\d+$', line.strip()):
                continue
            # 跳过页脚行
            if re.match(r'^\d+\s*$', line.strip()):
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
            if para and len(para) > 50:  # 过滤太短的段落
                cleaned_paragraphs.append(para)
        
        return cleaned_paragraphs
    
    def label_paragraph_function(self, paragraph: str, section_name: str) -> str:
        """为段落标注功能标签"""
        paragraph_lower = paragraph.lower()
        
        # 根据section和内容判断功能
        if section_name == 'abstract':
            if 'propose' in paragraph_lower or 'introduce' in paragraph_lower:
                return 'method_overview'
            elif 'experiment' in paragraph_lower or 'result' in paragraph_lower:
                return 'result_report'
            else:
                return 'background'
        
        elif section_name == 'introduction':
            if any(word in paragraph_lower for word in ['however', 'but', 'although', 'despite']):
                return 'gap'
            elif any(word in paragraph_lower for word in ['propose', 'introduce', 'develop', 'present']):
                return 'method_overview'
            elif any(word in paragraph_lower for word in ['contribution', 'main', 'firstly', 'secondly']):
                return 'contribution_summary'
            else:
                return 'background'
        
        elif section_name == 'related_work':
            if 'recent' in paragraph_lower or 'latest' in paragraph_lower:
                return 'background'
            else:
                return 'background'
        
        elif section_name == 'methods':
            if any(word in paragraph_lower for word in ['overview', 'architecture', 'framework']):
                return 'method_overview'
            else:
                return 'technical_detail'
        
        elif section_name == 'results':
            if any(word in paragraph_lower for word in ['compare', 'comparison', 'baseline']):
                return 'comparison'
            elif any(word in paragraph_lower for word in ['show', 'demonstrate', 'achieve']):
                return 'result_report'
            elif any(word in paragraph_lower for word in ['analyze', 'observation', 'reason']):
                return 'result_explanation'
            else:
                return 'result_report'
        
        elif section_name == 'discussion':
            if any(word in paragraph_lower for word in ['limit', 'weakness', 'challenge']):
                return 'limitation'
            elif any(word in paragraph_lower for word in ['suggest', 'imply', 'future']):
                return 'implication'
            else:
                return 'result_explanation'
        
        elif section_name == 'conclusion':
            if any(word in paragraph_lower for word in ['summary', 'conclude', 'main']):
                return 'contribution_summary'
            elif any(word in paragraph_lower for word in ['future', 'next', 'extend']):
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
    analyzer = PaperAnalyzer("/mnt/g/project/PaperSkill/extracted_texts")
    analyzer.analyze_all_papers()
    analyzer.save_analysis("/mnt/g/project/PaperSkill/analysis/papers_analysis.json")