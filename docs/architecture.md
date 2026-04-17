# Architecture

## Core Model

This repository uses a role-oriented architecture with Markdown as the source artifact and Python-based publishing as the output layer.

The workflow is intentionally split into two planes:

- reasoning plane: skills that decide what the note should contain
- publishing plane: scripts that transform the note into distributable artifacts

## Flow

```text
free-form user request
        |
        v
chief-conductor
        |
        +--> researcher
        |
        +--> math-physicist
        |
        +--> markdown-writer
        |
        +--> derivation-expander (only on demand)
        |
        v
final Markdown note
        |
        v
latex-publisher
        |
        +--> markdown_to_latex.py
        +--> build_pdf.py
        +--> preview_site.py
```

## Main Design Choices

- Free-form user input is normalized by `chief-conductor`.
- The main note stays short enough to present in one sitting.
- Heavy derivations are gated behind explicit expansion requests.
- Publishing is deterministic and script-driven.

## Why Separate Roles From Scripts

Skills solve interpretation problems.
Scripts solve reproducibility problems.

This separation keeps writing quality and build reliability from becoming coupled.
