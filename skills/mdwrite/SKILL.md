---
name: mdwrite
description: Write a final Markdown note from already-refined discussion, deep-research output, or curated technical content, then optionally run GitHub-safe math-format checks. Default mode is compose-first.
category: writing
risk: safe
source: merged-draft
date_added: "2026-04-17"
---

# mdwrite

## Purpose

Use this skill when the content has already been discussed, narrowed down, or researched enough, and the main remaining task is:

- turning that material into a clean Markdown note
- matching the established research-note style
- keeping math GitHub-renderable
- controlling structure, density, and tables

This skill is **not** primarily a research agent.
It is a **writer + formatter + math-safety** skill.

## Core Idea

The user workflow is expected to be:

1. discuss a topic until it is sufficiently clear
2. optionally bring deep-research output or other notes
3. invoke `mdwrite`
4. produce one final `main.md`

If needed, `mdwrite` can then:

- expand selected material into an appendix
- perform math-format cleanup
- preserve Markdown-style outline structure when published to LaTeX
- keep table numbering stable in published output
- only split display equations when the line is actually too long
- hand off to publishing tools later

But it should not force publishing by default.

## Publishing Notes

When the user asks for `.tex` or `.pdf`, the publishing pipeline should preserve the note's readable structure rather than flatten it.

In particular:

- keep the Markdown outline section as an actual nested list in LaTeX
- do not strip nested bullets from outline blocks
- keep table numbering stable by using real table environments when a table is short enough to stay a table
- if a table is too wide, render it as structured block content instead of forcing a broken table
- do not auto-break every display equation
- only insert line breaks for display equations when the expression is long enough and the break point is structurally safe

## Primary Modes

### Mode 1: compose

This is the default mode.

Use it to convert already-refined material into a final Markdown note.

Typical inputs:

- discussion summaries
- deep-research output
- bullet points
- formulas
- tables
- conclusions
- a target file path such as `sar_research_note/RDA/main.md`

Typical outputs:

- one `main.md`
- concise but technically useful
- structured for reading, review, and later reporting

### Mode 2: math-check

Use this when the user explicitly asks to:

- check Markdown math formatting
- fix GitHub math issues
- revise notation spacing
- inspect display math blocks

Typical prompts:

- `mdwrite 檢查這份 markdown`
- `用 mdwrite 改數學格式`
- `mdwrite check math formatting`

In this mode, prioritize math notation rules before broader writing cleanup.

## Default Behavior

If the user simply says `mdwrite`, assume:

- they already have enough content
- they want a final Markdown note
- you should compose first
- then silently self-check for obvious math-format issues

Do not default to open-ended research unless the user explicitly asks for it.

## Reference Style

When writing research notes, use this file as the primary structural style reference:

- `research-writing-workflow/docs/reference_style.md`

What to learn from that reference:

- concise sectioned structure
- direct technical statements
- summary-first rhythm
- tables for trade-offs and comparisons
- math integrated into prose, not isolated as disconnected derivations
- engineering interpretation alongside formulas

Do not copy it mechanically.
Use it as a style target for density, clarity, and note rhythm.

The original SAR note that inspired this style can still be used as a secondary example when needed, but it is not a required dependency for this skill.

## Derivation Note Add-On

When the target note is derivation-heavy, inherit these rules:

- keep the note mathematically rigorous and physically interpretable
- prefer a stable section rhythm over decorative formatting
- for long notes, start with a summary and a clickable table of contents
- when a stage signal is central to the argument, do not stop at operator form if a usable closed form can be written
- keep physical meaning close to the equations instead of postponing all interpretation to the end
- use appendix sections when geometric side derivations or detailed expansions would interrupt the main line

For derivation-oriented Markdown, a good default section order is:

1. summary
2. problem definition
3. derivation highlights
4. symbols and assumptions
5. step-by-step derivation
6. physical meaning
7. final result
8. implementation correspondence
9. limitations and scope

You do not need to include all sections for every note, but the derivation should feel structured rather than improvised.

## Expected Input

`mdwrite` works best when the user gives one or more of the following:

- a refined discussion summary
- deep-research output
- key formulas
- key claims or conclusions
- required sections
- target output path

Useful example:

```text
Use mdwrite to turn this deep research into sar_research_note/RDA/main.md.
Follow the DPCA note style.
Keep it within 15 minutes of reading.
Use tables wherever possible.
Do not generate tex/pdf yet.
```

## Expected Output

The default output is:

- one Markdown file, usually named `main.md`

The output should be written into a working repository, not into the skill repository.

