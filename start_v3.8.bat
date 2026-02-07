@echo off
chcp 65001 >nul
echo ========================================
echo   DeepRead V3.8 - Export Features
echo ========================================
echo.
echo Starting...
echo.

python -m streamlit run app_v3.8.py

pause
