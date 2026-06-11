#!/usr/bin/env python3
"""
Convierte un archivo Markdown a PDF.

Uso:
    python scripts/md2pdf.py <entrada.md> [salida.pdf]

Pipeline: Markdown -> HTML (libreria `markdown`) -> PDF (Edge/Chrome headless).
No requiere LaTeX. Solo necesita Python con el paquete `markdown` y un navegador
Chromium (Microsoft Edge o Google Chrome), ambos ya presentes en Windows 10/11.

    pip install markdown pygments
"""
import sys
import os
import subprocess
import shutil

try:
    import markdown
except ImportError:
    print("Falta el paquete 'markdown'. Instalalo con:  pip install markdown pygments")
    sys.exit(1)

CSS = r"""
@page { size: A4; margin: 17mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: "Segoe UI", Calibri, Arial, sans-serif;
  font-size: 10.6pt; line-height: 1.45; color: #1f2933; margin: 0;
}
h1, h2, h3, h4 { color: #1f6fb2; line-height: 1.2; page-break-after: avoid; }
h1 { font-size: 21pt; border-bottom: 3px solid #1f6fb2; padding-bottom: 6px; margin: 0 0 10px; }
h2 { font-size: 15pt; border-bottom: 1px solid #c8d6e5; padding-bottom: 3px; margin: 20px 0 8px; }
h3 { font-size: 12.5pt; margin: 14px 0 5px; }
h4 { font-size: 11pt; margin: 11px 0 4px; color: #2a3b4d; }
p, li { margin: 4px 0; }
ul, ol { margin: 5px 0 5px 0; padding-left: 22px; }
li { page-break-inside: avoid; }
code { font-family: "Cascadia Code", Consolas, monospace; font-size: 9.2pt;
       background: #eef2f7; padding: 1px 4px; border-radius: 3px; color: #b03a5b; }
pre { background: #f5f7fa; border: 1px solid #d7e0ea; border-left: 4px solid #1f6fb2;
      border-radius: 4px; padding: 9px 12px; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; color: #243b53; padding: 0; font-size: 8.9pt; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9.6pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #b8c6d6; padding: 5px 8px; text-align: left; vertical-align: top; }
th { background: #1f6fb2; color: #fff; font-weight: 600; }
tr:nth-child(even) td { background: #f3f7fb; }
blockquote { border-left: 4px solid #f0ad4e; background: #fff8ec; margin: 8px 0;
             padding: 6px 12px; color: #6b4e16; }
hr { border: none; border-top: 1px solid #c8d6e5; margin: 16px 0; }
a { color: #1f6fb2; text-decoration: none; }
strong { color: #16324f; }
.codehilite { background: #f5f7fa; }
"""

HTML_TMPL = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}</style></head><body>
{body}
</body></html>"""


def find_browser():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    for name in ("msedge", "chrome", "chromium"):
        p = shutil.which(name)
        if p:
            return p
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = os.path.abspath(sys.argv[1])
    pdf = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 \
        else os.path.splitext(src)[0] + ".pdf"
    html_path = os.path.splitext(pdf)[0] + ".html"

    with open(src, encoding="utf-8") as f:
        text = f.read()

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "codehilite", "toc",
                    "sane_lists", "attr_list"],
        extension_configs={"codehilite": {"guess_lang": False}},
    )
    title = os.path.splitext(os.path.basename(src))[0]
    html = HTML_TMPL.format(title=title, css=CSS, body=body)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    browser = find_browser()
    if not browser:
        print("No se encontro Edge ni Chrome. HTML generado en:", html_path)
        sys.exit(2)

    url = "file:///" + html_path.replace("\\", "/")
    subprocess.run(
        [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf}", url],
        check=False,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if os.path.exists(pdf):
        print(f"PDF generado: {pdf} ({os.path.getsize(pdf)} bytes)")
    else:
        print("No se pudo generar el PDF. Revisa el HTML:", html_path)
        sys.exit(3)


if __name__ == "__main__":
    main()
