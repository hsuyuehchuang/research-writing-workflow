# Research Writing Workflow

Toolkit repo for reusable research-writing skills, templates, and publishing scripts.

Use this repo for:

- Markdown note writing
- math-safe GitHub Markdown cleanup
- algorithm and decision-note templates
- appendix expansion rules
- optional Markdown to LaTeX to PDF publishing

Do not use this repo as the default output location for topic notes.

## Main Skill

- `mdwrite`

`mdwrite` is the primary skill for turning already-refined discussion, deep-research output, or curated technical content into a final `main.md`.

Default behavior:

- write the Markdown note first
- keep output concise and structured
- do not auto-generate `tex/pdf`
- run math-safe cleanup when needed

## Typical Usage

```text
Use mdwrite to turn this discussion into sar_research_note/RDA/main.md.
Follow the DPCA note style.
Keep it within 15 minutes of reading.
Use tables wherever possible.
Do not generate tex/pdf yet.
```

Engineering-decision variant:

```text
Use research-writing-workflow to help me study RDA.
Please use the engineering-decision algorithm note format:
1. 重點摘要
2. 物理意義與關鍵數學
3. 核心流程
4. 3大風險
5. 演算法決策輔助
6. 最後告訴我還缺哪些參數要確認
```

## Input

Best inputs for this workflow:

- refined discussion summary
- deep-research output
- bullet points
- formulas
- target output path
- required sections or constraints

## Output

Default output:

- one Markdown file, usually `main.md`

Write outputs into a working repo, for example:

```text
sar_research_note/RDA/main.md
interview/perc-report/main.md
```

If the user later asks for publishing output, the same folder can receive:

- `main.tex`
- `main.pdf`
- `preview.html`

Publishing behavior now preserves:

- Markdown-style nested outline lists
- stable table numbering for normal-width tables
- conservative display-equation line breaking

## Templates

- `templates/research_note.md`
- `templates/algorithm_note.md`
- `templates/algorithm_decision_note.md`
- `templates/appendix_block.md`

Style reference:

- `docs/reference_style.md`

## Skill Boundaries

Shared skills belong here when they are reusable across repos.

Examples:

- `mdwrite`
- Markdown math rules
- research-note templates
- publishing helpers

Repo-local skills should stay local when they depend on one repo or one workflow.

Examples:

- `interview-company-prep`

See:

- [`docs/skill-boundaries.md`](./docs/skill-boundaries.md)

## Scripts

```bash
python3 scripts/markdown_to_latex.py input.md -o output.tex
python3 scripts/build_pdf.py input.md --output-dir build
python3 scripts/build_pdf.py sar_research_note/RDA/main.md --write-near-source
python3 scripts/preview_site.py build/input.pdf --title "Preview"
```
