# 使用示例

## 快速开始

### 1. 最简单的使用
```bash
python main.py https://example.com/videos
```

### 2. B站视频下载
```bash
python main.py https://www.bilibili.com/video/....
```
程序会自动：
- 启动浏览器抓包
- 获取 Cookie 和 Referer
- 下载视频（自动解密 webmask）
- 合并音视频（如果分离）

### 3. YouTube 视频下载
```bash
python main.py https://www.youtube.com/watch?v=xxxxx
```

### 4. HLS 流媒体下载
```bash
python main.py https://example.com/video/playlist.m3u8
```

## 进阶使用

### 使用关键词过滤
```bash
# 只下载包含 "1080p" 或 "high" 的视频
python main.py https://example.com/videos -k "1080p,high"
```

### 批量下载
```bash
# 下载最多 20 个视频
python main.py https://example.com/videos -m 20
```

### 使用代理
```bash
python main.py https://example.com/videos --proxy http://127.0.0.1:7890
```

### 多线程下载
```bash
# 使用 5 个线程并发下载
python main.py https://example.com/videos -w 5
```

### 断点续传
```bash
python main.py https://example.com/videos --resume
```

### 完整配置示例
```bash
python main.py https://example.com/videos \
  -o ./downloads \
  -m 20 \
  -w 5 \
  -r 3 \
  -k "1080p,high,quality" \
  --resume \
  --proxy http://127.0.0.1:7890
```

## Node.js 脚本使用

### 深度页面分析
```bash
node scripts/analyze.js https://example.com/video
```
输出文件：`video_urls.json`

### 解密加密视频
```bash
node scripts/decrypt.js input.webmask output.mp4
```

## 配置文件使用

编辑 `config.ini` 来设置默认行为：

```ini
[download]
output_dir = downloads
max_downloads = 10
workers = 3

[capture]
headless = true
wait_time = 10
keywords = 1080p,high,quality

[proxy]
enabled = true
http_proxy = http://127.0.0.1:7890
https_proxy = http://127.0.0.1:7890

[platforms]
bilibili_decrypt = true
auto_merge = true

[nodejs]
enabled = true
```

## 常见场景

### 场景1：下载B站视频
```bash
# 自动处理 webmask 加密和音视频分离
python main.py https://www.bilibili.com/video/BV1234567890
```

### 场景2：下载整个视频列表
```bash
# 下载页面中的所有视频
python main.py https://example.com/video-list -m 50
```

### 场景3：只下载高清视频
```bash
# 使用关键词过滤
python main.py https://example.com/videos -k "1080p,4k,hd"
```

### 场景4：通过代理下载
```bash
# 使用代理绕过地区限制
python main.py https://example.com/videos --proxy http://127.0.0.1:7890
```

### 场景5：强制使用抓包模式
```bash
# 对于动态加载的网站
python main.py https://example.com/videos --force-capture
```

## Python API 使用

### 基础下载
```python
from utils import VideoDownloader, setup_logger

logger = setup_logger()
downloader = VideoDownloader(logger=logger)

# 下载单个视频
downloader.download('https://example.com/video.mp4', 'output.mp4')
```

### 使用抓包
```python
from utils import NetworkCapture, setup_logger

logger = setup_logger()
capture = NetworkCapture(headless=True, logger=logger)

# 抓取视频URL
video_urls = capture.start_capture('https://example.com/video', wait_time=10)
cookies = capture.get_cookies()
referer = capture.get_referer()

print(f"找到 {len(video_urls)} 个视频")
```

### 关键词搜索
```python
from utils import NetworkCapture

capture = NetworkCapture()
capture.start_capture('https://example.com/videos')

# 搜索包含关键词的视频
results = capture.search_video_urls_by_keywords(['1080p', 'high'])
print(f"找到 {len(results)} 个匹配的视频")
```

### 加密视频解密
```python
from utils import EncryptedVideoHandler

handler = EncryptedVideoHandler()

# 解密单个文件
handler.decrypt_bilibili_webmask('input.webmask', 'output.mp4')

# 批量处理目录
handler.process_directory('downloads/')
```

### Cookie 管理
```python
from utils import CookieManager

manager = CookieManager()

# 保存 Cookie
manager.save_cookies(cookies, 'cookies.json')

# 加载 Cookie
cookies = manager.load_cookies('cookies.json')

# 转换格式
requests_cookies = manager.selenium_to_requests(selenium_cookies)
```

### 智能检测
```python
from utils import SmartDetector

detector = SmartDetector()

# 检测 URL 类型
url_type = detector.detect_url_type('https://example.com/video.m3u8')
print(f"URL 类型: {url_type}")  # 输出: hls

# 推荐策略
strategy = detector.recommend_strategy('https://www.bilibili.com/video/xxx')
print(f"推荐方法: {strategy['method']}")
print(f"使用抓包: {strategy['use_capture']}")
```

## 故障排除

### 问题1：浏览器启动失败
```bash
# 检查 ChromeDriver 是否安装
chromedriver --version

# 如果未安装，下载对应版本
# https://chromedriver.chromium.org/downloads
```

### 问题2：FFmpeg 未找到
```bash
# 检查 FFmpeg 是否安装
ffmpeg -version

# 如果未安装，下载安装
# https://ffmpeg.org/download.html
```

### 问题3：下载速度慢
```bash
# 增加并发线程数
python main.py https://example.com/videos -w 10

# 使用代理
python main.py https://example.com/videos --proxy http://127.0.0.1:7890
```

### 问题4：某些网站无法下载
```bash
# 强制使用抓包模式
python main.py https://example.com/videos --force-capture

# 增加等待时间
python main.py https://example.com/videos --wait-time 20
```

### 问题5：视频无法播放
```bash
# 检查是否是加密视频
# 程序会自动解密，如果失败可以手动解密
node scripts/decrypt.js input.webmask output.mp4
```

## 最佳实践

1. **首次使用**：先用简单的 URL 测试
   ```bash
   python main.py https://example.com/video.mp4
   ```

2. **动态网站**：使用抓包模式
   ```bash
   python main.py https://www.bilibili.com/video/xxx --force-capture
   ```

3. **批量下载**：合理设置并发数
   ```bash
   python main.py https://example.com/videos -m 50 -w 5
   ```

4. **网络不稳定**：启用断点续传和增加重试
   ```bash
   python main.py https://example.com/videos --resume -r 5
   ```

5. **需要代理**：在配置文件中设置
   ```ini
   [proxy]
   enabled = true
   http_proxy = http://127.0.0.1:7890
   ```

6. **关键词过滤**：在配置文件中设置默认关键词
   ```ini
   [capture]
   keywords = 1080p,high,quality,video
   ```
