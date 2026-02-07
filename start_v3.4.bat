@echo off
echo ========================================
echo   DeepRead V3.4 - 优雅优化版
echo ========================================
echo.
echo 改进：
echo - 扁平风SVG logo（思考+读书主题）
echo - 放大"给自己时间慢慢来"文字
echo - 修复《原子习惯》卡片显示和简介
echo - 缩小书籍卡片尺寸
echo - 移除有色方块，改为简约线条
echo - 修复页面跳转滚动到顶部
echo.
echo 启动中...
echo.

python -m streamlit run app_v3.4.py

pause
