# Regenera PLAN.pdf a partir de PLAN.md
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
$root = Split-Path -Parent $PSScriptRoot
python (Join-Path $PSScriptRoot "md2pdf.py") (Join-Path $root "PLAN.md") (Join-Path $root "PLAN.pdf")
