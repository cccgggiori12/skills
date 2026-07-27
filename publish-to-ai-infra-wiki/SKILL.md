---
name: publish-to-ai-infra-wiki
description: Curate project learning documents, current explanations, recursive prerequisite notes, concepts, and work records into the personal AI Infra Markdown wiki. Use when the user asks to publish, sync, curate, organize, or 沉淀 content into the Wiki; update an existing Wiki topic; turn detailed study notes into a clear reusable knowledge page; or push an explicitly requested Wiki change to its Git remote.
---

# Publish to AI Infra Wiki

## Purpose

Turn exploratory learning material into the user's current, searchable understanding. Preserve detailed study documents in their source projects; make the Wiki a clear navigation and retrieval layer for both the user and future agents.

Default to `/DATA210/Application/caolx201/ai-infra` when it exists. Verify the actual Wiki root before writing.

Read [publishing-policy.md](references/publishing-policy.md) before deciding how to merge, split, classify, or rewrite source material.

## Workflow

### 1. Resolve the source and target

- Identify the current answer, named Markdown files, recursive study documents, or work record to publish.
- Resolve the source repository root, exact source paths, current commit, and verification status when available.
- Map the source project to the matching Wiki project directory, such as `torch_zeus/`.
- Inspect the Wiki tree, project home, category indexes, Git status, and remote before changing anything.
- Preserve unrelated or pre-existing dirty changes.

### 2. Search before creating

Search the Wiki with `rg` for the proposed title, important symbols, keywords, and source paths.

Choose one operation:

- update an existing page;
- merge into an existing page;
- create one new page;
- split stable reusable models into several pages;
- keep unstable material in `收集箱.md` or leave it only in the source learning document.

Do not assume one source document equals one Wiki page.

For one source with an obvious destination, proceed directly. Before a batch operation that merges, splits, renames, or restructures several pages, show a compact publication map and obtain confirmation.

### 3. Classify content independently

Use the smallest existing structure:

- `concepts/`: reusable concepts or language and framework knowledge;
- `project-understanding/`: project-specific architecture, implementation, call chains, module responsibilities, and data flow;
- `practice-records/`: builds, changes, debugging, tests, experiments, results, and reusable operating experience;
- `收集箱.md`: useful but not yet stable or classifiable material.

Classification is independent from navigation. A basic syntax concept may live in `concepts/` without being linked to a project page. Add relationships only when the source material establishes a real relationship or the user requests one.

### 4. Rewrite for later reading

Convert learning order into knowledge order:

1. lead with a searchable title and a short stable conclusion;
2. give the minimum model or main flow;
3. retain responsibility boundaries, important handoffs, and one useful example;
4. annotate every source-grounded layer or call boundary in place with its exact repository-relative source file and key symbol or statement;
5. retain source commit, last verification, and unresolved points;
6. keep a consolidated source list at the end, but never use that list as a substitute for in-place source locations;
7. move detailed syntax, repeated exploration, and superseded explanations out of the main path;
8. use links for optional depth instead of embedding every recursive explanation.

Use natural topic-specific headings. Do not force every page into one template.

For a source-grounded call chain, make each boundary independently locatable:

```text
PrivateUse1 registration
→ m.impl("add.Tensor", TORCH_FN(wrapper_add_Tensor))
→ torch_zeus/csrc/aten/generated/RegisterZeus.cpp
→ aten::add.Tensor enters the Zeus wrapper
```

- Use repository-relative paths, not only filenames.
- Mark generated files explicitly.
- Prefer stable symbols over line numbers. Include line numbers only when the page freezes a source commit and exact-line evidence is useful.
- If several adjacent symbols are implemented in the same file, one nearby source-location line may cover them, but do not defer all locations to the final source list.
- Label a boundary as unverified instead of guessing its file.

### 5. Handle recursive documents

- Publish a child model separately when it is stable and reusable.
- Merge a small parent-specific prerequisite into the parent page.
- Merge multiple documents about the same model into one current page.
- Update the current page with corrected understanding; do not publish known-wrong intermediate conclusions as parallel truth.
- Keep one-off syntax details in the source document unless they form a reusable concept.
- Preserve parent and return-point links only for genuinely related recursive models.

Never delete the original project learning documents as part of Wiki publication.

### 6. Maintain navigation

- Keep the root `README.md` or home page as the project entry list.
- Keep each project home as the shortest useful map of its current knowledge.
- Create or update a category `README.md` when that category contains real pages.
- Link a page from the nearest useful index, but avoid redundant links in every index.
- Prefer searchable filenames that name the knowledge object; remove learning-sequence names such as `文档3.1` from the Wiki title.

### 7. Verify

Run:

```bash
python <skill-dir>/scripts/validate_wiki.py <wiki-root>
git -C <wiki-root> diff --check
git -C <wiki-root> status --short
```

Inspect changed pages and navigation links. Report the exact created, updated, merged, or intentionally skipped pages.

For source-grounded call-chain pages, also inspect the body and confirm that every described layer or handoff has an in-place repository-relative source location; a passing link validator alone is insufficient.

Do not commit or push unless the user explicitly requests it. When push is requested, verify the remote and upstream first, then confirm the final local/remote status.

## Safety Boundaries

- Do not overwrite unique Wiki content without incorporating it.
- Do not reorganize unrelated pages.
- Do not change source repositories except for an explicitly requested handoff update.
- Do not publish unverified inference as source-confirmed fact.
- Do not expose private credentials, tokens, keys, internal secrets, or sensitive work material.
