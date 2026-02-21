@echo off
chcp 65001 >nul
echo ========================================
echo 视频爬虫工具 - 打包脚本
echo ========================================
echo.

echo [1/3] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)
echo ✓ PyInstaller 已就绪
echo.

echo [2/3] 清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
echo ✓ 清理完成
echo.

echo [3/3] 开始打包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

python -m PyInstaller --clean video_downloader.spec

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可执行文件位置: dist\视频爬虫工具.exe
echo.
echo 提示：
echo 1. 首次运行可能需要较长时间
echo 2. 需要将 ChromeDriver 放在同一目录
echo 3. 需要安装 FFmpeg 才能使用合并功能
echo.
pause
