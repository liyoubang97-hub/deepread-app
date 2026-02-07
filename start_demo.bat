@echo off
echo Starting DeepRead Demo...
echo.
echo Browser will open automatically at http://localhost:8501
echo Press Ctrl+C to stop
echo.

python -m streamlit run app_demo.py --server.headless=true

pause
