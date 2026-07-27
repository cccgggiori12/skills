---
name: weekly-report-ppt
description: Create or revise a concise weekly-report PowerPoint by imitating a user-supplied PPTX template and using user-supplied report text or explicitly named reference files/directories. Use when Codex is asked to generate, update, or restyle a work-weekly-report PPT while preserving a reference deck's layout, typography, colors, icons, backgrounds, and level of detail.
---

# Weekly Report PPT

Generate a source-grounded weekly report by treating the supplied PPTX as the visual contract and the supplied text or file paths as the content contract.

## Required inputs

Require both of these before generating:

1. A readable `.pptx` template path. If the user supplies legacy `.ppt`, request or perform an approved conversion to `.pptx`.
2. Either report content written by the user or explicit reference file/directory paths from which to summarize it.

Also use an output path or reporting date range when supplied. Otherwise infer the current Monday-Friday range and save beside the working files with a clear name such as `姓名工作周报YYYY.MM.DD-YYYY.MM.DD.pptx`.

Do not guess a template, scan unrelated repositories, or invent completed work. Ask one concise question only when a required input cannot be discovered from the request or workspace.

## Workflow

### 1. Inspect the template

Run:

```bash
python <skill-dir>/scripts/inspect_pptx.py <template.pptx>
```

Identify:

- slide count, aspect ratio, and which layouts can be reused for added pages;
- section names and intended information hierarchy;
- reusable slide layouts, shape positions, fonts, sizes, colors, icons, backgrounds, and images;
- the reference deck's density and writing style.

Use the template itself rather than recreating an approximately similar theme. Never overwrite it.

### 2. Read and distill content

Treat direct user statements as authoritative. For reference paths:

- start from the exact files or directories named by the user;
- use focused filename and symbol searches when a directory is supplied;
- summarize only claims supported by those sources;
- distinguish completed work, current investigation, next-week plans, blockers, and longer-term goals;
- do not place a cultivation goal or future plan under completed work unless the user explicitly requests it.

Keep wording presentation-ready: conclusion first, short numbered items, one idea per item, consistent product and symbol names. Preserve technical handoff chains when they are the substance of the work.

Before building, group the content by reporting section or responsibility area. Use the template's page count only as a starting point, not as a limit.

### 3. Build from a copy

Copy the template to the output path, then edit the copy.

Prefer `python-pptx` when available. For simple exact text replacement, direct OOXML editing is acceptable if it preserves formatting and package relationships. Install dependencies only when necessary and with the required approval.

Preserve:

- slide size and theme;
- backgrounds, icons, images, and decorative shapes;
- section-title placement;
- typography and color hierarchy;
- a concise result without forcing all content into the template's original page count.

Add one or more pages when the workload, number of responsibility areas, or amount of source-backed detail grows. Prefer duplicating the closest matching content layout so new pages remain visually consistent.

Use these expansion rules:

- keep related bullets together and split independent responsibility areas across pages;
- add a continuation page when a section would otherwise need dense paragraphs, excessive abbreviation, or unusually small body text;
- add a dedicated page for a substantial technical chain, comparison, result set, or next-step plan when combining it with other sections hurts readability;
- preserve the template's title hierarchy and visual rhythm on every added page;
- prefer adding a page over deleting meaningful work or shrinking body text excessively.

Adjust text-box height, font size, paragraph spacing, wording, and page count together to prevent overflow. The final number of pages should follow the content, while the visual language should continue to follow the template.

### 4. Validate

Run:

```bash
python <skill-dir>/scripts/validate_pptx.py <output.pptx> \
  --template <template.pptx> \
  --expected "本周工作内容"
```

Add one `--expected` argument for each required section or key phrase. Then:

- reopen the output with `python-pptx` when available;
- print and review all slide text;
- confirm added pages reuse a coherent template layout and do not duplicate stale template text;
- render to images with LibreOffice or another available renderer and inspect them when possible;
- otherwise use conservative font sizing and shape-bound checks;
- confirm the output is not the template path and the archive has no corrupt entries.

Fix missing content, overflow, inconsistent dates, accidental placeholders, or unnecessary verbosity before handing off.

## Output

Return a clickable absolute path to the generated `.pptx`. Briefly state the reporting range, slide count, sections included, and validation performed.

Do not include the template or source documents inside the skill. They are per-run user inputs.

## Bundled scripts

- `scripts/inspect_pptx.py`: inspect PPTX structure and visible text without requiring third-party packages.
- `scripts/validate_pptx.py`: validate the OOXML archive, required text, and preservation of template media.
