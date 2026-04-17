#!/usr/bin/env python3
"""Convert constrained research-note Markdown into LaTeX."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


LATEX_PREAMBLE = r"""\documentclass[journal,onecolumn]{IEEEtran}

\usepackage{graphicx}
\usepackage{color}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fontspec}
\usepackage{subcaption}
\usepackage{soul}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{array}
\usepackage{listings}
\usepackage{hyperref}
\usepackage{float}
\usepackage{caption}
\sethlcolor{yellow}
\setmainfont{TeX Gyre Termes}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  columns=fullflexible,
  frame=single
}
\hypersetup{pdftitle={%s}}
\begin{document}

\title{%s}
\author{H.-Y. Chuang, E-mail: hsuyueh.chuang@tronfuture.com.}
\maketitle
\markboth{hsuyueh.chuang}{}

Update Date: %s
"""

LATEX_END = r"""
\end{document}
"""


INLINE_REPLACEMENTS = [
    (re.compile(r"`([^`]+)`"), r"\\texttt{\1}"),
    (re.compile(r"\*\*([^\*]+)\*\*"), r"\\textbf{\1}"),
    (re.compile(r"\*([^\*]+)\*"), r"\\emph{\1}"),
]

MATH_TOKEN_RE = re.compile(r"(\$[^$\n]+\$)")
HEADING_NUMBER_RE = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s+")
BREAK_TOKENS = [
    r"\approx",
    r"\propto",
    r"\Rightarrow",
    r"\Longrightarrow",
    "=",
]
TABLE_MAX_COLS = 4
TABLE_MAX_CELL_LEN = 44
TABLE_MAX_ROW_LEN = 120


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


def format_inline_segment(text: str) -> str:
    image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def replace_image(match: re.Match[str]) -> str:
        caption = escape_latex(match.group(1))
        path = match.group(2)
        return (
            "\\begin{figure}[H]\n"
            "\\centering\n"
            f"\\includegraphics[width=0.9\\linewidth]{{{path}}}\n"
            f"\\caption{{{caption}}}\n"
            "\\end{figure}"
        )

    def replace_link(match: re.Match[str]) -> str:
        label = escape_latex(match.group(1))
        target = match.group(2)
        if target.startswith("#"):
            return label
        return f"\\href{{{target}}}{{{label}}}"

    text = image_pattern.sub(replace_image, text)
    text = link_pattern.sub(replace_link, text)
    text = escape_latex(text)
    for pattern, replacement in INLINE_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text


def apply_inline_markup(text: str) -> str:
    parts = MATH_TOKEN_RE.split(text)
    rendered: list[str] = []
    for part in parts:
        if not part:
            continue
        if MATH_TOKEN_RE.fullmatch(part):
            rendered.append(part)
        else:
            rendered.append(format_inline_segment(part))
    return "".join(rendered)


def normalize_heading_text(text: str) -> str:
    return HEADING_NUMBER_RE.sub("", text).strip()


def extract_title(markdown: str, fallback: str) -> tuple[str, int | None]:
    for idx, line in enumerate(markdown.splitlines()):
        match = re.match(r"^#\s+(.*)$", line.strip())
        if match:
            return normalize_heading_text(match.group(1).strip()), idx
    return fallback, None


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def should_render_as_table(rows: list[list[str]]) -> bool:
    if len(rows) < 2:
        return False
    column_count = max(len(row) for row in rows)
    if column_count > TABLE_MAX_COLS:
        return False
    for row in rows:
        if sum(len(cell) for cell in row) > TABLE_MAX_ROW_LEN:
            return False
        for cell in row:
            if len(cell) > TABLE_MAX_CELL_LEN:
                return False
    return True


def render_table_as_blocks(header: list[str], body: list[list[str]]) -> list[str]:
    out: list[str] = []
    for row in body:
        out.append(r"\begin{quote}")
        for idx, label in enumerate(header):
            value = row[idx] if idx < len(row) else ""
            out.append(r"\textbf{" + apply_inline_markup(label) + r"}: " + apply_inline_markup(value) + r"\\")
        out.append(r"\end{quote}")
    return out


def slugify_label(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or fallback


def derive_table_caption(paragraph_before: str | None, heading_stack: dict[int, str], table_index: int) -> tuple[str, str]:
    if paragraph_before:
        cleaned = paragraph_before.strip()
        cleaned = re.sub(r"^the\s+", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.rstrip(":").rstrip(".").strip()
        cleaned = re.sub(r"\s+is\s*$", "", cleaned, flags=re.IGNORECASE)
        if 0 < len(cleaned) <= 80:
            caption = cleaned[:1].upper() + cleaned[1:]
            return caption, slugify_label(caption, f"table-{table_index}")

    for level in (3, 2, 1):
        heading = heading_stack.get(level)
        if heading:
            return heading, slugify_label(heading, f"table-{table_index}")

    caption = f"Table {table_index}"
    return caption, f"table-{table_index}"


def make_column_spec(column_count: int) -> str:
    width = 0.92 / max(column_count, 1)
    cols = []
    for _ in range(column_count):
        cols.append(r">{\raggedright\arraybackslash}p{" + f"{width:.3f}" + r"\linewidth}")
    return "".join(cols)


def render_table(table_lines: list[str], paragraph_before: str | None, heading_stack: dict[int, str], table_index: int) -> list[str]:
    rows = [split_table_row(line) for line in table_lines]
    header = rows[0]
    body = rows[2:]
    if not should_render_as_table([header] + body):
        return render_table_as_blocks(header, body)

    column_count = len(header)
    caption, label = derive_table_caption(paragraph_before, heading_stack, table_index)
    alignment = make_column_spec(column_count)

    out = [
        r"\begin{table}[H]",
        r"\centering",
        rf"\caption{{{apply_inline_markup(caption)}}}",
        rf"\label{{tab:{label}}}",
        rf"\begin{{tabular}}{{{alignment}}}",
        r"\toprule",
        " & ".join(apply_inline_markup(cell) for cell in header) + r" \\",
        r"\midrule",
    ]

    for row in body:
        padded = row + [""] * (column_count - len(row))
        out.append(" & ".join(apply_inline_markup(cell) for cell in padded[:column_count]) + r" \\")

    out.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    return out


def split_equation_line(line: str) -> list[str]:
    stripped = line.strip()
    if len(stripped) <= 110:
        return [stripped]

    protected_tokens = [r"\left", r"\right", r"\biggl", r"\biggr", r"\Bigl", r"\Bigr"]
    if any(token in stripped for token in protected_tokens):
        return [stripped]

    best_idx = -1
    best_token = ""
    for token in BREAK_TOKENS:
        idx = stripped.rfind(token)
        if idx > 24:
            best_idx = idx
            best_token = token
            break

    if best_idx == -1:
        return [stripped]

    split_at = best_idx if best_token.startswith("\\") else best_idx + len(best_token)
    left = stripped[:split_at].rstrip()
    right = stripped[split_at:].lstrip()
    if not left or not right:
        return [stripped]
    return [left, right]


def render_display_math(math_lines: list[str]) -> list[str]:
    content = [line.rstrip() for line in math_lines if line.strip()]
    if not content:
        return []

    joined = " ".join(line.strip() for line in content)
    if any(r"\left" in line or r"\right" in line for line in content):
        return [r"\begin{equation}", joined, r"\end{equation}"]

    if len(joined) <= 180:
        return [r"\begin{align}", joined, r"\end{align}"]

    if len(content) > 1:
        out = [r"\begin{align}"]
        for idx, line in enumerate(content):
            line = line.strip()
            if idx < len(content) - 1:
                out.append(line + r" \\")
            else:
                out.append(line)
        out.append(r"\end{align}")
        return out

    line = content[0].strip()
    segments = split_equation_line(line)
    if len(segments) == 1:
        return [r"\begin{align}", segments[0], r"\end{align}"]

    out = [r"\begin{align}"]
    for idx, segment in enumerate(segments):
        if idx < len(segments) - 1:
            out.append(segment + r" \notag \\")
        else:
            out.append(segment)
    out.append(r"\end{align}")
    return out


def open_list_env(level: int) -> str:
    indent = "  " * max(level - 1, 0)
    return indent + r"\begin{itemize}"


def close_list_env(level: int) -> str:
    indent = "  " * max(level - 1, 0)
    return indent + r"\end{itemize}"


def list_item_line(level: int, text: str) -> str:
    indent = "  " * level
    return indent + r"\item " + text


def markdown_list_level(line: str) -> int | None:
    match = re.match(r"^(\s*)-\s+(.*)$", line)
    if not match:
        return None
    indent = len(match.group(1).replace("\t", "    "))
    return indent // 2 + 1


def markdown_list_text(line: str) -> str:
    match = re.match(r"^\s*-\s+(.*)$", line)
    return match.group(1) if match else line


def convert(markdown: str, title: str) -> str:
    lines = markdown.splitlines()
    extracted_title, title_line_idx = extract_title(markdown, title)
    if extracted_title:
        title = extracted_title

    heading_level_offset = 1 if title_line_idx is not None else 0
    escaped_title = escape_latex(title)
    out: list[str] = [LATEX_PREAMBLE % (escaped_title, escaped_title, date.today().isoformat())]

    in_code = False
    in_quote = False
    in_math = False
    paragraph: list[str] = []
    table_buffer: list[str] = []
    math_buffer: list[str] = []
    list_stack = 0
    heading_stack: dict[int, str] = {}
    last_paragraph_text: str | None = None
    table_index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph, last_paragraph_text
        if paragraph:
            raw_text = " ".join(line.strip() for line in paragraph).strip()
            out.append(apply_inline_markup(raw_text) + "\n")
            last_paragraph_text = raw_text
            paragraph = []

    def close_lists(target_level: int = 0) -> None:
        nonlocal list_stack
        while list_stack > target_level:
            out.append(close_list_env(list_stack))
            list_stack -= 1

    def close_quote() -> None:
        nonlocal in_quote
        if in_quote:
            out.append(r"\end{quote}")
            in_quote = False

    def flush_table() -> None:
        nonlocal table_buffer, table_index, last_paragraph_text
        if table_buffer:
            table_index += 1
            out.extend(render_table(table_buffer, last_paragraph_text, heading_stack, table_index))
            table_buffer = []

    def flush_math() -> None:
        nonlocal math_buffer
        if math_buffer:
            out.extend(render_display_math(math_buffer))
            math_buffer = []

    for idx, raw_line in enumerate(lines):
        line = raw_line.rstrip()

        if title_line_idx is not None and idx == title_line_idx:
            continue

        if line.startswith("```"):
            flush_paragraph()
            close_lists()
            close_quote()
            flush_table()
            flush_math()
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
            close_lists()
            close_quote()
            flush_table()
            flush_math()
            continue

        if line.strip() == "---":
            flush_paragraph()
            close_lists()
            close_quote()
            flush_table()
            flush_math()
            out.append(r"\hrule")
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            flush_paragraph()
            close_lists()
            close_quote()
            flush_table()
            flush_math()
            raw_level = len(heading_match.group(1))
            level = max(1, raw_level - heading_level_offset)
            normalized = normalize_heading_text(heading_match.group(2).strip())
            heading_stack[level] = normalized
            for stale_level in list(heading_stack):
                if stale_level > level:
                    del heading_stack[stale_level]
            heading_text = apply_inline_markup(normalized)

            if normalized.lower() == "outline":
                out.append(r"\section*{" + heading_text + "}")
                continue

            command = {
                1: r"\section",
                2: r"\subsection",
                3: r"\subsubsection",
                4: r"\paragraph",
                5: r"\subparagraph",
                6: r"\textbf",
            }[level]
            out.append(f"{command}{{{heading_text}}}")
            continue

        if line.strip() == "$$":
            flush_paragraph()
            close_lists()
            close_quote()
            flush_table()
            if not in_math:
                in_math = True
                math_buffer = []
            else:
                flush_math()
                in_math = False
            continue

        if in_math:
            math_buffer.append(raw_line)
            continue

        if line.startswith("$$") and line.endswith("$$"):
            flush_paragraph()
            close_lists()
            close_quote()
            flush_table()
            math_buffer = [line[2:-2].strip()]
            flush_math()
            continue

        if "|" in line:
            if not table_buffer:
                flush_paragraph()
                close_lists()
                close_quote()
                flush_math()
            table_buffer.append(raw_line)
            continue
        flush_table()

        if line.lstrip().startswith(">"):
            flush_paragraph()
            close_lists()
            flush_math()
            if not in_quote:
                out.append(r"\begin{quote}")
                in_quote = True
            quote_text = line.lstrip()[1:].strip()
            out.append(apply_inline_markup(quote_text))
            continue
        close_quote()

        list_level = markdown_list_level(line)
        if list_level is not None:
            flush_paragraph()
            flush_math()
            while list_stack < list_level:
                list_stack += 1
                out.append(open_list_env(list_stack))
            close_lists(list_level)
            item_text = apply_inline_markup(markdown_list_text(line))
            out.append(list_item_line(list_level, item_text))
            continue
        close_lists()

        paragraph.append(raw_line)

    flush_paragraph()
    close_lists()
    close_quote()
    flush_table()
    flush_math()
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
    fallback_title = args.input.stem.replace("_", " ").replace("-", " ").title()
    title, _ = extract_title(markdown, args.title or fallback_title)
    latex = convert(markdown, title)

    output = args.output or args.input.with_suffix(".tex")
    output.write_text(latex, encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
