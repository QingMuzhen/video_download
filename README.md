# 视频爬虫工具 (Video Slider)

一个功能强大的多语言视频爬虫工具，支持**智能自动检测**、HTML解析、网络抓包、流媒体下载、音视频合并和加密视频解密。

## ✨ 核心特性

### 🤖 智能自动检测
- **自动识别URL类型**：HLS流、DASH流、直接视频文件或普通网页
- **智能选择策略**：根据网站特征自动选择最佳下载方式
- **自动检测分离流**：识别并自动合并分离的音视频流
- **质量智能排序**：自动选择最高质量的视频
- **零配置使用**：用户只需提供URL，程序自动处理一切

### 🔐 高级功能
- **Cookie/Referer 自动获取**：真实化请求，绕过反爬虫检测
- **关键词搜索**：通过关键词过滤和匹配视频URL
- **加密视频解密**：支持B站 webmask 等加密格式自动解密
- **多语言支持**：Python + Node.js 协同工作，性能优化
- **反检测技术**：隐藏 WebDriver 特征，模拟真实浏览器

### 🎯 功能特性
- 🔍 HTML解析模式（静态网页）
- 📡 网络抓包模式（动态网页）
- 🎬 HLS/DASH流媒体支持
- 🎵 音视频分离下载与合并
- 🔓 加密视频自动解密
- 🍪 Cookie/Referer 智能管理
- 🔎 关键词搜索和过滤
- ⚡ 多线程并发下载
- 📊 实时进度显示
- 🔄 断点续传
- 🔁 智能重试机制
- 🌐 代理支持
- 📝 完整日志记录
- ✅ 文件完整性验证

### 支持的格式
- **视频格式**: mp4, avi, mov, wmv, flv, mkv, webm, mpg, mpeg, 3gp
- **流媒体**: HLS (.m3u8), DASH (.mpd)
- **分离流**: 自动检测并合并音视频

## 🚀 快速开始

### 方式1：GUI 可视化界面（推荐）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 GUI
python gui.py
```

或者直接运行打包好的 exe 文件（无需安装Python）：
```bash
# Windows
dist\视频爬虫工具.exe
```

详细说明请查看 [`GUI_README.md`](GUI_README.md:1)

### 方式2：命令行模式

```bash
# 1. 克隆项目
git clone <repository-url>
cd video_lider

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. （可选）安装 Node.js 依赖（用于增强功能）
npm install
```

### 配置文件

项目使用 [`config.ini`](config.ini:1) 进行集中配置：

```ini
[download]
output_dir = downloads      # 下载目录
max_downloads = 10          # 最大下载数量
workers = 3                 # 并发线程数

[capture]
headless = true             # 无头浏览器模式
wait_time = 10              # 抓包等待时间（秒）
keywords = video,stream     # 默认搜索关键词

[proxy]
enabled = false             # 是否启用代理
http_proxy =                # HTTP代理地址
https_proxy =               # HTTPS代理地址

[platforms]
bilibili_decrypt = true     # B站视频自动解密
auto_merge = true           # 自动合并音视频

[nodejs]
enabled = true              # 启用Node.js辅助脚本
analyzer_script = scripts/analyze.js
decryptor_script = scripts/decrypt.js
```

### 基础使用（推荐）

**只需提供URL，程序会自动处理一切！**

```bash
# 自动模式 - 程序会智能检测并选择最佳策略
python main.py https://example.com/videos

# 指定保存目录
python main.py https://example.com/videos -o ./my_videos

# 下载更多视频
python main.py https://example.com/videos -m 20
```

就这么简单！程序会：
1. 🔍 自动分析URL类型
2. 🤖 智能选择最佳下载策略
3. 📡 必要时自动启用抓包
4. 🎵 自动检测并合并分离的音视频
5. ⬇️ 自动下载所有视频

## 🖥️ GUI 界面

### 启动 GUI
```bash
python gui.py
```

### 主要功能
- 📝 可视化URL输入和配置
- 📊 实时进度显示
- 📋 彩色日志输出
- ⚙️ 完整的选项配置
- 📁 一键打开下载目录
- 🎯 智能检测和推荐

### 打包成 EXE
```bash
# Windows
build.bat

