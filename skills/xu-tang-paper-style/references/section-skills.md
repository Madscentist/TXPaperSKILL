# Section Skills

## skill_abstract

goal: Write one compact paragraph that completes the loop from task importance to existing limitations, proposed method, module rationale, and experimental validation.

structure:
1. Define the task and field importance.
2. Acknowledge existing progress.
3. Use a contrastive move to introduce 1-3 concrete limitations.
4. Introduce the named method.
5. Explain modules in order; each module should solve one limitation.
6. Close with experiments on named datasets or a conservative validation sentence.
7. Mention code availability only when provided.

tone: Objective, restrained, technical, and problem-driven.

preferred_phrases:
- "has become an important topic in ..."
- "Although existing methods have achieved promising performance, ..."
- "To overcome these limitations, this article proposes ..."
- "Specifically, ... is designed to ..."
- "Extensive experiments on ... demonstrate ..."

logic_pattern: background -> limitation -> proposed method -> module rationale -> experimental confirmation.

avoid:
- Long related-work summaries.
- Unsupported exact numbers.
- Promotional language.
- Repeating module descriptions with only synonym changes.

constraints:
- Every module must state the problem it addresses.
- If no result values are provided, do not create them.
- Use "demonstrate", "verify", or "indicate" for evidence-based claims.

## skill_introduction

goal: Establish research necessity, move from broad remote sensing context to a specific gap, and introduce the proposed method and contributions.

structure:
1. Open with the value of remote sensing data or the target task.
2. Define the target task and application relevance.
3. Review major method families.
4. Identify 2-4 limitations.
5. State the problem addressed by this paper.
6. Summarize the proposed framework.
7. List 3-4 contributions.
8. Optionally give article organization.

tone: Explanatory, balanced, and problem-driven.

preferred_phrases:
- "As important earth observation data, ..."
- "Among diverse interpretation techniques, ..."
- "However, these methods still suffer from ..."
- "Motivated by the above observations, ..."
- "The main contributions are summarized as follows."

logic_pattern: broad field -> task importance -> method evolution -> unresolved limitations -> proposed response -> contributions.

avoid:
- Starting with architecture details before motivation.
- Dismissing prior work.
- Vague challenge lists that are not connected to method design.

constraints:
- Each gap must correspond to a later method component.
- Contributions should name both the technical object and its function.
- Do not invent citations.

## skill_related_work

goal: Organize prior work by technical route and use it to clarify the paper's gap.

structure:
1. Divide related work into method families.
2. Summarize the common idea of each family.
3. Mention representative works only when supplied by the user.
4. Identify the shared limitation under the target setting.
5. Transition to how the proposed method differs.

tone: Neutral, compressed, and taxonomic.

preferred_phrases:
- "These methods can be roughly divided into ..."
- "Based on ..., diverse networks have been proposed."
- "Despite their effectiveness, ... remains insufficient."
- "Different from the above methods, ..."

logic_pattern: taxonomy -> representative mechanisms -> shared limitation -> relation to proposed method.

avoid:
- Paper-by-paper citation dumping.
- Unsupported criticism of previous methods.
- Treating related work as a second introduction.

constraints:
- Use only user-provided reference details.
- End each method-family discussion with relevance to the current gap.
- If evidence is thin, use conservative generalization.

## skill_methods

goal: Describe the framework, modules, training strategy, and implementation logic with clear functional boundaries.

structure:
1. Give the overall framework.
2. Define notation or preliminaries.
3. Describe the backbone or base representation.
4. Describe core module 1: input, operation, output, purpose.
5. Describe core module 2: input, operation, output, purpose.
6. Describe additional modules if needed.
7. Define loss functions or training strategy.
8. State implementation or inference flow only when provided.

tone: Rigorous, procedural, and low-rhetoric.

preferred_phrases:
- "Before introducing the proposed method, ..."
- "The overall framework consists of ..."
- "To mine/explore/capture ..., we design ..."
- "In this way, ... can be obtained."
- "Finally, ... is used to ..."

logic_pattern: architecture -> notation -> module decomposition -> objective -> implementation flow.

avoid:
- Saying a module is effective without explaining its mechanism.
- Overlapping module responsibilities.
- Adding formulas, complexity, or hyperparameters not supplied.

constraints:
- Each module needs input, operation, output, and purpose.
- Formula prose must explain variables before or after the equation.
- Do not overstate generalization.

## skill_results

goal: Report experimental evidence and explain how comparisons, ablations, visualizations, and efficiency results support the method.

structure:
1. State datasets, metrics, and settings.
2. Describe compared methods.
3. Report main quantitative results.
4. Compare with baselines or state-of-the-art methods only from supplied data.
5. Explain ablations by module.
6. Add parameter, visualization, or efficiency analysis if provided.
7. Mention limitations or weak cases when available.

tone: Fact-first, conservative, and evidence-linked.

preferred_phrases:
- "The reported results are the average values of ..."
- "Compared with ..., the proposed method achieves ..."
- "The positive experimental results demonstrate ..."
- "This confirms the effectiveness of ..."
- "The ablation studies verify ..."

logic_pattern: setting -> quantitative comparison -> module validation -> qualitative or efficiency evidence -> limitation.

avoid:
- Reporting only the best case.
- Ignoring experimental setup.
- Treating correlation as causation.
- Using "significantly" without statistical or numeric support.

constraints:
- All numbers must come from user input.
- Every conclusion must correspond to a table, figure, or supplied fact.
- Use placeholders or request missing data instead of inventing results.

## skill_discussion

goal: Interpret results, explain likely causes, state applicability, and acknowledge limitations.

structure:
1. Restate the key finding.
2. Explain the likely performance source by mapping to method modules.
3. Discuss abnormal or weak cases.
4. Relate findings to task properties.
5. Acknowledge limitations.
6. Give future work.

tone: Conservative, analytical, and clearly separated from raw result reporting.

preferred_phrases:
- "This may be attributed to ..."
- "One possible reason is that ..."
- "However, when ..., the performance may be limited."
- "Overcoming this limitation will be our future work."

logic_pattern: finding -> explanation -> implication -> limitation -> future direction.

avoid:
- Repeating the results section.
- Generalizing to all remote sensing tasks.
- Presenting speculation as fact.

constraints:
- Mark interpretations with hedging.
- Do not introduce new experiments, data, or references.
- Use a conservative version when discussion evidence is insufficient.

## skill_conclusion

goal: Concisely recap the problem, method, module contributions, experimental evidence, and future work.

structure:
1. State that the article proposes the method for the task.
2. Summarize the core components.
3. Explain the problem addressed by each component.
4. Summarize experimental evidence.
5. End with one future-work sentence if appropriate.

tone: Brief, definite, and restrained.

preferred_phrases:
- "This article proposes a new ..."
- "First, ... is developed to ..."
- "Second, ... is designed to ..."
- "The encouraging results demonstrate ..."
- "Future work will focus on ..."

logic_pattern: method recap -> module recap -> empirical confirmation -> limitation or future work.

avoid:
- New experiments, references, concepts, or metrics.
- Repeating the whole introduction.
- Long background restatement.

constraints:
- Use only information already present in the draft or user input.
- Future work must follow from a known limitation or result.
