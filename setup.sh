#!/bin/bash

echo "========================================"
echo "视频爬虫工具 - 自动安装脚本"
echo "========================================"
echo ""

echo "[1/4] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[错误] 未检测到 Python，请先安装 Python 3.7+"
        echo "下载地址: https://www.python.org/downloads/"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi
$PYTHON_CMD --version
echo ""

echo "[2/4] 安装 Python 依赖..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[警告] Python 依赖安装失败，请检查网络连接"
fi
echo ""

echo "[3/4] 检查 Node.js 环境（可选）..."
if ! command -v node &> /dev/null; then
    echo "[提示] 未检测到 Node.js，跳过 Node.js 依赖安装"
    echo "[提示] Node.js 是可选的，不影响核心功能"
    echo "[提示] 如需增强功能，请安装 Node.js: https://nodejs.org/"
else
    node --version
    echo "[4/4] 安装 Node.js 依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[警告] Node.js 依赖安装失败，请检查网络连接"
    fi
fi
echo ""

echo "========================================"
echo "安装完成！"
echo "========================================"
echo ""
echo "快速开始:"
echo "  $PYTHON_CMD main.py https://example.com/videos"
echo ""
echo "查看帮助:"
echo "  $PYTHON_CMD main.py --help"
echo ""
echo "详细文档请查看 README.md"
echo ""
