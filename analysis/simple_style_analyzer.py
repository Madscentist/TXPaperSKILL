"""
阶段2：单论文风格分析（完全不依赖NLTK）
"""
import os
import re
import json
from typing import Dict, List, Tuple

class SimpleStyleAnalyzer:
    def __init__(self, analysis_file: str):
        self.analysis_file = analysis_file
        self.papers = []
        self.load_analysis()
    
    def load_analysis(self):
        """加载阶段1的分析结果"""
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            self.papers = json.load(f)
    
    def simple_sent_tokenize(self, text: str) -> List[str]:
        """简单的分句方法"""
        # 按句号、问号、感叹号分句
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def simple_word_tokenize(self, text: str) -> List[str]:
        """简单的分词方法"""
        # 按空格和标点分词
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def analyze_surface_style(self, text: str) -> Dict:
        """分析表层风格"""
        # 分句
        sentences = self.simple_sent_tokenize(text)
        
        # 分词
        words = self.simple_word_tokenize(text)
        
        # 计算句长
        sentence_lengths = [len(self.simple_word_tokenize(sent)) for sent in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # 判断句长偏好
        if avg_sentence_length < 15:
            sentence_length_pref = "短句"
        elif avg_sentence_length < 25:
            sentence_length_pref = "中等句"
        else:
            sentence_length_pref = "长句"
        
        # 计算段落长度（按空行分割）
        paragraphs = re.split(r'\n\s*\n', text)
        paragraph_lengths = [len(self.simple_word_tokenize(para)) for para in paragraphs if para.strip()]
        avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
        
        # 分析主动/被动语态
        passive_indicators = ['is', 'are', 'was', 'were', 'be', 'been', 'being']
        passive_count = sum(1 for word in words if word.lower() in passive_indicators)
        passive_ratio = passive_count / len(words) if words else 0
        
        # 判断语态偏好
        if passive_ratio > 0.05:
            voice_pref = "被动语态较多"
        else:
            voice_pref = "主动语态较多"
        
        # 分析第一人称使用
        first_person = ['i', 'we', 'our', 'us', 'me', 'my']
        first_person_count = sum(1 for word in words if word.lower() in first_person)
        first_person_ratio = first_person_count / len(words) if words else 0
        
        # 判断第一人称使用
        if first_person_ratio > 0.01:
            first_person_usage = "使用第一人称"
        else:
            first_person_usage = "避免第一人称"
        
        # 分析高频连接词
        conjunctions = ['however', 'but', 'although', 'therefore', 'thus', 'hence', 'consequently', 
                       'furthermore', 'moreover', 'additionally', 'in addition', 'for example', 
                       'for instance', 'specifically', 'in particular', 'on the other hand']
        conjunction_counts = {}
        for conj in conjunctions:
            count = text.lower().count(conj)
            if count > 0:
                conjunction_counts[conj] = count
        
        # 分析hedge词
        hedge_words = ['may', 'might', 'could', 'possibly', 'perhaps', 'suggests', 'indicates', 
                      'appears', 'seems', 'likely', 'unlikely', 'probably']
        hedge_counts = {}
        for hedge in hedge_words:
            count = text.lower().count(hedge)
            if count > 0:
                hedge_counts[hedge] = count
        
        # 分析强调词
        emphasis_words = ['notably', 'importantly', 'significantly', 'considerably', 'remarkably', 
                         'particularly', 'especially', 'crucially', 'essentially']
        emphasis_counts = {}
        for emphasis in emphasis_words:
            count = text.lower().count(emphasis)
            if count > 0:
                emphasis_counts[emphasis] = count
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'sentence_length_pref': sentence_length_pref,
            'avg_paragraph_length': avg_paragraph_length,
            'passive_ratio': passive_ratio,
            'voice_pref': voice_pref,
            'first_person_ratio': first_person_ratio,
            'first_person_usage': first_person_usage,
            'top_conjunctions': dict(sorted(conjunction_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'top_hedge_words': dict(sorted(hedge_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'top_emphasis_words': dict(sorted(emphasis_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        }
    
    def analyze_syntactic_style(self, text: str) -> Dict:
        """分析句法表达风格"""
        sentences = self.simple_sent_tokenize(text)
        
        # 分析先总后分结构
        general_specific_indicators = ['in general', 'generally', 'overall', 'in summary', 'to summarize',
                                      'specifically', 'in particular', 'for example', 'for instance']
        general_specific_count = sum(1 for indicator in general_specific_indicators if indicator in text.lower())
        
        # 分析让步句
        concession_indicators = ['although', 'though', 'even though', 'while', 'whereas', 'despite', 
                                'in spite of', 'nevertheless', 'however', 'but']
        concession_count = sum(1 for indicator in concession_indicators if indicator in text.lower())
        
        # 分析因果句
        causal_indicators = ['because', 'since', 'as', 'therefore', 'thus', 'hence', 'consequently', 
                           'as a result', 'due to', 'owing to']
        causal_count = sum(1 for indicator in causal_indicators if indicator in text.lower())
        
        # 分析比较句
        comparison_indicators = ['compared with', 'compared to', 'in comparison', 'relative to', 
                               'similarly', 'likewise', 'in contrast', 'on the other hand']
        comparison_count = sum(1 for indicator in comparison_indicators if indicator in text.lower())
        
        # 分析名词化表达
        nominalization_indicators = ['tion', 'sion', 'ment', 'ness', 'ity', 'ance', 'ence']
        nominalization_count = sum(1 for word in self.simple_word_tokenize(text) 
                                 if any(word.lower().endswith(indicator) for indicator in nominalization_indicators))
        
        # 分析句尾收意义
        sentence_endings = [sent.strip()[-20:] for sent in sentences if len(sent.strip()) > 20]
        ending_patterns = {}
        for ending in sentence_endings:
            if ending.endswith('.'):
                ending_patterns['period'] = ending_patterns.get('period', 0) + 1
            elif ending.endswith(')'):
                ending_patterns['citation'] = ending_patterns.get('citation', 0) + 1
            elif ending.endswith(':'):
                ending_patterns['colon'] = ending_patterns.get('colon', 0) + 1
        
        return {
            'general_specific_ratio': general_specific_count / len(sentences) if sentences else 0,
            'concession_ratio': concession_count / len(sentences) if sentences else 0,
            'causal_ratio': causal_count / len(sentences) if sentences else 0,
            'comparison_ratio': comparison_count / len(sentences) if sentences else 0,
            'nominalization_ratio': nominalization_count / len(self.simple_word_tokenize(text)) if text else 0,
            'sentence_endings': ending_patterns
        }
    
    def analyze_rhetorical_structure(self, paper_analysis: Dict) -> Dict:
        """分析修辞结构（按section）"""
        rhetorical_patterns = {}
        
        for section_name, section_data in paper_analysis['sections'].items():
            if section_data['paragraph_count'] == 0:
                continue
            
            # 分析段落功能标签的分布
            function_counts = {}
            for para in section_data['paragraphs']:
                func = para['function']
                function_counts[func] = function_counts.get(func, 0) + 1
            
            # 确定主要的修辞模式
            if section_name == 'introduction':
                if function_counts.get('background', 0) > 0 and function_counts.get('gap', 0) > 0:
                    rhetorical_patterns[section_name] = "background → gap → method → contribution"
                else:
                    rhetorical_patterns[section_name] = "background → method"
            
            elif section_name == 'methods':
                if function_counts.get('method_overview', 0) > 0:
                    rhetorical_patterns[section_name] = "overview → technical details"
                else:
                    rhetorical_patterns[section_name] = "technical details"
            
            elif section_name == 'results':
                if function_counts.get('comparison', 0) > 0:
                    rhetorical_patterns[section_name] = "setup → results → comparison"
                else:
                    rhetorical_patterns[section_name] = "results"
            
            elif section_name == 'discussion':
                if function_counts.get('limitation', 0) > 0:
                    rhetorical_patterns[section_name] = "observation → explanation → limitation"
                else:
                    rhetorical_patterns[section_name] = "observation → explanation"
            
            elif section_name == 'conclusion':
                if function_counts.get('contribution_summary', 0) > 0:
                    rhetorical_patterns[section_name] = "summary → contribution → future work"
                else:
                    rhetorical_patterns[section_name] = "summary"
        
        return rhetorical_patterns
    
    def analyze_academic_stance(self, text: str) -> Dict:
        """分析学术姿态"""
        text_lower = text.lower()
        
        # 分析断言强弱
        strong_assertions = ['prove', 'demonstrate', 'show', 'confirm', 'establish', 'clearly', 'obviously']
        weak_assertions = ['suggest', 'indicate', 'imply', 'appear', 'seem', 'likely', 'possibly']
        
        strong_count = sum(1 for word in strong_assertions if word in text_lower)
        weak_count = sum(1 for word in weak_assertions if word in text_lower)
        
        if strong_count > weak_count:
            assertion_strength = "强断言"
        elif weak_count > strong_count:
            assertion_strength = "弱断言"
        else:
            assertion_strength = "平衡"
        
        # 分析保守表达
        conservative_indicators = ['may', 'might', 'could', 'possibly', 'perhaps', 'suggests', 'indicates']
        conservative_count = sum(1 for word in conservative_indicators if word in text_lower)
        
        if conservative_count > 5:
            conservative_expression = "保守表达较多"
        else:
            conservative_expression = "保守表达较少"
        
        # 分析是否承认局限
        limitation_indicators = ['limit', 'weakness', 'drawback', 'challenge', 'issue', 'problem', 
                               'difficulty', 'future work', 'further research']
        limitation_count = sum(1 for indicator in limitation_indicators if indicator in text_lower)
        
        if limitation_count > 3:
            acknowledges_limitations = "承认局限"
        else:
            acknowledges_limitations = "较少承认局限"
        
        # 分析强调方向
        novelty_indicators = ['novel', 'new', 'first', 'innovative', 'original', 'unique']
        robustness_indicators = ['robust', 'stable', 'reliable', 'consistent', 'effective']
        generalization_indicators = ['generalize', 'general', 'universal', 'broad', 'wide']
        efficiency_indicators = ['efficient', 'fast', 'speed', 'time', 'computational']
        
        novelty_count = sum(1 for word in novelty_indicators if word in text_lower)
        robustness_count = sum(1 for word in robustness_indicators if word in text_lower)
        generalization_count = sum(1 for word in generalization_indicators if word in text_lower)
        efficiency_count = sum(1 for word in efficiency_indicators if word in text_lower)
        
        emphasis_directions = []
        if novelty_count > 2:
            emphasis_directions.append("novelty")
        if robustness_count > 2:
            emphasis_directions.append("robustness")
        if generalization_count > 2:
            emphasis_directions.append("generalization")
        if efficiency_count > 2:
            emphasis_directions.append("efficiency")
        
        return {
            'assertion_strength': assertion_strength,
            'conservative_expression': conservative_expression,
            'acknowledges_limitations': acknowledges_limitations,
            'emphasis_directions': emphasis_directions
        }
    
    def analyze_paper_style(self, paper_analysis: Dict) -> Dict:
        """分析单篇论文的风格"""
        filename = paper_analysis['filename']
        print(f"分析风格: {filename}")
        
        # 提取所有文本
        all_text = ""
        for section_name, section_data in paper_analysis['sections'].items():
            all_text += section_data['content_preview'] + " "
        
        # 分析四个维度
        surface_style = self.analyze_surface_style(all_text)
        syntactic_style = self.analyze_syntactic_style(all_text)
        rhetorical_structure = self.analyze_rhetorical_structure(paper_analysis)
        academic_stance = self.analyze_academic_stance(all_text)
        
        return {
            'filename': filename,
            'surface_style': surface_style,
            'syntactic_style': syntactic_style,
            'rhetorical_structure': rhetorical_structure,
            'academic_stance': academic_stance
        }
    
    def analyze_all_papers(self):
        """分析所有论文的风格"""
        style_analyses = []
        
        for paper_analysis in self.papers:
            try:
                style_analysis = self.analyze_paper_style(paper_analysis)
                style_analyses.append(style_analysis)
            except Exception as e:
                print(f"分析{paper_analysis['filename']}风格时出错: {e}")
                import traceback
                traceback.print_exc()
        
        return style_analyses
    
    def save_style_analysis(self, output_path: str, style_analyses: List[Dict]):
        """保存风格分析结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(style_analyses, f, indent=2, ensure_ascii=False)
        print(f"风格分析结果已保存到: {output_path}")


# 使用示例
if __name__ == "__main__":
    analyzer = SimpleStyleAnalyzer("/mnt/g/project/PaperSkill/analysis/direct_papers_analysis.json")
    style_analyses = analyzer.analyze_all_papers()
    analyzer.save_style_analysis("/mnt/g/project/PaperSkill/analysis/simple_style_analyses.json", style_analyses)