# 视频爬虫工具 v4.0 - 完整功能版

一个功能强大的**多语言多功能资源下载工具**，支持智能检测、多类型资源下载、任务队列管理、Web界面和RESTful API。

## 🎉 v4.0 新增功能

### 🆕 核心增强
- ✨ **通用资源下载器** - 支持图片、音频、文档、字体等多种文件类型
- 🔍 **智能资源检测器** - 自动识别页面中的所有资源（图片、视频、音频、文档等）
- 📋 **任务队列管理** - 批量下载任务管理，支持暂停、继续、重试
- 💾 **SQLite数据库** - 完整的下载历史记录和统计
- 🌐 **Flask API服务器** - RESTful API接口，支持远程调用
- 🎨 **现代化Web界面** - 美观的浏览器界面，实时进度显示
- 🚀 **增强Node.js脚本** - 更强大的资源分析和下载功能

### 📦 支持的资源类型
- **视频**: mp4, avi, mov, wmv, flv, mkv, webm, m3u8, mpd
- **图片**: jpg, png, gif, bmp, webp, svg, ico, tiff
- **音频**: mp3, wav, flac, aac, ogg, m4a, wma, opus
- **文档**: pdf, doc, docx, xls, xlsx, ppt, pptx, txt
- **压缩包**: zip, rar, 7z, tar, gz, bz2
- **字体**: ttf, otf, woff, woff2, eot
- **其他**: 自动检测

## 🚀 快速开始

### 安装依赖

```bash
# Python依赖
pip install -r requirements.txt

# Node.js依赖（可选，用于增强功能）
npm install
```

### 使用方式

#### 1. Web界面（推荐）

启动API服务器：
```bash
python api_server.py
```

然后在浏览器中打开：`http://localhost:5000`

功能特性：
- 📡 智能资源检测 - 输入网页URL，自动检测所有资源
- ⬇️ 批量下载 - 一键下载某类型的所有资源
- 📊 实时进度 - 查看下载进度和状态
- 📋 任务管理 - 暂停、继续、取消、重试任务
- 📈 统计信息 - 查看下载统计和历史记录

#### 2. GUI界面

```bash
python gui.py
```

#### 3. 命令行模式

```bash
# 原有的视频下载功能
python main.py https://example.com/videos

# 使用新的资源下载功能（开发中）
python resource_cli.py https://example.com --type image
```

#### 4. Node.js脚本

```bash
# 分析网页资源
node scripts/analyze.js https://example.com

# 批量下载
node scripts/download.js --json=resources.json

# 下载单个文件
node scripts/download.js https://example.com/file.mp4
```

## 📖 详细使用指南

### Web API接口

#### 检测资源
```bash
POST /api/detect
Content-Type: application/json

{
  "url": "https://example.com"
}
```

响应：
```json
{
  "success": true,
  "resources": {
    "images": ["url1", "url2"],
    "videos": ["url3"],
    "audios": ["url4"]
  },
  "statistics": {
    "total": 4,
    "byType": {
      "images": 2,
      "videos": 1,
      "audios": 1
    }
  }
}
```

#### 创建下载任务
```bash
POST /api/tasks
Content-Type: application/json

{
  "url": "https://example.com/file.mp4",
  "resource_type": "video"
}
```

#### 批量创建任务
```bash
POST /api/tasks/batch
Content-Type: application/json

{
  "urls": ["url1", "url2", "url3"],
  "resource_type": "image"
}
```

#### 获取任务列表
```bash
GET /api/tasks
```

#### 任务操作
```bash
POST /api/tasks/{task_id}/pause    # 暂停
POST /api/tasks/{task_id}/resume   # 继续
POST /api/tasks/{task_id}/cancel   # 取消
POST /api/tasks/{task_id}/retry    # 重试
```

#### 获取统计信息
```bash
GET /api/statistics
GET /api/tasks/statistics
```

#### 搜索历史
```bash
GET /api/history/search?keyword=video
```

### Python API使用

