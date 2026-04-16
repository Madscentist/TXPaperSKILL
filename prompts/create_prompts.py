"""
Prompt模板
"""
import json
import os

# 为每个section创建Prompt模板
def create_prompt_templates():
    """创建Prompt模板"""
    
    # 通用Prompt模板结构
    def create_section_prompt(section_name, skill_data):
        """创建单个section的Prompt模板"""
        return {
            "section": section_name,
            "prompt_template": f"""你是一个学术论文写作助手。请根据以下要求撰写论文的{section_name}部分。

【写作目标】
{chr(10).join(f'- {goal}' for goal in skill_data['goal'])}

【结构要求】
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(skill_data['structure']))}

【语气要求】
{chr(10).join(f'- {tone}' for tone in skill_data['tone'])}

【常用句式】
{chr(10).join(f'- {phrase}' for phrase in skill_data['preferred_phrases'])}

【逻辑模式】
{chr(10).join(f'- {pattern}' for pattern in skill_data['logic_pattern'])}

【禁用表达】
{chr(10).join(f'- {avoid}' for avoid in skill_data['avoid'])}

【写作约束】
{chr(10).join(f'- {constraint}' for constraint in skill_data['constraints'])}

【重要提醒】
1. 不要编造事实、数字、引用
2. 不要引入新的实验结果
3. 不要跨section写内容
4. 请先输出提纲，再输出正文
5. 风格要接近导师风格，但不得机械照抄原文

【提纲格式】
请先输出以下格式的提纲：
1. [段落功能] 段落主要内容概述
2. [段落功能] 段落主要内容概述
...

【正文格式】
然后按照提纲输出完整正文。

【输入信息】
请提供以下信息以生成更准确的{section_name}：
- 论文标题：
- 研究领域：
- 主要方法：
- 关键创新点：
- 主要实验结果：
- 参考文献（如有）：
"""
        }
    
    # 加载所有skill
    with open("/mnt/g/project/PaperSkill/skills/all_skills.json", 'r', encoding='utf-8') as f:
        all_skills = json.load(f)
    
    # 为每个section创建Prompt模板
    prompts = {}
    for section_name, skill_data in all_skills.items():
        prompts[section_name] = create_section_prompt(section_name, skill_data)
    
    # 保存Prompt模板
    with open("/mnt/g/project/PaperSkill/prompts/all_prompts.json", 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    
    # 为每个section单独保存Prompt文件
    for section_name, prompt_data in prompts.items():
        section_dir = os.path.join("/mnt/g/project/PaperSkill/prompts", section_name)
        os.makedirs(section_dir, exist_ok=True)
        
        prompt_path = os.path.join(section_dir, f"prompt_{section_name}.json")
        with open(prompt_path, 'w', encoding='utf-8') as f:
            json.dump(prompt_data, f, indent=2, ensure_ascii=False)
    
    print("所有Prompt模板已保存到: /mnt/g/project/PaperSkill/prompts/all_prompts.json")
    print("各section的Prompt模板已保存到对应子目录")

# 创建Prompt模板
create_prompt_templates()