# PaperSkill v2 — 多文风学术写作 SKILL 平台

本项目是从单一导师风格进化为「多文风可选、自动蒸馏、即插即用」的论文写作 SKILL 平台。

## 核心设计

- **作者空间（Author Namespace）**：每位导师/作者有独立的 `authors/<id>/` 目录
- **模板化工厂（Style Factory）**：新增一位导师只需放入 PDF，跑一条命令
- **Hermes 主控 SKILL**：`paper-writing-assistant` 负责解析意图、选择文风、指挥写作流程

## 目录结构

```
G:\project\PaperSkill\n├── authors/
│   └── xu-tang/                  # 作者资产
│       ├── papers/                # 原始论文 PDF
│       ├── extracted_texts/       # 提取的文本
│       ├── analysis/              # 聚合分析报告
│       ├── skills/                # 7 个 section skill JSON
│       ├── prompts/               # 7 个 section prompt JSON
│       ├── examples/              # 示例库
│       └── rubric.json            # 评分表
├── factory/                     # 自动化脚本
│   ├── run_pipeline.py          # 一键跑完整流程
│   ├── llm_client.py            # LLM 调用客户端
│   ├── generate_skill.py        # 生成 skill（混合模式）
│   ├── build_prompts.py         # 生成 prompts
│   ├── build_rubric.py          # 生成 rubric
│   └── compile_hermes_references.py  # 编译 Hermes references
├── registry.json                # 文风注册表 + 默认作者
├── hermes-skills/               # Hermes SKILL 入口
│   ├── paper-writing-assistant/
│   │   └── SKILL.md             # 主控 SKILL
│   └── author-styles/
│       └── xu-tang-paper-style/
│           ├── SKILL.md         # 子文风 SKILL
│           └── references/      # section-skills.md + prompts-and-rubric.json
└── README-v2.md
```

## 快速开始

### 1. 给现有作者重新生成资产

如果你已经有聚合分析报告，可以跑完整流程（使用外部 LLM）：

```bash
cd /mnt/g/project/PaperSkill
python factory/run_pipeline.py --author xu-tang
```

环境变量设置（可选，用于 LLM 增强）：
```bash
export PAPERSKILL_BASE_URL="http://localhost:18080/v1"
export PAPERSKILL_MODEL="gemma4:31b-64k"
export PAPERSKILL_API_KEY=""  # 本地模型可为空
```

如果你希望由 **Hermes 直接充当 LLM**（无需外部 API），请使用两阶段流程：

```bash
# 第一阶段：只生成骨架
python factory/run_pipeline.py --author xu-tang --no-llm

# 第二阶段：在 Hermes 对话中，让 Hermes 读取 authors/xu-tang/analysis/aggregation_report.json
# 然后为每个 section 手动/智能填充 preferred_phrases 和 logic_pattern

# 第三阶段：重新生成 prompts 和 references
python factory/rebuild_after_enrich.py --author xu-tang
```

### 2. 新增一位导师文风（Hermes 模式）

第一步：准备论文
```bash
mkdir -p authors/prof-zhang/papers
cp /path/to/papers/*.pdf authors/prof-zhang/papers/
```

第二步：提取文本并生成聚合分析报告（复用你现有的提取和分析脚本）

第三步：生成骨架
```bash
python factory/run_pipeline.py --author prof-zhang --no-llm
```

第四步：让 Hermes 为每个 section 填充文风特征
- Hermes 读取 `authors/prof-zhang/analysis/aggregation_report.json`
- 为 7 个 section 分别生成 `preferred_phrases` 和 `logic_pattern`
- 写入 `authors/prof-zhang/skills/skill_*.json`

第五步：同步资产
```bash
python factory/rebuild_after_enrich.py --author prof-zhang
```

第六步：注册到 `registry.json`
手动添加新作者元数据。

### 3. Hermes 中使用

只要 `paper-writing-assistant` 被加载，你可以直接说：

> "帮我写一个 Introduction，关于遥感变化检测的。"

系统会自动使用 `registry.json` 中的 `default_author`（默认唐旭）。

如果你想切换风格：

> "用张教授的风格重写这段 results。"

## 工厂脚本说明

| 脚本 | 作用 |
|------|------|
| `run_pipeline.py` | 一键执行全部流程 |
| `generate_skill.py` | 根据聚合报告生成 7 个 section skill（硬编码骨架 + LLM 提取句式/逻辑） |
| `build_prompts.py` | 从 skill 生成可直接使用的 prompt 模板 |
| `build_rubric.py` | 复制/生成评分表 |
| `compile_hermes_references.py` | 将所有 JSON 编译为 Hermes SKILL 能识别的 references 文件 |

## 未来拓展

- [ ] 向量化 Few-shot：对 examples 做 embedding 检索
- [ ] 自动评分器：`auto_evaluator.py` 自动按 rubric 打分
- [ ] 增量更新：导师发了新论文后只需分析差异并更新 skill
- [ ] 多文风对比：A 导师和 B 导师在 Methods 部分的差异分析

## 注意事项

1. `给我建议` 并不会触发本 SKILL。只有涉及写作、修改、评估或蒸馏时才会调用。
2. 所有生成结果均需人工验证，特别是数据和引用。
3. 不同期刊有不同格式要求，本 SKILL 主要拟合内容风格，不替代格式排版工具。