```python
from utils import (
    ResourceDownloader,
    ResourceDetector,
    TaskManager,
    DatabaseManager
)

# 资源检测
detector = ResourceDetector()
resources = detector.detect_all_resources('https://example.com')
print(f"找到 {len(resources['images'])} 张图片")

# 资源下载
downloader = ResourceDownloader(output_dir='downloads')
result = downloader.download_resource('https://example.com/image.jpg')

# 批量下载
urls = ['url1', 'url2', 'url3']
results = downloader.download_batch(urls)
print(f"成功: {len(results['success'])}, 失败: {len(results['failed'])}")

# 任务管理
task_manager = TaskManager(max_workers=5)
task_manager.start(download_function)

task_id = task_manager.add_task('https://example.com/file.mp4', 'video')
task = task_manager.get_task(task_id)
print(f"任务状态: {task.status}")

# 数据库操作
db = DatabaseManager()
db.add_download_record(task_id, url, 'video')
history = db.get_download_history(limit=10)
stats = db.get_statistics()
```

### Node.js API使用

```javascript
const { analyzeResources } = require('./scripts/analyze');
const { downloadBatch } = require('./scripts/download');

// 分析资源
analyzeResources('https://example.com', {
    headless: true,
    outputFile: 'resources.json'
}).then(result => {
    console.log(`找到 ${result.statistics.total} 个资源`);
});

// 批量下载
const urls = ['url1', 'url2', 'url3'];
downloadBatch(urls, 'downloads', {
    concurrency: 3,
    onProgress: (url, progress) => {
        console.log(`${url}: ${progress}%`);
    }
}).then(results => {
    console.log(`成功: ${results.success.length}`);
});
```

## 🏗️ 项目结构

```
video_slider/
├── main.py                    # 主程序（视频下载）
├── gui.py                     # GUI界面
├── api_server.py             # Flask API服务器 ⭐新增
├── config.ini                # 配置文件
├── requirements.txt          # Python依赖
├── package.json              # Node.js依赖
│
├── utils/                    # Python工具模块
│   ├── __init__.py
│   ├── logger.py            # 日志系统
│   ├── parser.py            # HTML解析器
│   ├── downloader.py        # 视频下载器
│   ├── capture.py           # 网络抓包器
│   ├── stream.py            # 流媒体下载器
│   ├── merger.py            # 音视频合并器
│   ├── detector.py          # 智能检测器
│   ├── cookie_manager.py    # Cookie管理器
│   ├── crypto.py            # 加密视频处理器
│   ├── config.py            # 配置读取器
│   ├── version.py           # 版本管理器
│   ├── resource_downloader.py  # 通用资源下载器 ⭐新增
│   ├── resource_detector.py    # 智能资源检测器 ⭐新增
│   ├── database.py             # 数据库管理器 ⭐新增
│   └── task_manager.py         # 任务管理器 ⭐新增
│
├── scripts/                  # Node.js脚本
│   ├── analyze.js           # 资源分析脚本 ⭐增强
│   ├── download.js          # 资源下载脚本 ⭐新增
│   └── decrypt.js           # 解密工具
│
├── web/                      # Web界面 ⭐新增
│   ├── index.html           # 主页面
│   ├── static/              # 静态资源
│   └── templates/           # 模板
│
├── data/                     # 数据目录 ⭐新增
│   └── downloads.db         # SQLite数据库
│
├── downloads/                # 下载目录
│   ├── video/               # 视频文件
│   ├── image/               # 图片文件
│   ├── audio/               # 音频文件
│   ├── document/            # 文档文件
│   └── other/               # 其他文件
│
└── logs/                     # 日志目录
```

## 🎯 使用场景

### 场景1: 批量下载网站图片
```python
from utils import ResourceDetector, ResourceDownloader

# 检测图片
detector = ResourceDetector()
resources = detector.detect_all_resources('https://example.com')

# 下载所有图片
downloader = ResourceDownloader()
results = downloader.download_by_type(
    resources['images'], 
    ['image']
)
```

### 场景2: 下载在线课程视频
```bash
# 使用Web界面
1. 启动服务器: python api_server.py
2. 打开浏览器: http://localhost:5000
3. 输入课程页面URL
4. 点击"开始检测"
5. 选择视频类型，批量下载
```