# Linux/Mac
chmod +x build.sh && ./build.sh
```

详细说明：[`GUI_README.md`](GUI_README.md:1)

## 📖 使用指南

### 智能自动模式（推荐）

程序会自动检测以下情况：

#### 1. HLS流媒体
```bash
python main.py https://example.com/playlist.m3u8
```
✅ 自动识别为HLS流，下载并合并所有片段

#### 2. 视频平台（YouTube、B站等）
```bash
python main.py https://www.bilibili.com/video/xxxxx
```
✅ 自动启用抓包模式，捕获动态加载的视频

#### 3. 普通网页
```bash
python main.py https://example.com/videos
```
✅ 自动使用HTML解析，快速提取视频链接

#### 4. 分离的音视频流
```bash
python main.py https://example.com/videos
```
✅ 自动检测分离流，下载并使用FFmpeg合并

### 命令行选项

#### 基本选项
```bash
-o, --output DIR          # 保存目录 (默认: downloads)
-m, --max-downloads N     # 最大下载数量 (默认: 10)
-k, --keywords WORDS      # 搜索关键词（逗号分隔）
```

#### 下载选项
```bash
-w, --workers N           # 并发线程数 (默认: 3)
-r, --retries N           # 重试次数 (默认: 3)
--proxy URL               # 代理服务器
--resume                  # 启用断点续传
--no-verify               # 跳过文件验证
```

#### 高级选项（覆盖自动检测）
```bash
--force-capture           # 强制使用抓包模式
--force-hls               # 强制使用HLS模式
--no-merge                # 禁用音视频合并
--no-decrypt              # 禁用加密视频解密
--wait-time N             # 抓包等待时间（秒）
```

## 💡 使用示例

### 示例1: 最简单的使用
```bash
python main.py https://example.com/videos
```

### 示例2: 指定保存位置和数量
```bash
python main.py https://example.com/videos -o ./downloads -m 20
```

### 示例3: 使用代理
```bash
python main.py https://example.com/videos --proxy http://127.0.0.1:7890
```

### 示例4: 启用断点续传和多线程
```bash
python main.py https://example.com/videos --resume -w 5
```

### 示例5: 强制使用抓包模式
```bash
python main.py https://example.com/videos --force-capture
```

### 示例6: 使用关键词搜索
```bash
python main.py https://example.com/videos -k "1080p,high,quality"
```

### 示例7: 完整配置
```bash
python main.py https://example.com/videos \
  -o ./my_videos \
  -m 20 \
  -w 5 \
  -r 3 \
  -k "video,stream" \
  --resume \
  --proxy http://127.0.0.1:7890
```

## 🔧 依赖说明

### 必需依赖
```bash
pip install requests beautifulsoup4 tqdm
```

### 网络抓包功能（强烈推荐）
```bash
pip install selenium
```
还需要安装Chrome浏览器和ChromeDriver

**作用**:
- 捕获动态加载的视频（YouTube、B站等）
- 自动获取 Cookie 和 Referer
- 绕过反爬虫检测

### 音视频合并功能（强烈推荐）
下载并安装FFmpeg: https://ffmpeg.org/download.html

**作用**:
- 合并分离的音视频流
- 解密加密视频（webmask等）

### Node.js 增强功能（可选）
```bash
npm install
```

**作用**:
- 使用 Puppeteer 进行更强大的页面分析
- 提供备用的视频解密方案
- 增强网络请求捕获能力

**Node.js 脚本**:
- [`scripts/analyze.js`](scripts/analyze.js:1) - 深度页面分析和视频URL提取
- [`scripts/decrypt.js`](scripts/decrypt.js:1) - 加密视频解密工具

## 🎯 工作原理

### 智能检测流程

```
用户输入URL
    ↓
