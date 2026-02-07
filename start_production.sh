#!/bin/bash

# DeepRead 生产环境启动脚本

echo "========================================"
echo "  DeepRead 深度阅读 - 生产环境启动"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.10+"
    exit 1
fi

# 检查依赖
echo "[1/3] 检查依赖..."
if ! pip3 show streamlit &> /dev/null; then
    echo "[信息] 正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
fi

# 创建必要的目录
echo "[2/3] 创建数据目录..."
mkdir -p data cache

# 启动应用
echo "[3/3] 启动应用..."
echo ""
echo "========================================"
echo "  应用正在启动..."
echo "  访问地址: http://localhost:8501"
echo "  按 Ctrl+C 停止应用"
echo "========================================"
echo ""

streamlit run app_v3.8.py --server.port=8501 --server.headless=true
