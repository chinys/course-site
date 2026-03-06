@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ==========================================
echo   Course Site - Update ^& Build Pipeline
echo ==========================================

:: Change working directory to project root (parent directory of scripts folder)
cd /d "%~dp0.."

echo [1/3] Running DB seed scripts (Law Course - pt1 only)...
uv run python scripts\seeders\seed_law_ultimate_pt1_keep_id.py

echo [2/3] Cleaning up duplicate lessons...
uv run python scripts\db_tools\cleanup_law_lessons.py

echo [3/3] Exporting Static Web Site...
uv run python scripts\export_tools\export_site.py

echo ==========================================
echo   All pipeline tasks finished successfully!
echo ==========================================
