# 唐旭教授论文写作风格蒸馏系统 - 最终输出报告

## Part 1. 数据质量判断

### 语料是否足够
**部分足够**。获取到12篇论文的全文内容，但缺乏更多论文的对比分析。

### 风格是否稳定
**初步判断稳定**。从12篇论文中识别出多个稳定风格特征（>60%论文出现）。

### 主要风险点
1. **语料数量有限**：只有12篇论文，可能无法完全代表所有写作风格
2. **期刊格式差异**：不同期刊（IEEE TGRS、Pattern Recognition）可能有不同的格式要求
3. **合作作者影响**：部分论文可能有其他作者的写作风格影响
4. **领域特异性**：主要针对遥感影像处理领域，其他领域可能不适用

### 结论置信度
- **高置信结论**（基于>60%论文）：
  - 句长偏好：短句（75%）
  - 语态偏好：主动语态（100%）
  - 修辞结构：introduction的"background → method"模式（80%）
  - 学术姿态：平衡语气（66.7%）

- **中置信结论**（基于30-60%论文）：
  - 第一人称使用：41.7%使用第一人称
  - 让步句使用：平均使用率0.066
  - 因果句使用：平均使用率0.079

- **不稳定结论**（<30%论文，忽略）：
  - 比较句使用：平均使用率0.003
  - 先总后分结构：平均使用率0.026

## Part 2. 全局风格画像

### 全局语气
**技术导向、客观严谨**。语气偏向技术描述，注重方法创新和实验验证，避免主观表达。

### 全局句法偏好
**结构清晰、术语密集**。使用标准的学术结构，句子结构完整，术语使用规范。

### 全局论证偏好
**问题导向、方法创新**。论文通常针对具体问题提出新方法，强调创新性和实用性。

### 全局高频表达
**技术术语**：
- remote sensing (遥感)
- classification (分类)
- detection (检测)
- network (网络)
- learning (学习)
- transformer (Transformer)
- mamba (Mamba)
- attention (注意力)

**方法描述术语**：
- based on (基于)
- for (用于)
- via (通过)
- with (使用)

**应用场景术语**：
- remote sensing images (遥感影像)
- hyperspectral images (高光谱图像)
- scene classification (场景分类)
- change detection (变化检测)

### 全局禁忌表达
1. **主观评价**：excellent, outstanding, best, superior
2. **夸大词汇**：revolutionary, groundbreaking, state-of-the-art
3. **模糊表达**：maybe, perhaps, might be
4. **口语化表达**：缩写、俚语
5. **过度承诺**：解决所有问题、完美方案

## Part 3. 分section skill（7个）

### 1. skill_abstract
```json
{
  "section": "abstract",
  "goal": ["简洁概括论文的核心贡献", "说明研究问题和动机", "简要描述方法创新", "突出主要实验结果", "吸引读者兴趣"],
  "structure": ["研究背景与问题（1-2句）", "方法创新（1-2句）", "技术特点（1-2句）", "实验结果（1-2句）", "意义与贡献（1句）"],
  "tone": ["客观、简洁、准确", "避免主观评价", "使用专业术语", "一般现在时描述方法", "一般过去时描述实验"],
  "preferred_phrases": ["This paper proposes... for...", "The proposed method... by...", "Experimental results on... demonstrate...", "Compared with... methods, our approach...", "The main contributions are..."],
  "logic_pattern": ["背景 → 问题 → 方法 → 结果 → 贡献"],
  "avoid": ["主观评价：excellent, outstanding, best, superior", "夸大词汇：revolutionary, groundbreaking, state-of-the-art", "模糊表达：maybe, perhaps, might be", "口语化表达：缩写、俚语", "过度承诺：解决所有问题、完美方案"],
  "constraints": ["长度：150-250词", "结构：单一段落或2-3个短段落", "术语：使用领域标准术语", "数据：包含关键实验结果数据", "创新点：明确说明主要创新", "不编造事实、数字、引用", "不引入新实验结果"]
}
```