Examples:

- `sar_research_note/RDA/main.md`
- `sar_research_note/CSA/main.md`
- `interview/perc-report/main.md`

Do not place topic outputs under:

- `research-writing-workflow/skills/`
- `research-writing-workflow/templates/`

Those locations are for tools, not artifacts.

## Compose Workflow

### 1. Determine the note type

First determine whether the content is mainly:

- topic note
- algorithm note
- engineering decision note
- interview prep note
- derivation appendix

Do not write blindly.
The note structure should match the note type.

### 2. Determine the output path

Before writing, determine where the file should live.

Preferred rules:

- SAR / radar / signal-processing topics -> `sar_research_note/<topic>/main.md`
- interview or report-prep topics -> `interview/<topic>/main.md`

If the target path is ambiguous, ask or infer conservatively.

### 3. Write the main note first

The default artifact is one main Markdown note.

By default:

- do not auto-generate `.tex`
- do not auto-generate `.pdf`
- do not create appendix sections unless needed

### 4. Keep density under control

The note should be:

- easy to scan
- technically accurate
- concise
- structurally stable

Do not bloat the document with textbook-style filler.
If detailed derivation is requested, place it in an appendix at the end of the same file.

### 5. Prefer visual compression

When information can be represented more clearly as a table, prefer a table over long prose.

Use tables for:

- pros and cons
- trade-offs
- algorithm comparisons
- implementation choices
- decision support summaries

Use Mermaid when a flowchart helps more than a paragraph.

## Appendix Rule

Detailed derivations should not appear automatically in the main body.

If the user wants more detail:

- ask or confirm the expansion target
- append the detailed derivation at the end of the same `main.md`
- keep the main body concise

## Publishing Rule

`mdwrite` does not publish by default.

If the user later wants publishing output, that should be a separate step:

- `main.md`
- then optional `main.tex`
- then optional `main.pdf`

## Math-Check Rules

These rules are inherited from the earlier math-first `mdwrite` skill and should be applied whenever math cleanup is requested.

### Inline Math Spacing

- Do not add spaces inside inline math delimiters.
- Add spaces outside delimiters when required by prose.
- Write `$a+b$`, not `$ a+b $`.

Treat these as violations:

- `,$a+b$,`
- `.$a+b$.`
- `，$a+b$，`
- `$ a+b $`
- `g/m$^3$`
- `/m$^3$`

### Delimiter Rules

- Do not use `\left` or `\right`.
- Prefer manual sizing commands:
  - `\bigl` / `\bigr`
  - `\Bigl` / `\Bigr`
  - `\biggl` / `\biggr`
  - `\Biggl` / `\Biggr`
- Use `\biggl` / `\biggr` with `()` or `[]` only.
- Avoid illegal `{}` sizing combinations in GitHub Markdown math.

### Display Math Rules

- A display math block must be surrounded by blank lines.
- Prefer one logical line for one display equation.
- If the equation truly needs line breaks, convert it into `align` or `aligned`.
- Do not leave `+`, `-`, `*`, `/`, `=` dangling on isolated lines.

### Multiline Equation Rules

- Prefer `align` or `aligned` for multiline equations.
- Keep each line semantically complete.
- Optimize for stable GitHub rendering, not textbook numbering.

### Navigation Rules

For longer derivation notes:

- add a clickable table of contents near the top
- use repository-relative links only
- if the note belongs to a larger flow, add short navigation links to prerequisite or next notes

## Writing Rules

- Prefer clarity over cleverness.
- Prefer technical precision over broad motivational prose.
- Keep terminology consistent inside the file.
- Prefer summary-first writing.
- Preserve the user's conclusions and intended emphasis.
- Do not re-open already settled debates unless the user asks.
- Use tables when comparisons are the point.
- Use short paragraphs unless density is necessary.

## Invocation Patterns

Examples:

- `用 mdwrite 幫我把這段 deep research 寫成 main.md`
- `用 mdwrite 根據我們剛剛的討論整理成 sar_research_note/RDA/main.md`
- `mdwrite 幫我重寫這份演算法筆記，照 DPCA 那個格式`
- `mdwrite 檢查這份 Markdown 的數學格式`
- `用 mdwrite 改這份技術筆記，但先不要產生 tex/pdf`

## Success Standard

This skill is successful when:

- the output is a usable final Markdown note
- it matches the intended note type
- it is structurally close to the user's preferred style
- it keeps math GitHub-safe
- it does not over-research or over-expand
- it writes to the correct working repository path
