# Research Writing Workflow

A role-based toolkit for technical research writing workflows centered on Markdown as the source of truth.

This repository is designed for:

- research notes
- engineering concept writeups
- math and physics explanations
- appendix-style derivation expansion
- Markdown to LaTeX to PDF publishing

## Goals

- Keep the main note concise enough for a 30-minute report
- Preserve clear mathematical and physical explanations
- Support optional deep appendix expansion on demand
- Separate research, writing, derivation, and publishing concerns
- Make the publishing path stable with Python scripts instead of ad hoc prompt conversion

## Roles

- `chief-conductor`: receives free-form user requests and routes work
- `researcher`: collects topic background, principles, trade-offs, and engineering context
- `math-physicist`: explains math meaning, physical meaning, and notation consistency
- `markdown-writer`: writes the main Markdown note with report-aware structure
- `derivation-expander`: expands selected sections into detailed appendices only when requested
- `latex-publisher`: converts Markdown to LaTeX and builds PDF/web-preview artifacts

## Repository Layout

```text
research-writing-workflow/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── role-boundaries.md
│   └── style-guide.md
├── skills/
│   ├── chief-conductor/
│   ├── researcher/
│   ├── math-physicist/
│   ├── markdown-writer/
│   ├── derivation-expander/
│   └── latex-publisher/
├── scripts/
│   ├── markdown_to_latex.py
│   ├── build_pdf.py
│   └── preview_site.py
└── templates/
    ├── research_note.md
    ├── appendix_block.md
    └── report_outline.md
```

## Typical Workflow

1. User discusses a topic in free form with `chief-conductor`.
2. `chief-conductor` routes background gathering to `researcher`.
3. `math-physicist` refines mathematical and physical explanations.
4. `markdown-writer` produces a single main Markdown note.
5. If needed, `derivation-expander` appends a detailed appendix.
6. `latex-publisher` runs the publishing scripts to generate LaTeX, PDF, and a lightweight preview page.

## Script Usage

Convert Markdown to LaTeX:

```bash
python3 scripts/markdown_to_latex.py input.md -o output.tex
```

Build PDF from Markdown:

```bash
python3 scripts/build_pdf.py input.md --output-dir build
```

Create a simple HTML page that embeds a PDF:

```bash
python3 scripts/preview_site.py build/input.pdf --title "Research Note"
```

## Design Constraints

- Markdown is the authoritative editing format.
- The main body should stay concise by default.
- Detailed derivations belong in an appendix block when explicitly requested.
- Publishing scripts should prefer predictable transformations over aggressive formatting tricks.

## First-Version Scope

- Research-note focused
- Role definitions and handoff boundaries
- Minimal but usable Markdown to LaTeX pipeline
- PDF build wrapper
- HTML preview wrapper for generated PDFs

Interview or company-specific reporting workflows should be built on top of this toolkit, not embedded into the first-version core.
