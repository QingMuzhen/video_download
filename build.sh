#!/bin/bash

echo "========================================"
echo "视频爬虫工具 - 打包脚本"
echo "========================================"
echo ""

echo "[1/3] 检查 PyInstaller..."
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "PyInstaller 未安装，正在安装..."
    python3 -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "[错误] PyInstaller 安装失败"
        exit 1
    fi
fi
echo "✓ PyInstaller 已就绪"
echo ""

echo "[2/3] 清理旧的构建文件..."
rm -rf build dist
echo "✓ 清理完成"
echo ""

echo "[3/3] 开始打包..."
echo "这可能需要几分钟时间，请耐心等待..."
echo ""

pyinstaller --clean video_downloader.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 打包失败"
    exit 1
fi

echo ""
echo "========================================"
echo "打包完成！"
echo "========================================"
echo ""
echo "可执行文件位置: dist/视频爬虫工具"
echo ""
echo "提示："
echo "1. 首次运行可能需要较长时间"
echo "2. 需要将 ChromeDriver 放在同一目录"
echo "3. 需要安装 FFmpeg 才能使用合并功能"
echo ""
