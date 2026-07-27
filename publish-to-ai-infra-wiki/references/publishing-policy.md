# AI Infra Wiki Publishing Policy

## 1. Global goal

Optimize the Wiki for:

- clear navigation;
- reusable knowledge;
- gradual formation of a personal professional knowledge system;
- fast retrieval by both the user and an agent.

Do not maximize page count. Prefer a small number of stable pages with clear names, boundaries, and indexes.

## 2. Learning document versus Wiki page

A learning document may preserve:

- first-contact explanations;
- chronological questions;
- repeated examples;
- recursive prerequisite descent;
- corrections and reorganizations;
- detailed syntax needed at that learning stage.

A Wiki page should preserve:

- the current stable conclusion;
- the minimum model or main flow;
- important responsibilities and boundaries;
- exact evidence and verification baseline;
- optional links to genuinely related deeper pages;
- unresolved or unverified boundaries.

Transform rather than merely shorten. Several learning documents may become one Wiki page, and one broad learning document may yield several stable Wiki pages.

## 3. Classification

### concepts

Use for independently reusable knowledge, including basic language syntax, ABI, linking, JIT/AOT, decorators, function pointers, or framework concepts.

Do not require a concept page to link to the project where it was first learned. A relation is optional and must be useful rather than ceremonial.

### project-understanding

Use for knowledge whose meaning depends on one project:

- architecture and subsystem maps;
- call chains and data flows;
- module, class, or function responsibilities;
- generated-code relationships;
- project-specific runtime and kernel boundaries.

### practice-records

Use for evidence of work performed:

- build and environment procedures;
- debugging investigations;
- code changes and validation;
- performance experiments;
- failures, root causes, and reusable resolutions.

### inbox

Use only when the material is worth retaining but is still unstable, incomplete, or difficult to classify. Revisit it later; do not treat it as published knowledge.

## 4. Recursive model decision

For each recursive or prerequisite document, ask:

1. Is its conclusion now stable?
2. Can it be understood as one knowledge object?
3. Is it likely to be reused?
4. Does it need an independent page for clarity?

Then choose:

- stable and reusable: create or update an independent page;
- small and parent-specific: merge into the parent;
- duplicate of an existing model: merge into that model;
- correction: update the current truth and retain history only in source documents and Git;
- one-off syntax detail: keep in the learning document unless it becomes reusable;
- incomplete: keep in the inbox or source document.

Only preserve `parent model` and `return point` links when the pages are actually part of the same learning dependency. Do not force this relationship onto independently classified syntax or concepts.

## 5. Reading layers

Make a substantial page readable at three depths:

1. **Quick position**: what it is, why it matters, and its boundary.
2. **Working model**: inputs, responsibility, core rule or flow, output, and handoff.
3. **Evidence and optional depth**: concrete example, exact source paths and symbols, related pages when useful, source commit, verification date, and unresolved items.

Use only the layers the topic needs. A simple concept page may remain short.

For source-grounded call chains, put the exact repository-relative source path beside each described layer or handoff. Keep the consolidated evidence list at the end for auditing, but do not make the reader jump there to locate every function. Prefer stable symbols to line numbers; mark generated files and unverified boundaries explicitly.

## 6. Search and naming

- Name pages after the knowledge object or question, not the study sequence.
- Put the most important searchable symbols in the title or opening lines.
- Include a compact keyword line only when the title is insufficient.
- Use exact file paths and symbol names for source-grounded technical pages.
- Search titles, symbols, keywords, and source paths before creating a page.

## 7. Navigation

- Root home: list projects.
- Project home: show the shortest useful map of stable project knowledge.
- Category README: group actual pages within that category.
- Page body: link only directly useful related knowledge.

Navigation and classification are separate decisions. A page may be correctly classified without being linked from an unrelated learning path.

## 8. Source traceability

When available, retain:

```text
source project
source document path
source-code commit
last verified date
verification status
```

Do not copy known-wrong or obsolete explanations into the Wiki. If evidence is incomplete, label the boundary explicitly.

## 9. Publication mapping

Before a multi-document structural publication, present a compact map such as:

```text
source A -> update project-understanding/add-call-chain.md
source B -> create project-understanding/tensor-iterator-bridge.md
source C -> merge into concepts/function-pointers.md
source D -> keep only in the learning docs because it is a one-off syntax detail
```

Require confirmation when the map would rename, merge, split, or replace several existing Wiki pages.
