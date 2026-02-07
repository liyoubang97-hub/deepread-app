@echo off
echo ========================================
echo   DeepRead V3.6 - 极简优化版
echo ========================================
echo.
echo 改进：
echo - 侧边栏改为脑子黑白线条图（透明底）
echo - 两列布局对齐，占满一行
echo - 移除所有有色框（极简设计）
echo - 修复跳转后滚动到顶部
echo.
echo 启动中...
echo.

python -m streamlit run app_v3.6.py

pause
