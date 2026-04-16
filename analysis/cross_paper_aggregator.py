"""
阶段3：跨论文聚合分析
"""
import os
import json
from typing import Dict, List, Tuple
from collections import Counter

class CrossPaperAggregator:
    def __init__(self, style_analyses_file: str):
        self.style_analyses_file = style_analyses_file
        self.style_analyses = []
        self.load_style_analyses()
    
    def load_style_analyses(self):
        """加载风格分析结果"""
        with open(self.style_analyses_file, 'r', encoding='utf-8') as f:
            self.style_analyses = json.load(f)
    
    def aggregate_surface_style(self) -> Dict:
        """聚合表层风格"""
        # 收集所有论文的表层风格
        sentence_length_prefs = []
        voice_prefs = []
        first_person_usages = []
        all_conjunctions = []
        all_hedge_words = []
        all_emphasis_words = []
        
        for analysis in self.style_analyses:
            surface = analysis['surface_style']
            sentence_length_prefs.append(surface['sentence_length_pref'])
            voice_prefs.append(surface['voice_pref'])
            first_person_usages.append(surface['first_person_usage'])
            
            # 收集连接词
            for conj, count in surface['top_conjunctions'].items():
                all_conjunctions.extend([conj] * count)
            
            # 收集hedge词
            for hedge, count in surface['top_hedge_words'].items():
                all_hedge_words.extend([hedge] * count)
            
            # 收集强调词
            for emphasis, count in surface['top_emphasis_words'].items():
                all_emphasis_words.extend([emphasis] * count)
        
        # 计算统计信息
        total_papers = len(self.style_analyses)
        
        # 句长偏好统计
        sentence_length_counter = Counter(sentence_length_prefs)
        sentence_length_stats = {pref: f"{count}篇 ({count/total_papers*100:.1f}%)" 
                               for pref, count in sentence_length_counter.items()}
        
        # 语态偏好统计
        voice_counter = Counter(voice_prefs)
        voice_stats = {pref: f"{count}篇 ({count/total_papers*100:.1f}%)" 
                      for pref, count in voice_counter.items()}
        
        # 第一人称使用统计
        first_person_counter = Counter(first_person_usages)
        first_person_stats = {usage: f"{count}篇 ({count/total_papers*100:.1f}%)" 
                            for usage, count in first_person_counter.items()}
        
        # 高频连接词统计
        conjunction_counter = Counter(all_conjunctions)
        top_conjunctions = conjunction_counter.most_common(10)
        
        # 高频hedge词统计
        hedge_counter = Counter(all_hedge_words)
        top_hedge_words = hedge_counter.most_common(10)
        
        # 高频强调词统计
        emphasis_counter = Counter(all_emphasis_words)
        top_emphasis_words = emphasis_counter.most_common(10)
        
        return {
            'sentence_length_stats': sentence_length_stats,
            'voice_stats': voice_stats,
            'first_person_stats': first_person_stats,
            'top_conjunctions': top_conjunctions,
            'top_hedge_words': top_hedge_words,
            'top_emphasis_words': top_emphasis_words,
            'total_papers': total_papers
        }
    
    def aggregate_syntactic_style(self) -> Dict:
        """聚合句法表达风格"""
        # 收集所有论文的句法风格
        general_specific_ratios = []
        concession_ratios = []
        causal_ratios = []
        comparison_ratios = []
        nominalization_ratios = []
        
        for analysis in self.style_analyses:
            syntactic = analysis['syntactic_style']
            general_specific_ratios.append(syntactic['general_specific_ratio'])
            concession_ratios.append(syntactic['concession_ratio'])
            causal_ratios.append(syntactic['causal_ratio'])
            comparison_ratios.append(syntactic['comparison_ratio'])
            nominalization_ratios.append(syntactic['nominalization_ratio'])
        
        # 计算平均值
        avg_general_specific = sum(general_specific_ratios) / len(general_specific_ratios) if general_specific_ratios else 0
        avg_concession = sum(concession_ratios) / len(concession_ratios) if concession_ratios else 0
        avg_causal = sum(causal_ratios) / len(causal_ratios) if causal_ratios else 0
        avg_comparison = sum(comparison_ratios) / len(comparison_ratios) if comparison_ratios else 0
        avg_nominalization = sum(nominalization_ratios) / len(nominalization_ratios) if nominalization_ratios else 0
        
        # 判断风格偏好
        general_specific_pref = "先总后分" if avg_general_specific > 0.05 else "较少使用先总后分"
        concession_pref = "常用让步句" if avg_concession > 0.05 else "较少使用让步句"
        causal_pref = "常用因果句" if avg_causal > 0.05 else "较少使用因果句"
        comparison_pref = "常用比较句" if avg_comparison > 0.05 else "较少使用比较句"
        nominalization_pref = "常用名词化" if avg_nominalization > 0.05 else "较少使用名词化"
        
        return {
            'avg_general_specific_ratio': avg_general_specific,
            'general_specific_pref': general_specific_pref,
            'avg_concession_ratio': avg_concession,
            'concession_pref': concession_pref,
            'avg_causal_ratio': avg_causal,
            'causal_pref': causal_pref,
            'avg_comparison_ratio': avg_comparison,
            'comparison_pref': comparison_pref,
            'avg_nominalization_ratio': avg_nominalization,
            'nominalization_pref': nominalization_pref
        }
    
    def aggregate_rhetorical_structure(self) -> Dict:
        """聚合修辞结构"""
        # 收集所有论文的修辞结构
        rhetorical_patterns = {}
        
        for analysis in self.style_analyses:
            rhetorical = analysis['rhetorical_structure']
            for section, pattern in rhetorical.items():
                if section not in rhetorical_patterns:
                    rhetorical_patterns[section] = []
                rhetorical_patterns[section].append(pattern)
        
        # 统计每个section最常见的修辞模式
        section_patterns = {}
        for section, patterns in rhetorical_patterns.items():
            pattern_counter = Counter(patterns)
            most_common = pattern_counter.most_common(1)[0] if pattern_counter else (None, 0)
            section_patterns[section] = {
                'most_common_pattern': most_common[0],
                'frequency': f"{most_common[1]}篇 ({most_common[1]/len(patterns)*100:.1f}%)",
                'total_papers': len(patterns)
            }
        
        return section_patterns
    
    def aggregate_academic_stance(self) -> Dict:
        """聚合学术姿态"""
        # 收集所有论文的学术姿态
        assertion_strengths = []
        conservative_expressions = []
        acknowledges_limitations_list = []
        all_emphasis_directions = []
        
        for analysis in self.style_analyses:
            stance = analysis['academic_stance']
            assertion_strengths.append(stance['assertion_strength'])
            conservative_expressions.append(stance['conservative_expression'])
            acknowledges_limitations_list.append(stance['acknowledges_limitations'])
            
            # 收集强调方向
            for direction in stance['emphasis_directions']:
                all_emphasis_directions.append(direction)
        
        # 计算统计信息
        total_papers = len(self.style_analyses)
        
        # 断言强弱统计
        assertion_counter = Counter(assertion_strengths)
        assertion_stats = {strength: f"{count}篇 ({count/total_papers*100:.1f}%)" 
                          for strength, count in assertion_counter.items()}
        
        # 保守表达统计
        conservative_counter = Counter(conservative_expressions)
        conservative_stats = {expr: f"{count}篇 ({count/total_papers*100:.1f}%)" 
                            for expr, count in conservative_counter.items()}
        
        # 承认局限统计
        limitation_counter = Counter(acknowledges_limitations_list)
        limitation_stats = {ack: f"{count}篇 ({count/total_papers*100:.1f}%)" 
                          for ack, count in limitation_counter.items()}
        
        # 强调方向统计
        emphasis_counter = Counter(all_emphasis_directions)
        top_emphasis_directions = emphasis_counter.most_common(10)
        
        return {
            'assertion_stats': assertion_stats,
            'conservative_stats': conservative_stats,
            'limitation_stats': limitation_stats,
            'top_emphasis_directions': top_emphasis_directions
        }
    
    def identify_stable_styles(self) -> Dict:
        """识别稳定出现的风格（>60%论文）"""
        stable_styles = {}
        
        # 分析表层风格的稳定性
        surface_aggregate = self.aggregate_surface_style()
        
        # 句长偏好稳定性
        sentence_length_stats = surface_aggregate['sentence_length_stats']
        for pref, stat in sentence_length_stats.items():
            if '篇' in stat:
                count = int(stat.split('篇')[0])
                percentage = float(stat.split('(')[1].split('%')[0])
                if percentage > 60:
                    stable_styles[f'句长偏好_{pref}'] = {
                        'confidence': '高置信',
                        'description': f'{percentage:.1f}%的论文使用{pref}',
                        'recommendation': '优先采用'
                    }
        
        # 语态偏好稳定性
        voice_stats = surface_aggregate['voice_stats']
        for pref, stat in voice_stats.items():
            if '篇' in stat:
                percentage = float(stat.split('(')[1].split('%')[0])
                if percentage > 60:
                    stable_styles[f'语态偏好_{pref}'] = {
                        'confidence': '高置信',
                        'description': f'{percentage:.1f}%的论文使用{pref}',
                        'recommendation': '优先采用'
                    }
        
        # 分析句法风格的稳定性
        syntactic_aggregate = self.aggregate_syntactic_style()
        
        # 先总后分结构稳定性
        if syntactic_aggregate['general_specific_pref'] == '先总后分':
            stable_styles['句法结构_先总后分'] = {
                'confidence': '中置信',
                'description': f'平均使用率{syntactic_aggregate["avg_general_specific_ratio"]:.3f}',
                'recommendation': '根据需要采用'
            }
        
        # 让步句使用稳定性
        if syntactic_aggregate['concession_pref'] == '常用让步句':
            stable_styles['句法结构_让步句'] = {
                'confidence': '中置信',
                'description': f'平均使用率{syntactic_aggregate["avg_concession_ratio"]:.3f}',
                'recommendation': '根据需要采用'
            }
        
        # 分析学术姿态的稳定性
        stance_aggregate = self.aggregate_academic_stance()
        
        # 断言强弱稳定性
        assertion_stats = stance_aggregate['assertion_stats']
        for strength, stat in assertion_stats.items():
            if '篇' in stat:
                percentage = float(stat.split('(')[1].split('%')[0])
                if percentage > 60:
                    stable_styles[f'学术姿态_{strength}'] = {
                        'confidence': '高置信',
                        'description': f'{percentage:.1f}%的论文使用{strength}',
                        'recommendation': '优先采用'
                    }
        
        return stable_styles
    
    def generate_aggregation_report(self) -> Dict:
        """生成聚合分析报告"""
        print("生成跨论文聚合分析报告...")
        
        # 聚合各个维度的分析
        surface_aggregate = self.aggregate_surface_style()
        syntactic_aggregate = self.aggregate_syntactic_style()
        rhetorical_aggregate = self.aggregate_rhetorical_structure()
        stance_aggregate = self.aggregate_academic_stance()
        stable_styles = self.identify_stable_styles()
        
        # 生成报告
        report = {
            'summary': {
                'total_papers_analyzed': len(self.style_analyses),
                'analysis_dimensions': ['surface_style', 'syntactic_style', 'rhetorical_structure', 'academic_stance']
            },
            'surface_style_aggregate': surface_aggregate,
            'syntactic_style_aggregate': syntactic_aggregate,
            'rhetorical_structure_aggregate': rhetorical_aggregate,
            'academic_stance_aggregate': stance_aggregate,
            'stable_styles': stable_styles,
            'confidence_levels': {
                'high_confidence': '稳定出现在>60%论文中的风格',
                'medium_confidence': '部分一致的风格（30-60%论文）',
                'unstable': '不稳定的风格（<30%论文，忽略）'
            }
        }
        
        return report
    
    def save_aggregation_report(self, output_path: str, report: Dict):
        """保存聚合分析报告"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"聚合分析报告已保存到: {output_path}")


# 使用示例
if __name__ == "__main__":
    aggregator = CrossPaperAggregator("/mnt/g/project/PaperSkill/analysis/simple_style_analyses.json")
    report = aggregator.generate_aggregation_report()
    aggregator.save_aggregation_report("/mnt/g/project/PaperSkill/analysis/aggregation_report.json", report)