🔍 分析URL类型
    ↓
┌─────────────────────────────────┐
│  .m3u8?  → HLS流下载            │
│  .mpd?   → DASH流下载           │
│  .mp4?   → 直接下载             │
│  网页?   → 继续分析...          │
└─────────────────────────────────┘
    ↓
📄 获取HTML内容
    ↓
🤖 智能判断
    ↓
┌─────────────────────────────────┐
│  视频平台? → 启用抓包模式       │
│  动态加载? → 启用抓包模式       │
│  静态网页? → HTML解析模式       │
└─────────────────────────────────┘
    ↓
📡 执行下载策略
    ↓
┌─────────────────────────────────┐
│  发现HLS流? → 下载并合并片段    │
│  发现分离流? → 下载并合并音视频 │
│  发现直接链接? → 并发下载       │
└─────────────────────────────────┘
    ↓
✅ 下载完成
```

### 支持的网站类型

#### 自动启用抓包的平台
- YouTube / Youku
- Bilibili / 抖音
- 爱奇艺 / 腾讯视频
- Vimeo / Dailymotion
- Twitch / Facebook
- Instagram / Twitter

#### HTML解析适用的网站
- 静态视频网站
- 直接视频链接
- 简单的视频列表页面

## 📁 项目结构

```
video_lider/
├── main.py                    # 主程序（智能自动模式）
├── config.ini                 # 配置文件 ⭐
├── package.json               # Node.js 依赖 ⭐
├── utils/                     # Python 工具模块
│   ├── __init__.py           # 模块初始化
│   ├── logger.py             # 日志系统
│   ├── parser.py             # HTML解析器
│   ├── downloader.py         # 视频下载器（支持Cookie/Referer）⭐
│   ├── capture.py            # 网络抓包器（反检测+关键词搜索）⭐
│   ├── stream.py             # 流媒体下载器
│   ├── merger.py             # 音视频合并器
│   ├── detector.py           # 智能检测器
│   ├── cookie_manager.py     # Cookie管理器 ⭐
│   ├── crypto.py             # 加密视频处理器 ⭐
│   └── config.py             # 配置读取器 ⭐
├── scripts/                   # Node.js 脚本 ⭐
│   ├── analyze.js            # Puppeteer 页面分析器
│   └── decrypt.js            # Node.js 解密工具
├── requirements.txt           # Python 依赖列表
├── README.md                 # 项目文档
└── .gitignore                # Git配置
```

## ❓ 常见问题

### Q: 如何使用？
A: 最简单的方式：`python main.py <URL>`，程序会自动处理一切。

### Q: 程序如何知道使用哪种模式？
A: 程序会自动分析URL和网页内容，智能选择最佳策略。你也可以使用`--force-capture`或`--force-hls`手动指定。

### Q: 需要安装selenium吗？
A: 对于静态网页不需要。但对于YouTube、B站等动态网站，强烈建议安装以获得最佳效果和反检测能力。

### Q: 需要安装FFmpeg吗？
A: 如果视频的音频和视频是分离的，或者需要解密加密视频，需要FFmpeg。程序会自动检测并提示。

### Q: 需要安装Node.js吗？
A: 不是必需的。Node.js脚本提供增强功能，但Python版本已经足够强大。

### Q: 下载速度慢怎么办？
A: 使用`-w`参数增加并发线程数，例如：`-w 5`

### Q: 某些网站无法下载？
A: 尝试使用`--force-capture`强制启用抓包模式，或配置代理`--proxy`。程序会自动获取Cookie和Referer来绕过检测。

### Q: 如何下载高质量视频？
A: 程序会自动选择最高质量的视频。如果有多个质量选项，会优先选择4K/1080p等高质量版本。

### Q: 下载的是 .webmask 文件怎么办？
A: 程序会自动检测并解密B站的 webmask 加密格式，转换为标准的 MP4 文件。

### Q: 如何使用关键词搜索？
A: 使用 `-k` 参数指定关键词，例如：`-k "1080p,high"` 或在 [`config.ini`](config.ini:17) 中设置默认关键词。

### Q: Cookie 和 Referer 是如何获取的？
A: 在抓包模式下，程序会自动从浏览器中提取 Cookie 和 Referer，并在下载时使用，无需手动配置。

## ⚠️ 注意事项

1. **遵守法律**: 遵守目标网站的robots.txt和服务条款
2. **合理使用**: 避免过于频繁的请求
3. **个人使用**: 仅用于学习和个人使用
4. **版权保护**: 遵守版权法规
5. **资源占用**: 抓包模式会启动浏览器，占用较多资源

## 🛠️ 技术栈

### Python 核心
- Python 3.7+
- Requests - HTTP客户端
- BeautifulSoup4 - HTML解析
- Selenium - 浏览器自动化（可选）
- tqdm - 进度条
- FFmpeg - 音视频处理（可选）

### Node.js 增强（可选）
- Node.js 14+
- Puppeteer - 无头浏览器
- Axios - HTTP客户端
- Cheerio - HTML解析

### 核心技术
- 网络抓包与请求分析
- HLS/DASH 流媒体协议
- XOR 加密/解密算法
- Cookie/Referer 管理
- 反检测技术（WebDriver隐藏）
- 多线程并发下载
- 智能URL检测与分类

## 📝 更新日志

### v4.0 (2026-02-21) - 多语言增强版
- 🌐 **新增 Node.js 多语言支持**
- 🔐 **Cookie/Referer 自动获取和管理**
- 🔎 **关键词搜索和智能过滤**
- 🔓 **加密视频自动解密（webmask等）**
- 🛡️ **反检测技术（隐藏WebDriver）**
- ⚙️ **配置文件支持（config.ini）**
- 📊 **相关性评分系统**
- 🎯 **多置信度URL分类**

### v3.0 (2026-02-21)
- 🤖 **新增智能自动检测功能**
- ✨ 自动识别URL类型和网站特征
- ✨ 智能选择最佳下载策略
- ✨ 自动检测并合并分离的音视频流
- ✨ 支持网络抓包和流媒体下载
- 📝 简化使用方式，零配置即可使用

### v2.0
- ✨ 模块化代码结构
- ✨ 多线程并发下载
- ✨ 断点续传功能
- ✨ 智能重试机制

### v1.0
- 🎉 初始版本
- 基础HTML解析和下载

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 🔧 高级用法

### 使用 Node.js 脚本

#### 1. 深度页面分析
```bash
node scripts/analyze.js https://example.com/video
```
输出: `video_urls.json` - 包含所有发现的视频URL

#### 2. 解密加密视频
```bash
node scripts/decrypt.js input.webmask output.mp4
```

### 自定义配置

编辑 [`config.ini`](config.ini:1) 来自定义默认行为：

```ini
[capture]
keywords = 1080p,high,quality,video  # 自定义搜索关键词

[platforms]
bilibili_decrypt = true              # 自动解密B站视频
auto_merge = true                    # 自动合并音视频

[nodejs]
enabled = true                       # 启用Node.js增强功能
```

### Cookie 管理

程序会自动管理Cookie，但你也可以手动操作：

```python
from utils import CookieManager

# 保存Cookie
manager = CookieManager()
manager.save_cookies(cookies, 'cookies.json')

# 加载Cookie
cookies = manager.load_cookies('cookies.json')
```

### 加密视频处理

```python
from utils import EncryptedVideoHandler

handler = EncryptedVideoHandler()
# 自动检测并解密
handler.process_directory('downloads/')
```

---

**提示**: 大多数情况下，你只需要运行 `python main.py <URL>`，程序会自动处理一切！
