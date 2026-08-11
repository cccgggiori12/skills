---
name: guide-technical-learning-experiment
description: "Use only when the user explicitly invokes $guide-technical-learning-experiment to run or resume a multi-hour or multi-day technical-learning experiment, or to evaluate this experimental learning workflow."
---

# Guide Technical Learning Experiment

## Core Principle

Organize learning around completing the current target, not eliminating every unknown term. Preserve useful curiosity by classifying and deferring non-blocking concepts instead of expanding all of them immediately.

Keep this skill experimental and explicitly invoked. Do not turn ordinary questions, one-off source analysis, Markdown saving, or Wiki publication into this workflow.

## Start or Resume

1. Read the named topic workspace when one exists. Restore the original goal, current question, parent model, and exact return point.
2. Otherwise resolve one workspace location and copy `assets/topic-workspace.md`. Prefer the project's established personal-learning directory; do not scatter one file per answer.
3. Classify the primary entry mode:
   - **文档驱动**：从一篇或一组材料建立目标、全文骨架和章节权重。
   - **目标驱动**：从待回答问题定义完成标准，再选择文档、源码、测试、日志或实验作为证据。
   - **问题驱动**：从失败、fallback、性能或行为差异形成最小复现、假设和证据计划。
4. Write the completion condition and explicit non-goals before descending.
5. Build the minimum sufficient model for the current target.

Modes may change as evidence emerges. Preserve the original goal and return point when switching.

## Gate Unknown Concepts

最小模型控制单个概念的下钻深度；未知概念准入门控制需要立即展开的概念数量。**未知不自动等于当前材料的前置知识。**

Classify every unfamiliar concept before expanding it:

- `[阻塞]`：不理解就无法复述当前结论、理解当前 handoff 或继续主线。立即建立最低充分模型。
- `[提及]`：知道一句话职责和边界即可继续。记录最小定位，不展开内部机制。
- `[延后]`：有学习价值但不影响当前目标。写入待学习池。

Use this test: replace the term with “负责某件事的一种机制”. If the learner can still explain the paragraph's conclusion, the object's responsibility, and the handoff, the term is not blocking.

Keep learning priority separate from evidence strength:

```text
学习优先级：[阻塞] / [提及] / [延后]
证据状态：  [映射] / [确认] / [验证] / [待查]
```

On a first pass, take mainline concepts to a working model, supporting concepts to role-and-boundary orientation, and background terms only to recognition. If one section exposes **三个以上真正阻塞项**, stop word-by-word recursion, build their shared prerequisite model, save the return point, and then resume.

## Control Depth and Evidence

Before inspecting more source, tests, or external material, ask:

1. Does the gap block the current minimum model?
2. Is the learner about to record an issue, recommend restructuring, or make a correctness claim?
3. Does it involve ABI, dtype, truncation, fallback, aliasing, synchronization, or another high-risk boundary?
4. Can a local spot-check answer it in roughly ten minutes?

Keep a non-blocking teaching analogy at `[映射]`. Use a small source check for `[确认]`. Move a larger investigation to `[待查]` and return to the mainline. Upgrade to `[验证]` only with test, runtime, or experiment evidence. Separate simulator, real hardware, and closed-vendor boundaries.

Keep brief source spot-checks inside this learning workflow. A named symbol, path, or code term is evidence context, not by itself a mode switch. Apply `analyze-code` only when the user explicitly invokes it or requests a dedicated source-analysis subtask such as line-by-line explanation, a bounded call-chain trace, or analysis of an exact code object as the learning target. Reconnect that subtask to the parent question before continuing.

Examples:

- “`at::Scalar` 在这里承担什么职责，只要最小模型” stays in this skill.
- “追踪 `sub -> add_stub` 的完整源码调用链” applies `analyze-code`.

## Update the Workspace

Update the topic workspace when the user says “纳入本节”, “记录为待查”, “进入下一节/下一个问题”, or “收束今天”. At each checkpoint retain:

- current conclusion and its two status axes;
- unresolved questions and deferred concepts;
- parent question and return point;
- next useful action;
- Wiki candidates, without publishing them.

Use `save-answer-as-markdown` only when the user wants a separate reusable document. Otherwise merge useful material into the one topic workspace.

## Close a Session Safely

On “收束今天”:

1. Write the exact resume point.
2. Separate confirmed conclusions, initial mappings, and unverified questions.
3. Produce a compact source-to-target Wiki candidate map.
4. Copy and fill `assets/experiment-scorecard.md` or append its fields to the workspace.

Do not automatically modify the Wiki. Only after explicit user confirmation, use `publish-to-ai-infra-wiki` to search, classify, rewrite, and validate. Never commit or push unless separately requested.

Run the experiment for 3–5 working days across at least one 文档驱动, one 目标驱动, and one 问题驱动 task. Then recommend keep, revise, or disable based on the scorecards rather than one session.
