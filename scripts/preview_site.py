#!/usr/bin/env python3
"""Create a minimal HTML file that embeds a generated PDF for browser viewing."""

from __future__ import annotations

import argparse
from pathlib import Path


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      font-family: system-ui, sans-serif;
      background: #0b1020;
      color: #eef2ff;
    }}
    header {{
      padding: 16px 20px;
      border-bottom: 1px solid #334155;
      background: #111827;
    }}
    iframe {{
      width: 100%;
      height: calc(100vh - 68px);
      border: 0;
      background: white;
    }}
    a {{
      color: #93c5fd;
    }}
  </style>
</head>
<body>
  <header>
    <strong>{title}</strong>
    <span style="margin-left: 12px;">
      <a href="{pdf_name}">Open PDF directly</a>
    </span>
  </header>
  <iframe src="{pdf_name}"></iframe>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an HTML viewer for a PDF.")
    parser.add_argument("pdf", type=Path, help="PDF file to embed")
    parser.add_argument("--title", default="PDF Preview", help="Page title")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML file")
    args = parser.parse_args()

    output = args.output or args.pdf.with_suffix(".html")
    html = HTML_TEMPLATE.format(title=args.title, pdf_name=args.pdf.name)
    output.write_text(html, encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
