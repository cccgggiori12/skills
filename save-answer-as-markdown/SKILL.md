---
name: save-answer-as-markdown
description: Save a prior or current assistant answer as a Markdown document. Use when the user asks to output, export, save, persist, or write an answer/explanation/analysis/plan as an .md file, especially when they request a Chinese filename, numbered browsing path, code-reading notes, project documentation, a reusable study note, or an optional handoff for later publication into the personal AI Infra Wiki.
---

# Save Answer As Markdown

## Workflow

1. Identify the content to save.
   - If the user says "刚才/上面/这个回答", use the most recent relevant assistant answer.
   - If the user asks to save multiple answers, merge them into one coherent document and preserve the original intent.
   - If the referenced content is ambiguous and a wrong document would be risky, ask one concise clarification.

2. Choose the output location.
   - If the user specifies a target directory, use it and do not add a weekly subdirectory unless requested.
   - Otherwise, for project-related content in a code repository, prefer `docs/cg_personal/<ISO-year>-W<week>/`.
   - Determine the week in this order: an explicitly requested week, the reporting period clearly stated by the content, then the current date in the user's or session's timezone.
   - Use ISO 8601 weeks (Monday through Sunday) and an ISO week-year label such as `2026-W29`; when a shell is available, `date '+%G-W%V'` gives the correct cross-year label.
   - Interpret `/docs/cg_personal` requests as `<repository-root>/docs/cg_personal/`, not as a system-root directory, unless the user explicitly requests an absolute filesystem path.
   - If the target directory does not exist, create only the minimal needed directory after checking the repo convention.

3. Choose a filename.
   - Use a clear, searchable Chinese filename when the user asks for Chinese naming.
   - Keep `.md` extension.
   - Avoid spaces unless the repo already uses them heavily.
   - Prefer names that describe the question, not generic names like `note.md`.

4. Structure the Markdown.
   - Start with a concise H1 title matching the filename topic.
   - Preserve the original answer's reasoning order when it is already clear; merge repetition and add only the context needed for independent reading.
   - Prefer a natural opening paragraph that introduces the question and key conclusion together instead of forcing separate `问题背景` and `先给结论` sections.
   - Derive section titles from the subject being explained, such as `Zeus 从哪里接手` or `真正的根因`, rather than repeatedly using generic labels such as `执行过程` or `总结`.
   - Use as few sections as the material needs. A short answer may need only the H1 and several paragraphs.
   - Keep the document self-contained and silently check that it covers the relevant context, conclusion, evidence or process, exact commands/paths/symbols, data flow, verified result, boundaries, and unresolved items. Treat these as a completeness checklist, not mandatory headings.
   - For code-reading documents, include a `浏览路径` section with Arabic-numbered items such as `1.`, `2.`, `3.` when the user asks for browsing order or easy lookup.
   - Use fenced code blocks for commands, code, logs, and call chains.
   - Use tables only when comparison improves scanning.

5. Preserve technical fidelity.
   - Do not invent new results beyond what was actually observed.
   - If a result came from a command, include the key output lines or a concise summary.
   - If a path or symbol was verified, include exact file paths and symbol names.
   - Clearly distinguish source-code-confirmed facts from inferred runtime behavior.

6. Add an optional Wiki handoff.
   - Add this only when the user asks to publish later, requests a Wiki handoff, or identifies the document as part of a recursive model tree. Do not add it to every Markdown document.
   - Keep it short and omit fields that do not apply.
   - Record the main topic, current model, document role, reuse scope, maturity, source-code baseline, and source path when known.
   - Use document roles such as `主线`, `前置模型`, `局部例子`, `理解纠正`, or `实践记录`.
   - Record a parent model and return point only when a real recursive learning relationship exists. Do not force project links onto independently classified syntax or concept documents.
   - Treat the handoff as publication input, not as a command to modify or push the Wiki.

7. Write and verify.
   - Use `apply_patch` for repository file edits when possible.
   - After writing, verify with `sed -n '1,80p'`, `wc -l`, or equivalent lightweight reads.
   - Final response should include a clickable file link and a short confirmation of what was saved.

## Adaptive Document Patterns

For a call-chain explanation, use topic-specific headings:

```markdown
# PyTorch add 如何进入 Zeus kernel

`add_stub` 不是最终 kernel，而是 PyTorch 向设备实现交接的分发点。

## 从 Python 入口走到 Dispatcher
## Zeus 从哪里接手
## TensorIterator 准备了什么
## 最终计算落在哪里
## 源码查阅顺序
1. `path/to/entry.cpp`
2. `path/to/kernel.cpp`
```

For a debug walkthrough, follow the investigation:

```markdown
# add 算子调试实操复盘

开篇说明现象和最终原因。

## 最初观察到的现象
## 哪条线索缩小了范围
## 真正的根因
## 采取了什么处理
## 如何确认问题已经解决
## 下次可以复用的经验
```

For a weekly report:

```markdown
# 2026 年第 29 周工作总结

## 本周围绕什么展开
## 已经推进到哪里
## 形成了哪些关键判断
## 遇到的问题及处理结果
## 尚未解决的事项
## 下周准备继续推进什么
```

For an optional Wiki handoff:

```markdown
## Wiki 交接

- 主主题：add 调用链
- 当前模型：TensorIteratorBridge
- 文档角色：前置模型
- 父模型：impl_add_Tensor 到 add_stub
- 返回位置：完成输入输出准备后继续进入 add_stub
- 复用范围：torch_zeus 项目内
- 当前状态：已理解
- 源码基线：`<commit>`
```
