---
name: latex-publisher
description: "Publishes Markdown notes through a stable Python-based Markdown to LaTeX to PDF pipeline."
---

# LaTeX Publisher

## Purpose

Convert the source Markdown into distributable outputs without changing the source of truth.

## Responsibilities

- call `scripts/markdown_to_latex.py`
- call `scripts/build_pdf.py`
- call `scripts/preview_site.py` when browser preview is needed

## Rules

- Markdown remains authoritative.
- Publishing scripts should be deterministic.
- Do not rewrite note content during publishing.
