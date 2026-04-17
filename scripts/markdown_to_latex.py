#!/usr/bin/env python3
"""Convert a constrained research-note Markdown format into LaTeX.

This converter intentionally targets a stable subset:
- headings
- paragraphs
- bullet lists
- fenced code blocks
- block quotes
- horizontal rules
- inline emphasis, code, links, and images
- GitHub-style math blocks are passed through to LaTeX

The goal is deterministic conversion, not full Markdown coverage.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


LATEX_PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{enumitem}
\geometry{margin=1in}
\setlist[itemize]{leftmargin=1.5em}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  columns=fullflexible,
  frame=single
}
\title{%s}
\date{}
\begin{document}
\maketitle
"""

LATEX_END = r"""
\end{document}
"""


INLINE_REPLACEMENTS = [
    (re.compile(r"`([^`]+)`"), r"\\texttt{\1}"),
    (re.compile(r"\*\*([^\*]+)\*\*"), r"\\textbf{\1}"),
    (re.compile(r"\*([^\*]+)\*"), r"\\emph{\1}"),
]


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def apply_inline_markup(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\\begin{figure}[h]\n\\centering\n\\includegraphics[width=0.9\\linewidth]{\2}\n\\caption{\1}\n\\end{figure}", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\\href{\2}{\1}", text)
    for pattern, replacement in INLINE_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text


def convert(markdown: str, title: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = [LATEX_PREAMBLE % escape_latex(title)]

    in_code = False
    in_list = False
    in_quote = False
    in_math = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(line.strip() for line in paragraph)
            text = apply_inline_markup(escape_latex(text))
            out.append(text + "\n")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(r"\end{itemize}")
            in_list = False

    def close_quote() -> None:
        nonlocal in_quote
        if in_quote:
            out.append(r"\end{quote}")
            in_quote = False

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("```"):
            flush_paragraph()
            close_list()
            close_quote()
            if not in_code:
                out.append(r"\begin{lstlisting}")
                in_code = True
            else:
                out.append(r"\end{lstlisting}")
                in_code = False
            continue

        if in_code:
            out.append(raw_line)
            continue

        if not line.strip():
            flush_paragraph()
            close_list()
            close_quote()
            continue

        if line.strip() == "---":
            flush_paragraph()
            close_list()
            close_quote()
            out.append(r"\hrule")
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            flush_paragraph()
            close_list()
            close_quote()
            level = len(heading_match.group(1))
            heading_text = apply_inline_markup(escape_latex(heading_match.group(2).strip()))
            command = {
                1: r"\section",
                2: r"\subsection",
                3: r"\subsubsection",
                4: r"\paragraph",
                5: r"\subparagraph",
                6: r"\textbf",
            }[level]
            if level <= 5:
                out.append(f"{command}{{{heading_text}}}")
            else:
                out.append(f"{command}{{{heading_text}}}")
            continue

        if line.strip() == "$$":
            flush_paragraph()
            close_list()
            close_quote()
            out.append(raw_line)
            in_math = not in_math
            continue

        if in_math:
            out.append(raw_line)
            continue

        if line.startswith("$$") and line.endswith("$$"):
            flush_paragraph()
            close_list()
            close_quote()
            out.append(raw_line)
            continue

        if line.lstrip().startswith(">"):
            flush_paragraph()
            close_list()
            if not in_quote:
                out.append(r"\begin{quote}")
                in_quote = True
            quote_text = line.lstrip()[1:].strip()
            out.append(apply_inline_markup(escape_latex(quote_text)))
            continue
        else:
            close_quote()

        list_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_match:
            flush_paragraph()
            if not in_list:
                out.append(r"\begin{itemize}")
                in_list = True
            item_text = apply_inline_markup(escape_latex(list_match.group(1)))
            out.append(f"\\item {item_text}")
            continue
        else:
            close_list()

        paragraph.append(raw_line)

    flush_paragraph()
    close_list()
    close_quote()
    if in_code:
        out.append(r"\end{lstlisting}")
    out.append(LATEX_END)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert research-note Markdown to LaTeX.")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("-o", "--output", type=Path, help="Output LaTeX file")
    parser.add_argument("--title", help="Document title override")
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    title = args.title or args.input.stem.replace("_", " ").replace("-", " ").title()
    latex = convert(markdown, title)

    output = args.output or args.input.with_suffix(".tex")
    output.write_text(latex, encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
