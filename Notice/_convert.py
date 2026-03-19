"""Convertit le .md en PDF via markdown + weasyprint."""
import markdown
from weasyprint import HTML

MD_FILE = "/home/nicolas/Bureau/algebra live/algebra/Notice/matheux-notice-complete.md"
PDF_FILE = "/home/nicolas/Bureau/algebra live/algebra/Notice/matheux-notice-complete.pdf"

with open(MD_FILE, "r") as f:
    md_text = f.read()

html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])

html_full = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  body {{
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1e293b;
    max-width: 700px;
    margin: 0 auto;
    padding: 40px 30px;
  }}
  h1 {{
    font-size: 22pt;
    font-weight: 900;
    color: #0f172a;
    border-bottom: 3px solid #4338ca;
    padding-bottom: 8px;
    margin-top: 40px;
  }}
  h2 {{
    font-size: 16pt;
    font-weight: 700;
    color: #1e40af;
    margin-top: 30px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
  }}
  h3 {{
    font-size: 13pt;
    font-weight: 700;
    color: #334155;
    margin-top: 20px;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
  }}
  th {{
    background: #f1f5f9;
    font-weight: 700;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
  }}
  td {{
    padding: 6px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background: #f8fafc;
  }}
  code {{
    background: #f1f5f9;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 9.5pt;
    font-family: 'Fira Code', monospace;
  }}
  pre {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    font-size: 9pt;
    overflow-x: auto;
    line-height: 1.5;
  }}
  pre code {{
    background: none;
    padding: 0;
    color: inherit;
  }}
  blockquote {{
    border-left: 4px solid #4338ca;
    margin: 16px 0;
    padding: 8px 16px;
    background: #eef2ff;
    color: #3730a3;
    font-style: italic;
  }}
  hr {{
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 30px 0;
  }}
  strong {{
    font-weight: 700;
  }}
  a {{
    color: #4338ca;
    text-decoration: none;
  }}
  @page {{
    size: A4;
    margin: 2cm 2.5cm;
    @bottom-center {{
      content: "Matheux · Notice complète · 19 mars 2026 — Page " counter(page);
      font-size: 8pt;
      color: #94a3b8;
    }}
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html_full).write_pdf(PDF_FILE)
print(f"✅ PDF généré : {PDF_FILE}")
