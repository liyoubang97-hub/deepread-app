@echo off
REM DeepRead 生产环境启动脚本

echo ========================================
echo   DeepRead 深度阅读 - 生产环境启动
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

REM 创建必要的目录
echo [2/3] 创建数据目录...
if not exist "data" mkdir data
if not exist "cache" mkdir cache

REM 启动应用
echo [3/3] 启动应用...
echo.
echo ========================================
echo   应用正在启动...
echo   访问地址: http://localhost:8501
echo   按 Ctrl+C 停止应用
echo ========================================
echo.

streamlit run app_v3.8.py --server.port=8501 --server.headless=true

pause