### 2. skill_introduction
```json
{
  "section": "introduction",
  "goal": ["介绍研究领域和背景", "指出现有方法的不足和问题", "提出本文的方法和创新", "说明论文的主要贡献", "引导读者理解论文结构"],
  "structure": ["研究背景（2-3段）", "现有方法的局限性（1-2段）", "本文方法的提出（1-2段）", "主要贡献（1段）", "论文结构说明（可选）"],
  "tone": ["客观、严谨、有说服力", "使用文献支持观点", "避免过度批评现有方法", "强调创新性和必要性"],
  "preferred_phrases": ["In recent years, ... has attracted increasing attention", "However, existing methods still face challenges", "To address these issues, we propose...", "The main contributions of this paper are:", "First, ... Second, ... Finally, ..."],
  "logic_pattern": ["background → gap → method → contribution"],
  "avoid": ["过度批评现有方法", "夸大研究意义", "使用第一人称过多", "缺乏文献支持", "逻辑不连贯"],
  "constraints": ["长度：800-1200词", "引用：至少15-20篇参考文献", "结构：背景→问题→方法→贡献", "贡献：明确列出2-4个主要贡献", "不编造研究背景", "不夸大方法创新性"]
}
```

### 3. skill_related_work
```json
{
  "section": "related_work",
  "goal": ["全面回顾相关领域的研究", "分类整理现有方法", "指出现有方法的优缺点", "为本文方法提供理论依据", "突出本文方法的创新点"],
  "structure": ["研究领域概述（1段）", "方法分类（2-4个类别）", "各类方法详细分析（每类2-3段）", "现有方法的总结（1段）", "本文方法的定位（1段）"],
  "tone": ["客观、全面、有条理", "使用文献综述的语气", "避免主观评价", "强调分类和比较"],
  "preferred_phrases": ["Existing methods can be categorized into...", "The first category includes...", "The second category focuses on...", "Compared with these methods, our approach...", "In summary, existing methods..."],
  "logic_pattern": ["领域概述 → 方法分类 → 各类分析 → 总结 → 本文定位"],
  "avoid": ["简单罗列文献", "缺乏分类和比较", "主观评价现有方法", "遗漏重要文献", "与introduction重复"],
  "constraints": ["长度：1000-1500词", "引用：至少30-40篇参考文献", "分类：至少2-3个主要类别", "比较：突出各类方法的优缺点", "不遗漏重要相关工作", "不重复introduction内容"]
}
```

### 4. skill_methods
```json
{
  "section": "methods",
  "goal": ["详细描述提出的方法", "说明方法的技术细节", "解释方法的创新点", "提供方法的理论依据", "使读者能够理解和复现"],
  "structure": ["方法概述（1-2段）", "整体架构（1-2段）", "各个模块详细描述（每个模块2-3段）", "技术细节和公式（根据需要）", "训练和优化策略（1-2段）"],
  "tone": ["技术性、精确、清晰", "使用被动语态描述过程", "避免主观评价", "强调技术细节"],
  "preferred_phrases": ["The proposed method consists of...", "As shown in Fig. X, ...", "The main components include...", "Specifically, ...", "The training process involves..."],
  "logic_pattern": ["overview → technical details"],
  "avoid": ["过于简略的描述", "缺乏技术细节", "使用模糊表达", "缺乏公式和图表", "重复related work内容"],
  "constraints": ["长度：1500-2500词", "图表：至少3-5个图表", "公式：关键算法需要公式描述", "细节：足够详细的描述以支持复现", "不遗漏关键技术细节", "不引入未定义术语"]
}
```