### 场景3: 备份网站资源
```bash
# 使用Node.js脚本
node scripts/analyze.js https://example.com --output=backup.json
node scripts/download.js --json=backup.json
```

### 场景4: API集成
```python
import requests

# 创建下载任务
response = requests.post('http://localhost:5000/api/tasks', json={
    'url': 'https://example.com/file.mp4',
    'resource_type': 'video'
})

task_id = response.json()['task_id']

# 查询任务状态
response = requests.get(f'http://localhost:5000/api/tasks/{task_id}')
task = response.json()['task']
print(f"进度: {task['progress']}%")
```

## 🔧 配置说明

[`config.ini`](config.ini:1) 配置文件：

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

[api]
host = 0.0.0.0             # API服务器地址
port = 5000                # API服务器端口
debug = false              # 调试模式

[database]
path = data/downloads.db   # 数据库路径
auto_cleanup_days = 30     # 自动清理天数
```

## 📊 数据库结构

项目使用SQLite数据库记录下载历史：

- **download_history** - 下载历史记录
- **resource_info** - 资源信息缓存
- **site_statistics** - 网站统计
- **tags** - 标签管理
- **download_tags** - 下载-标签关联

## 🌟 技术栈

### Python
- **Flask** - Web框架和API服务器
- **Requests** - HTTP客户端
- **BeautifulSoup4** - HTML解析
- **Selenium** - 浏览器自动化
- **SQLite3** - 数据库
- **Threading** - 多线程并发

### Node.js
- **Puppeteer** - 无头浏览器
- **Axios** - HTTP客户端
- **Cheerio** - HTML解析

### 前端
- **原生JavaScript** - 无框架依赖
- **CSS3** - 现代化样式
- **Fetch API** - 异步请求

## ⚡ 性能优化

- ✅ 多线程并发下载
- ✅ 断点续传支持
- ✅ 智能重试机制
- ✅ 资源类型自动检测
- ✅ 数据库索引优化
- ✅ 任务队列管理
- ✅ 内存占用优化

## 🔒 安全特性

- ✅ Cookie自动管理
- ✅ Referer自动设置
- ✅ User-Agent伪装
- ✅ 反爬虫检测绕过
- ✅ 代理支持
- ✅ CORS跨域支持

## 📝 更新日志

### v4.0 (2026-02-21) - 全面升级版
- 🎉 **新增通用资源下载器** - 支持多种文件类型
- 🔍 **新增智能资源检测器** - 自动识别页面资源
- 📋 **新增任务队列管理** - 批量任务管理
- 💾 **新增SQLite数据库** - 完整历史记录
- 🌐 **新增Flask API服务器** - RESTful接口
- 🎨 **新增Web界面** - 现代化浏览器界面
- 🚀 **增强Node.js脚本** - 更强大的功能
- 📊 **新增统计功能** - 详细的下载统计

### v3.0 (2026-02-21)
- 🤖 智能自动检测功能
- ✨ 自动识别URL类型
- ✨ 智能选择下载策略

### v2.0
- ✨ 模块化代码结构
- ✨ 多线程并发下载

### v1.0
- 🎉 初始版本

## ❓ 常见问题

**Q: 如何启动Web界面？**
A: 运行 `python api_server.py`，然后访问 `http://localhost:5000`

**Q: 支持哪些资源类型？**
A: 支持视频、图片、音频、文档、压缩包、字体等多种类型

**Q: 如何批量下载？**
A: 使用Web界面的资源检测功能，或使用API的批量创建接口

**Q: 下载历史保存在哪里？**
A: 保存在 `data/downloads.db` SQLite数据库中

**Q: 如何查看下载进度？**
A: 在Web界面实时查看，或通过API查询任务状态

**Q: 支持断点续传吗？**
A: 支持，任务失败后可以重试继续下载





## 🔗 相关链接

- [原版README](README.md:1)
- [GUI使用指南](GUI_README.md:1)
- [使用示例](EXAMPLES.md:1)

---

**提示**: 这是一个功能完整的多用途资源下载工具，适合学习和个人使用。请遵守目标网站的服务条款和版权法规。
