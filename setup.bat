@echo off
chcp 65001 >nul
echo ========================================
echo 视频爬虫工具 - 自动安装脚本
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

echo [2/4] 安装 Python 依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] Python 依赖安装失败，请检查网络连接
    pause
)
echo.

echo [3/4] 检查 Node.js 环境（可选）...
node --version >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到 Node.js，跳过 Node.js 依赖安装
    echo [提示] Node.js 是可选的，不影响核心功能
    echo [提示] 如需增强功能，请安装 Node.js: https://nodejs.org/
) else (
    node --version
    echo [4/4] 安装 Node.js 依赖...
    call npm install
    if errorlevel 1 (
        echo [警告] Node.js 依赖安装失败，请检查网络连接
    )
)
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 快速开始:
echo   python main.py https://example.com/videos
echo.
echo 查看帮助:
echo   python main.py --help
echo.
echo 详细文档请查看 README.md
echo.
pause
