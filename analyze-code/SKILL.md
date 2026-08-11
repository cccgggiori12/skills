---
name: analyze-code
description: "Use when source code itself is the primary target: analyzing a named repository, path, symbol, snippet, generated artifact, build script, or configuration; tracing a call chain; verifying a claim against code; or when the user invokes $analyze-code. Do not use for general software concepts, logs, plans, summaries, or repository context alone. During an active $guide-technical-learning-experiment session, a named source object or brief evidence spot-check is insufficient; use only when the user explicitly requests dedicated source inspection, call-chain tracing, line-by-line analysis, or $analyze-code."
---

# Analyze Code

## Core Principle

Ground the explanation in the actual repository whenever the code is available. Verify exact files, symbols, definitions, uses, and generated sources instead of explaining from memory.

Choose the analysis strategy from three factors:

```text
target type x requested depth x minimum sufficient mental model
```

Do not measure completeness by the amount of detail. A complete explanation answers the current question, exposes the model boundary, and makes the next useful expansion point clear.

## 1. Choose the Depth

Use quick orientation when the user asks a narrow question, requests a short answer, or only needs to locate an object's responsibility or destination.

- Inspect the target and only the context required to answer correctly.
- Lead with the direct answer.
- State the object's role, relevant input or context, key effect, output or handoff, and boundary.
- Avoid expanding the full architecture unless the local meaning depends on it.

Use deep learning analysis when the user asks for a complete explanation, wants to learn the code, requests data flow or a call chain, or keeps drilling into successive layers.

- Start with the minimum sufficient mental model before adding details.
- Explain syntax, data flow, control flow, state changes, side effects, normal and exceptional paths, and surrounding architecture when relevant.
- Use a concrete input, before/after state, equivalent simpler code, or compact flow when it materially improves understanding.
- Continue to a stable semantic boundary such as a public API, storage operation, device kernel, runtime API, external library, or user-specified endpoint.

Infer the depth from the request. Do not turn a precise spot question into a full-system lecture, and do not give a wrapper-only answer when the user asks for end-to-end understanding.

## 2. Classify the Target

Adapt the emphasis to the object being analyzed:

- **Repository or project**: explain the problem it solves, entry points, directory and module responsibilities, build or run path, main data flows, and external boundaries.
- **Module or subsystem**: explain its responsibility, public interface, internal components, dependencies, state lifecycle, data flow, control flow, and what remains outside its boundary.
- **Feature or call chain**: identify the start and end, layer responsibilities, handoff points, values transformed at each layer, branches, fallback paths, and the final semantic boundary.
- **Class or struct**: explain the represented concept, owned or referenced state, invariants, construction and destruction, key methods, and how those methods cooperate.
- **Function or method**: explain its role, parameter types and sources, return or mutation destination, internal blocks, side effects, callers, callees, special cases, and failure paths.
- **Code block or several lines**: explain the overall intent, execution order, variable changes, control and data dependencies, and the syntax that connects the lines.
- **Single line or expression**: parse the syntax first; explain types, names, operators, evaluation order, lifetime or ownership implications, equivalent simpler code, and the line's local effect.
- **Macro, template, or lambda**: show an expanded, instantiated, or equivalent form when possible; explain parameters or captures, type deduction, generated object or code, lifetime, and use sites.
- **Generated code or configuration**: connect generated output to its generator and source schema, or connect configuration fields to their consumers and runtime effects.

Analyze the requested object first. Expand surrounding architecture only when it is needed to explain that object.

## 3. Locate and Bound the Evidence

- Search exact names with `rg` and open relevant code with line numbers.
- Locate definitions and uses proportionally to the selected depth.
- For functions and classes, inspect immediate callers or construction sites and important callees when needed.
- For macros and templates, locate the definition and a concrete expansion or instantiation site.
- For generated code, identify both the generated artifact and the generator input.
- For configuration, identify the reader or consumer and the behavior it controls.
- Distinguish source-confirmed facts, reasonable inferences, and runtime behavior that has not been verified.

## 4. Build the Minimum Sufficient Mental Model

Before expanding details, build the smallest model that can correctly explain the user's current target:

1. Identify what the code object is.
2. State the problem it solves and its responsibility.
3. Identify what enters it: data, state, configuration, or preconditions.
4. State the core rule, transformation, or coordination it performs.
5. Identify what it produces, mutates, or hands off.
6. State what it intentionally leaves outside its boundary.

Validate the model with one concrete example when useful. For abstract data flow, walk one value through the model. For syntax, show an equivalent simpler expression. For stateful code, show the relevant before and after state.

Introduce another concept or follow another layer only when:

- the user asks to go deeper;
- the current model cannot explain the observed code or behavior;
- an important exception contradicts the current model;
- the next boundary is required to answer the current question; or
- a new concept is necessary to connect two existing models.

