@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ==========================================
echo   Course Site - Update ^& Build Pipeline
echo ==========================================

:: Change working directory to project root (parent directory of scripts folder)
cd /d "%~dp0.."

echo [1/4] Running DB seed script (Law Course Part 4)...
uv run python scripts\seeders\seed_law_ultimate_pt4.py

echo [2/4] Extracting DB Content for validation...
uv run python scripts\export_tools\_extract_db_content.py

echo [3/4] Generating DOCX Contracts...
uv run python scripts\export_tools\generate_docx.py

echo [4/4] Exporting Static Web Site...
uv run python scripts\export_tools\export_site.py

echo ==========================================
echo   All pipeline tasks finished successfully!
echo ==========================================
