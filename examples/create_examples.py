"""
示例库规范
"""
import json

# 示例库JSONL格式规范
example_format = {
    "paper_id": "论文标识符（如文件名）",
    "section": "section名称（abstract, introduction, related_work, methods, results, discussion, conclusion）",
    "function": "段落功能标签（background, problem_statement, gap, motivation, method_overview, technical_detail, experiment_setup, result_report, comparison, result_explanation, limitation, implication, contribution_summary）",
    "text": "段落文本内容",
    "style_notes": ["风格注释1", "风格注释2", "..."]
}

# 示例库示例
example_samples = [
    {
        "paper_id": "EATDer_Edge-Assisted_Adaptive_Transformer_Detector_for_Remote_Sensing_Change_Detection",
        "section": "abstract",
        "function": "method_overview",
        "text": "Abstract— Change detection (CD) is one of the important research topics in remote sensing (RS) image processing. Recently, convolutional neural networks (CNNs) have dominated the RSCD community. Many successful CNN-based models have been proposed, and they achieved cracking performance. Nevertheless, influenced by the limited receptive field, the CNN-based models are not good at capturing long-distance context dependencies within RS images, negatively impacting their performance. With the appearance of the visual transformer, the above problems have been mitigated. However, the high time costs of the transformer-based models limit their applicability. In addition, previous CD networks (whether CNN-based or transform-based) do not pay attention to the edges of changed areas, reducing the quality of change maps. To overcome the shortcomings discussed above, we propose a new CD method named edge-assisted adaptive transformer detector (EATDer).",
        "style_notes": [
            "使用主动语态",
            "句长适中",
            "先描述问题再提出方法",
            "使用专业术语"
        ]
    },
    {
        "paper_id": "EATDer_Edge-Assisted_Adaptive_Transformer_Detector_for_Remote_Sensing_Change_Detection",
        "section": "introduction",
        "function": "background",
        "text": "HANKS to the development of sensor technologies, a large number of remote sensing (RS) images can be collected every day. These Earth observation data provide rich land-cover information for researchers. As a basic and vibrant interpretation technique, RS change detection (RSCD) plays a vital role in the RS community. It aims to find the changed pixels and regions within the multitemporal RS images, which cover the same areas but are produced at different times [1], [2]. The accurate RSCD results contribute to many RS applications, including land-cover analysis [3], object detection [4], disaster monitoring [5], and scene understanding [6], [7], [8], [9].",
        "style_notes": [
            "使用文献引用",
            "描述研究背景",
            "说明应用价值",
            "使用专业术语"
        ]
    },
    {
        "paper_id": "EATDer_Edge-Assisted_Adaptive_Transformer_Detector_for_Remote_Sensing_Change_Detection",
        "section": "introduction",
        "function": "gap",
        "text": "In the past, numerous methods have been developed for RSCD with the help of traditional machine learning [10], [11]. Those methods mainly rely on algebra and transformation techniques. The algebra-based methods, such as change vector analysis [12], are used to determine the changed pixels by performing the common algebraic operations on the original image space. The transformation-based approaches, such as principal component analysis [13], are habituated to mapping RS images into suitable feature spaces for deciding the changed areas. Although the above methods are feasible, their performance cannot meet what we expected due to the hand-crafted features, which are not able to represent the complex contents within RS images. For example, the pseudo variation issues (see Fig. 1) caused by illumination and shadows are hardly addressed using only the low-level visual features.",
        "style_notes": [
            "使用让步句（Although...）",
            "指出现有方法的局限性",
            "提供具体例子",
            "使用文献支持"
        ]
    },
    {
        "paper_id": "EATDer_Edge-Assisted_Adaptive_Transformer_Detector_for_Remote_Sensing_Change_Detection",
        "section": "methods",
        "function": "method_overview",
        "text": "The framework of the proposed EATDer is shown in Fig. 3. It mainly consists of a Siamese encoder and an edge-aware decoder. Each branch in the Siamese encoder encloses three self-adaption vision transformer (SAVT) blocks, which aim to capture the local and global information within RS images. Also, two branches are connected by full-range fusion modules (FRFMs), which focus on mining the temporal clues among bi-temporal RS images and pointing out the changed/unchanged messages. The edge-aware decoder first integrates the multiscale features obtained by the encoder using a restoring block. Then, it enhances the combined features by a refining block. Finally, based on the refined features, both the change and edge detection results can be produced.",
        "style_notes": [
            "使用图表示（Fig. 3）",
            "描述整体架构",
            "使用专业术语",
            "结构清晰"
        ]
    }
]

# 保存示例库规范
with open("/mnt/g/project/PaperSkill/examples/example_format.json", 'w', encoding='utf-8') as f:
    json.dump(example_format, f, indent=2, ensure_ascii=False)

# 保存示例样本
with open("/mnt/g/project/PaperSkill/examples/example_samples.jsonl", 'w', encoding='utf-8') as f:
    for example in example_samples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print("示例库规范已保存到: /mnt/g/project/PaperSkill/examples/example_format.json")
print("示例样本已保存到: /mnt/g/project/PaperSkill/examples/example_samples.jsonl")