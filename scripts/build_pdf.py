#!/usr/bin/env python3
"""Build a PDF from a Markdown source through the local conversion pipeline."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from markdown_to_latex import convert


def choose_latex_engine() -> list[str] | None:
    if shutil.which("latexmk"):
        return ["latexmk", "-pdf", "-interaction=nonstopmode"]
    if shutil.which("pdflatex"):
        return ["pdflatex", "-interaction=nonstopmode"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PDF from Markdown.")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("--output-dir", type=Path, default=Path("build"), help="Output directory")
    parser.add_argument("--title", help="Document title override")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    markdown = args.input.read_text(encoding="utf-8")
    title = args.title or args.input.stem.replace("_", " ").replace("-", " ").title()
    tex_path = args.output_dir / f"{args.input.stem}.tex"
    tex_path.write_text(convert(markdown, title), encoding="utf-8")
    print(f"Wrote {tex_path}")

    engine = choose_latex_engine()
    if engine is None:
        print("No LaTeX engine found. Install latexmk or pdflatex to build PDFs.")
        return 1

    cmd = engine + [tex_path.name]
    subprocess.run(cmd, cwd=args.output_dir, check=True)
    pdf_path = tex_path.with_suffix(".pdf")
    print(f"Built {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
