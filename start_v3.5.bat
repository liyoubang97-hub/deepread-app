@echo off
echo ========================================
echo   DeepRead V3.5 - 修复优化版
echo ========================================
echo.
echo 改进：
echo - 修复侧边栏图标显示（使用emoji）
echo - 修复图书封面（使用emoji占位符）
echo - 优化点击交互
echo - 改成两本书一行的布局
echo.
echo 启动中...
echo.

python -m streamlit run app_v3.5.py

pause