### 5. skill_results
```json
{
  "section": "results",
  "goal": ["展示实验结果和性能", "与现有方法进行比较", "分析方法的有效性", "验证方法的创新点", "提供定量的结果分析"],
  "structure": ["实验设置（1-2段）", "数据集和评估指标（1段）", "定量结果（2-3段）", "定性结果（1-2段）", "消融实验（1-2段）", "与现有方法比较（2-3段）"],
  "tone": ["客观、准确、有说服力", "使用数据和图表支持", "避免主观评价", "强调性能提升"],
  "preferred_phrases": ["As shown in Table X, ...", "Our method achieves...", "Compared with baseline methods, ...", "The results demonstrate that...", "From Fig. X, we can observe that..."],
  "logic_pattern": ["setup → results → comparison"],
  "avoid": ["选择性展示结果", "缺乏比较和分析", "使用模糊描述", "缺乏统计显著性", "过度解释结果"],
  "constraints": ["长度：1500-2000词", "表格：至少3-5个结果表格", "图表：至少2-4个可视化结果", "比较：与至少5-8个现有方法比较", "消融实验：验证各模块有效性", "不编造实验结果", "不遗漏重要比较方法"]
}
```

### 6. skill_discussion
```json
{
  "section": "discussion",
  "goal": ["解释实验结果的意义", "分析方法的优缺点", "讨论方法的局限性", "提出未来改进方向", "总结研究的主要发现"],
  "structure": ["结果分析（2-3段）", "方法优势（1-2段）", "方法局限性（1-2段）", "未来工作（1段）", "总结（1段）"],
  "tone": ["客观、分析性、反思性", "使用hedge词表达谨慎", "避免过度承诺", "强调学习和改进"],
  "preferred_phrases": ["The results suggest that...", "One possible explanation is...", "However, there are still limitations...", "Future work could focus on...", "In conclusion, ..."],
  "logic_pattern": ["结果解释 → 优势分析 → 局限讨论 → 未来方向 → 总结"],
  "avoid": ["重复results内容", "缺乏深度分析", "忽略局限性", "过度承诺", "缺乏未来方向"],
  "constraints": ["长度：800-1200词", "分析：深入解释结果原因", "局限：诚实承认方法不足", "未来：提出具体改进方向", "不重复results数据", "不夸大方法意义"]
}
```

### 7. skill_conclusion
```json
{
  "section": "conclusion",
  "goal": ["总结论文的主要贡献", "强调方法的创新点", "说明研究的意义", "提出未来工作方向", "给读者留下深刻印象"],
  "structure": ["研究总结（1-2段）", "主要贡献（1段）", "研究意义（1段）", "未来工作（1段）", "结束语（1句）"],
  "tone": ["简洁、有力、有说服力", "使用现在完成时总结", "避免引入新信息", "强调实际应用价值"],
  "preferred_phrases": ["In this paper, we have proposed...", "The main contributions include...", "Experimental results demonstrate that...", "Future work will focus on...", "We believe that..."],
  "logic_pattern": ["总结 → 贡献 → 意义 → 未来 → 结束"],
  "avoid": ["重复abstract内容", "引入新信息", "过度承诺", "缺乏未来方向", "过于简略"],
  "constraints": ["长度：300-500词", "贡献：明确列出主要贡献", "意义：说明实际应用价值", "未来：提出具体改进方向", "不引入新实验结果", "不重复详细内容"]
}
```

## Part 4. 示例库规范

### JSONL格式规范
```json
{
  "paper_id": "论文标识符（如文件名）",
  "section": "section名称（abstract, introduction, related_work, methods, results, discussion, conclusion）",
  "function": "段落功能标签（background, problem_statement, gap, motivation, method_overview, technical_detail, experiment_setup, result_report, comparison, result_explanation, limitation, implication, contribution_summary）",
  "text": "段落文本内容",
  "style_notes": ["风格注释1", "风格注释2", "..."]
}
```

### 示例样本
```json
{
  "paper_id": "EATDer_Edge-Assisted_Adaptive_Transformer_Detector_for_Remote_Sensing_Change_Detection",
  "section": "abstract",
  "function": "method_overview",
  "text": "Abstract— Change detection (CD) is one of the important research topics in remote sensing (RS) image processing...",
  "style_notes": ["使用主动语态", "句长适中", "先描述问题再提出方法", "使用专业术语"]
}
```

