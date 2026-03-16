#!/usr/bin/env python3
"""Convertit notice_fondateur.md en PDF avec style soigné via weasyprint."""
import markdown
from weasyprint import HTML
import os

DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DIR, '..', 'docs', 'notice_fondateur.md')
PDF_PATH = os.path.join(DIR, '..', 'docs', 'notice_fondateur.pdf')

with open(MD_PATH, 'r') as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])

html_full = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<style>
@page {{
  size: A4;
  margin: 2cm 2.2cm;
  @bottom-center {{
    content: counter(page) " / " counter(pages);
    font-size: 9pt;
    color: #999;
    font-family: 'Segoe UI', system-ui, sans-serif;
  }}
}}

body {{
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #1a1a2e;
  max-width: 100%;
}}

h1 {{
  font-size: 24pt;
  color: #10b981;
  border-bottom: 3px solid #10b981;
  padding-bottom: 8px;
  margin-top: 0;
  margin-bottom: 6px;
}}

h1 + blockquote {{
  background: #f0fdf4;
  border-left: 4px solid #10b981;
  padding: 10px 16px;
  margin: 0 0 20px 0;
  border-radius: 0 6px 6px 0;
  color: #166534;
  font-style: normal;
  font-size: 10pt;
}}

h2 {{
  font-size: 16pt;
  color: #1a1a2e;
  margin-top: 28px;
  margin-bottom: 10px;
  padding-bottom: 4px;
  border-bottom: 1.5px solid #e5e7eb;
  page-break-after: avoid;
}}

h3 {{
  font-size: 12pt;
  color: #374151;
  margin-top: 18px;
  margin-bottom: 8px;
  page-break-after: avoid;
}}

p {{
  margin: 6px 0;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0 16px 0;
  font-size: 10pt;
  page-break-inside: avoid;
}}

thead {{
  background: #f8fafc;
}}

th {{
  text-align: left;
  padding: 8px 10px;
  border-bottom: 2px solid #10b981;
  font-weight: 600;
  color: #1a1a2e;
}}

td {{
  padding: 6px 10px;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: top;
}}

tr:last-child td {{
  border-bottom: none;
}}

code {{
  background: #f1f5f9;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 9.5pt;
  font-family: 'Cascadia Code', 'Fira Code', monospace;
  color: #0f172a;
}}

pre {{
  background: #1e293b;
  color: #e2e8f0;
  padding: 14px 18px;
  border-radius: 8px;
  font-size: 9pt;
  line-height: 1.5;
  overflow-x: auto;
  page-break-inside: avoid;
  margin: 10px 0;
}}

pre code {{
  background: none;
  padding: 0;
  color: #e2e8f0;
  font-size: 9pt;
  word-wrap: break-word;
  white-space: pre-wrap;
}}

blockquote {{
  border-left: 3px solid #d1d5db;
  padding: 6px 14px;
  margin: 10px 0;
  color: #6b7280;
  font-size: 10pt;
}}

hr {{
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 20px 0;
}}

strong {{
  color: #1a1a2e;
}}

em {{
  color: #6b7280;
}}

ul, ol {{
  padding-left: 20px;
  margin: 6px 0;
}}

li {{
  margin: 3px 0;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html_full).write_pdf(PDF_PATH)
print(f'PDF generé : {PDF_PATH}')