Otherwise, name the possible expansion point without explaining it yet.

For a complex system, first decompose it into minimal models and their interfaces:

```text
model A: responsibility, input, rule, output, boundary
    -> handoff: data, control, assumptions
model B: responsibility, input, rule, output, boundary
```

Deepen one model at a time. Emphasize what crosses each boundary and which layer owns each responsibility.

## 5. Recurse Only Through Blocking Models

Use recursive decomposition when the current model still depends on something the user must understand first. Reuse the same six-part minimum model at every level.

Distinguish two recursion directions:

- **Structural recursion** follows implementation containment, such as project -> subsystem -> module -> function -> code block -> expression.
- **Prerequisite recursion** explains a concept required by the parent model, such as a Python decorator, function pointer, dispatch table, object protocol, or dynamic linking.

Use a hybrid policy:

1. Preserve the original question, current parent model, reason for descending, and exact return point.
2. Identify no more than one to three candidate child models.
3. Automatically expand only the smallest child that blocks understanding, normally one level per response.
4. Explain that child with the minimum model and one concrete example when useful.
5. State the child's conclusion and explicitly connect it back to the parent.
6. Return to the parent question unless another child still blocks it or the user explicitly asks to descend again.
7. Name non-blocking dependencies without expanding them.

Treat statements such as “不懂”, “比较乱”, “没接触过”, or “基础较弱” as signals to look for a blocking prerequisite. Also consider recursion when the user repeatedly cannot follow a handoff, the explanation relies on undefined syntax or an unfamiliar object model, or the outer responsibility is clear but the next relevant line is not.

Honor explicit controls such as:

- “对 X 继续递归”, “把 X 建成最小模型”, or “对 X 下钻一层”;
- “展开当前模型的前置知识” or “列出当前模型树”;
- “回到上一层”, “回到原问题”, or “这个模型我懂了，继续”;
- “停止递归，只给结论”.

For extended learning, optionally maintain a compact model tree with statuses such as `[已理解]`, `[当前]`, `[待学习]`, and `[暂缓]`. Do not show the tree when it adds more ceremony than clarity.

Stop descending when the current idea can be explained using concepts the user already understands, a concrete example is sufficient, a stable semantic boundary is reached, deeper detail is irrelevant to the original question, or the user asks to stop or return. Do not recurse merely because another dependency exists.

## 6. Explain Behavior at the Right Granularity

- For functions, map each parameter to its source and each return value, mutation, reference, pointer, or output parameter to its destination.
- Group function bodies into purpose-driven blocks rather than explaining every token mechanically.
- For code blocks and expressions, explain line-by-line or token-by-token syntax when that is the user's actual question.
- Distinguish values passed unchanged from values allocated, copied, cast, resized, validated, captured, moved, or transformed.
- Cover normal, fallback, error, early-return, warning, and special-case paths only to the degree relevant to the selected depth.
- Call out behavior controlled by types, shapes, devices, dispatch keys, environment variables, build flags, ownership, or lifetime.
- State what an object does not do when that prevents a responsibility-boundary mistake.

## 7. Teach, Do Not Merely Restate

Prefer the smallest learning aid that makes the idea concrete:

- one realistic input walking through the code;
- a compact caller-to-callee or data-flow chain;
- an equivalent desugared expression;
- a before/after state snapshot;
- a macro expansion, template instantiation, or lambda closure approximation;
- an explanation of why the code is written this way and what would change if a key line changed.

Introduce terminology after establishing an intuitive model when the user is unfamiliar with the subject. Use the user's language and calibrate detail to their background.

## 8. Present the Answer Naturally

- Lead with the outcome or minimum model.
- Use headings derived from the actual question instead of a fixed template.
- In quick orientation, keep only the facts needed to answer the narrow question.
- In deep analysis, present the minimum model first, then expand the requested layers.
- Include exact file paths, symbols, and line-local evidence.
- Use a compact flow only when relationships are easier to understand visually.
- End by stating the current boundary and the one or two most useful next expansion points.

For a saved code-reading document, include a numbered browsing path when it improves later lookup:

```markdown
## 浏览路径

1. `path/to/entry`
2. `path/to/target`
3. `path/to/next_boundary`
```

## Quality Rules

- Preserve the user's requested scope and depth.
- Keep framework-specific concepts out of generic explanations unless the target actually uses them.
- Do not conflate wrappers, adapters, dispatch, generated code, host APIs, runtimes, and final kernels.
- Do not hide important syntax behind an architecture summary when the user asks about one line or expression.
- Do not expand a dependency merely because it exists; pass it through the expansion gate.
- After recursive explanation, reconnect the child model to its parent and resume the original question at the saved return point.
- Mark uncertainty explicitly and avoid inventing runtime behavior.
- Offer debugging hooks only when tied to verified code and useful for the requested depth.