## Part 5. Prompt模板

### 通用Prompt模板结构
```json
{
  "section": "section名称",
  "prompt_template": "你是一个学术论文写作助手。请根据以下要求撰写论文的{section_name}部分。\n\n【写作目标】\n- 目标1\n- 目标2\n...\n\n【结构要求】\n1. 结构步骤1\n2. 结构步骤2\n...\n\n【语气要求】\n- 语气1\n- 语气2\n...\n\n【常用句式】\n- 句式1\n- 句式2\n...\n\n【逻辑模式】\n- 模式1\n- 模式2\n...\n\n【禁用表达】\n- 禁用1\n- 禁用2\n...\n\n【写作约束】\n- 约束1\n- 约束2\n...\n\n【重要提醒】\n1. 不要编造事实、数字、引用\n2. 不要引入新的实验结果\n3. 不要跨section写内容\n4. 请先输出提纲，再输出正文\n5. 风格要接近导师风格，但不得机械照抄原文\n\n【提纲格式】\n请先输出以下格式的提纲：\n1. [段落功能] 段落主要内容概述\n2. [段落功能] 段落主要内容概述\n...\n\n【正文格式】\n然后按照提纲输出完整正文。\n\n【输入信息】\n请提供以下信息以生成更准确的{section_name}：\n- 论文标题：\n- 研究领域：\n- 主要方法：\n- 关键创新点：\n- 主要实验结果：\n- 参考文献（如有）："
}
```

## Part 6. 风格评分表

### 评分维度（1-5分制）
1. **风格相似度**：与导师风格的一致性
2. **语气一致性**：整个section语气的统一性
3. **section匹配度**：内容与section功能的匹配程度
4. **结构完整性**：是否包含所有必要部分
5. **事实忠实度**：信息的准确性和可靠性
6. **术语一致性**：术语使用的准确性和规范性

### 评分标准
- **1分**：完全不符合要求
- **2分**：基本不符合要求
- **3分**：部分符合要求
- **4分**：大部分符合要求
- **5分**：完全符合要求

### 合格标准
- **总分≥3分**，且没有1分的维度
- **优秀标准**：总分≥4分，且没有2分及以下的维度

## Part 7. 总结（最核心风格）

### 1. 这位导师最核心的写作风格是什么
**技术导向、客观严谨、结构清晰**。导师的写作风格注重技术细节，使用客观、专业的语气，结构组织清晰，术语使用规范。

### 2. 最值得迁移的不是哪些表面词汇，而是哪些深层习惯
**深层习惯**：
- **问题导向**：先描述问题和背景，再提出方法
- **结构化表达**：使用清晰的段落结构和逻辑连接
- **技术细节**：注重方法的技术细节和实现
- **实验验证**：强调实验结果和性能比较
- **创新性强调**：突出方法的创新点和贡献

### 3. 未来调用时最应该优先加载哪3个skill
1. **introduction skill**：最核心的部分，决定论文的整体框架和逻辑
2. **methods skill**：技术核心，决定论文的技术深度和可复现性
3. **results skill**：实验验证，决定论文的可信度和说服力

## 使用建议

### 写作新论文时
1. 先加载introduction skill，按照"background → gap → method → contribution"结构写作
2. 加载methods skill，按照"overview → technical details"结构描述方法
3. 加载results skill，按照"setup → results → comparison"结构展示结果
4. 使用其他skill补充完善其他部分

### 改进现有论文时
1. 对照skill检查现有内容是否符合导师风格
2. 识别不符合的部分进行修改
3. 使用评分表评估改进效果
4. 不断迭代优化

### 持续改进
1. 收集更多论文进行分析
2. 更新和完善skill
3. 扩充示例库
4. 优化prompt模板

---

**最终输出时间**：2024年4月16日
**系统版本**：v1.0
**分析论文数量**：12篇
**生成Skill数量**：7个section
**核心价值**：提供可复用的学术论文写作框架和风格指导