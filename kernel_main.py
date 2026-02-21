"""视频爬虫工具 - 主程序（智能自动模式）"""

import argparse
import sys
import os
import requests
from utils import (
    setup_logger,
    VideoParser,
    VideoDownloader,
    NetworkCapture,
    MediaMerger,
    StreamDownloader,
    SmartDetector,
    EncryptedVideoHandler
)


def get_html_content(url, proxy=None, logger=None):
    """
    获取网页HTML内容
    
    Args:
        url: 目标URL
        proxy: 代理服务器地址
        logger: 日志记录器
    
    Returns:
        str: HTML内容，失败返回None
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        
        if logger:
            logger.info(f"正在获取网页内容: {url}")
        
        response = requests.get(url, headers=headers, timeout=30, proxies=proxies)
        response.raise_for_status()
        
        if logger:
            logger.info(f"成功获取网页内容，大小: {len(response.text)} 字节")
        
        return response.text
    
    except requests.exceptions.RequestException as e:
        if logger:
            logger.error(f"获取网页内容失败: {e}")
        else:
            print(f"获取网页内容失败: {e}")
        return None
    except Exception as e:
        if logger:
            logger.error(f"未知错误: {e}")
        else:
            print(f"未知错误: {e}")
        return None


def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing_deps = []
    
    try:
        import requests
    except ImportError:
        missing_deps.append('requests')
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        missing_deps.append('beautifulsoup4')
    
    try:
        import tqdm
    except ImportError:
        missing_deps.append('tqdm')
    
    if missing_deps:
        print("错误: 缺少必要的依赖库")
        print(f"缺失依赖: {', '.join(missing_deps)}")
        print("\n请运行以下命令安装依赖:")
        print("  pip install -r requirements.txt")
        print("\n或者手动安装:")
        print(f"  pip install {' '.join(missing_deps)}")
        return False
    
    return True


def check_optional_dependencies():
    """检查可选依赖"""
    optional_deps = {}
    
    try:
        import selenium
        optional_deps['selenium'] = True
    except ImportError:
        optional_deps['selenium'] = False
    
    return optional_deps


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='视频爬虫工具 - 智能自动检测模式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 自动模式（推荐）- 程序会自动检测并选择最佳策略
  %(prog)s https://example.com/videos
  
  # 指定输出目录和下载数量
  %(prog)s https://example.com/videos -o ./my_videos -m 20
  
  # 使用代理
  %(prog)s https://example.com/videos --proxy http://127.0.0.1:7890
  
  # 手动指定模式（高级用户）
  %(prog)s https://example.com/videos --force-capture
  %(prog)s https://example.com/playlist.m3u8 --force-hls
        """
    )
    
    # 必需参数
    parser.add_argument('url', help='目标网站URL')
    
    # 基本选项
    basic_group = parser.add_argument_group('基本选项')
    basic_group.add_argument(
        '-o', '--output',
        default='downloads',
        help='视频保存目录 (默认: downloads)'
    )
    basic_group.add_argument(
        '-m', '--max-downloads',
        type=int,
        default=10,
        help='最大下载数量 (默认: 10)'
    )
    
    # 下载选项
    download_group = parser.add_argument_group('下载选项')
    download_group.add_argument(
        '-w', '--workers',
        type=int,
        default=3,
        help='并发下载线程数 (默认: 3)'
    )
    download_group.add_argument(
        '-r', '--retries',
        type=int,
        default=3,
        help='下载失败重试次数 (默认: 3)'
    )
    download_group.add_argument(
        '--proxy',
        help='代理服务器地址 (例如: http://127.0.0.1:7890)'
    )
    download_group.add_argument(
        '--resume',
        action='store_true',
        help='启用断点续传'
    )
    download_group.add_argument(
        '--no-verify',
        action='store_true',
        help='跳过文件完整性验证'
    )
    
    # 高级选项（手动控制）
    advanced_group = parser.add_argument_group('高级选项（覆盖自动检测）')
    advanced_group.add_argument(
        '--force-capture',
        action='store_true',
        help='强制使用抓包模式'
    )
    advanced_group.add_argument(
        '--force-hls',
        action='store_true',
        help='强制使用HLS下载模式'
    )
    advanced_group.add_argument(
        '--no-merge',
        action='store_true',
        help='禁用自动音视频合并'
    )
    advanced_group.add_argument(
        '--wait-time',
        type=int,
        default=10,
        help='抓包模式页面加载等待时间（秒） (默认: 10)'
    )
    advanced_group.add_argument(
        '--keywords',
        help='搜索关键词（用逗号分隔多个关键词，例如: video,stream,play）'
    )
    
    # 其他选项
    other_group = parser.add_argument_group('其他选项')
    other_group.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='日志级别 (默认: INFO)'
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查可选依赖
    optional_deps = check_optional_dependencies()
    
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置日志
    import logging
    log_level = getattr(logging, args.log_level)
    logger = setup_logger(level=log_level)
    
    # 显示配置信息
    print("=" * 70)
    print("视频爬虫工具 v3.0 - 智能自动检测模式")
    print("=" * 70)
    print(f"目标URL: {args.url}")
    print(f"保存目录: {args.output}")
    print(f"最大下载数: {args.max_downloads}")
    print(f"并发线程数: {args.workers}")
    if args.proxy:
        print(f"代理服务器: {args.proxy}")
    print("=" * 70)
    print()
    
    logger.info("程序启动 - 智能自动检测模式")
    
    try:
        # 创建智能检测器
        detector = SmartDetector(logger=logger)
        
        # 初步检测URL类型
        print("🔍 正在分析URL...")
        url_type = detector.detect_url_type(args.url)
        
        # 获取推荐策略
        strategy = None
        html_content = None
        
        # 如果是网页，先获取HTML内容进行更详细的分析
        if url_type == 'webpage' and not args.force_hls and not args.force_capture:
            print("📄 获取网页内容进行分析...")
            html_content = get_html_content(args.url, args.proxy, logger)
            if html_content:
                strategy = detector.recommend_strategy(args.url, html_content)
            else:
                print("⚠️  无法获取网页内容，将尝试抓包模式")
                strategy = {'method': 'capture_and_analyze', 'use_capture': True, 'use_merge': True}
        else:
            strategy = detector.recommend_strategy(args.url)
        
        # 应用手动覆盖
        if args.force_capture:
            strategy['use_capture'] = True
            strategy['method'] = 'capture_and_analyze'
            print("🔧 手动启用抓包模式")
        
        if args.force_hls:
            strategy['use_hls'] = True
            strategy['method'] = 'hls_download'
            print("🔧 手动启用HLS下载模式")
        
        if args.no_merge:
            strategy['use_merge'] = False
            print("🔧 已禁用自动音视频合并")
        else:
            strategy['use_merge'] = strategy.get('use_merge', False)
        
        # 显示检测结果和策略
        print(f"\n✅ 检测完成")
        print(f"   URL类型: {url_type}")
        print(f"   推荐策略: {strategy['method']}")
        print()
        
        # 根据策略执行下载
        video_links = []
        captured_cookies = None
        captured_referer = None
        
        # 策略1: HLS流下载
        if strategy['method'] == 'hls_download':
            print("📺 HLS流下载模式")
            print("-" * 70)
            stream_downloader = StreamDownloader(output_dir=args.output, logger=logger)
            output_file = stream_downloader.download_hls(args.url, "video.mp4")
            
            if output_file:
                print(f"\n✅ 下载完成: {output_file}")
            else:
                print("\n❌ 下载失败")
            return
        
        # 策略2: 直接下载视频文件
        elif strategy['method'] == 'direct_download':
            print("📥 直接下载模式")
            print("-" * 70)
            video_links = [args.url]
        
        # 策略3: 抓包分析
        elif strategy['method'] == 'capture_and_analyze':
            if not optional_deps['selenium']:
                print("⚠️  抓包模式需要selenium，但未安装")
                print("   尝试使用HTML解析模式...")
                strategy['method'] = 'html_parse'
            else:
                print("🌐 网络抓包模式")
                print("-" * 70)
                print(f"   正在启动浏览器并分析网络请求...")
                print(f"   等待时间: {args.wait_time}秒")
                print()
                
                capture = NetworkCapture(headless=True, logger=logger)
                requests_list = capture.start_capture(args.url, wait_time=args.wait_time)
                
                # 获取Cookie和Referer
                captured_cookies = capture.get_cookies()
                captured_referer = capture.get_referer()
                
                if captured_cookies:
                    print(f"   ✅ 获取到 {len(captured_cookies)} 个Cookie")
                if captured_referer:
                    print(f"   ✅ 获取到Referer: {captured_referer[:50]}...")
                
                if requests_list:
                    # 解析关键词
                    keywords = None
                    if args.keywords:
                        keywords = [k.strip() for k in args.keywords.split(',')]
                        print(f"   🔍 使用关键词搜索: {', '.join(keywords)}")
                    
                    # 获取所有视频候选URL（使用增强的搜索）
                    print(f"\n📊 智能分析视频URL...")
                    candidates = capture.get_all_video_candidates(keywords=keywords)
                    
                    # 显示分析结果
                    print(f"   高置信度: {len(candidates['high_confidence'])} 个")
                    print(f"   中等置信度: {len(candidates['medium_confidence'])} 个")
                    if keywords:
                        print(f"   关键词匹配: {len(candidates['keyword_matches'])} 个")
                    
                    # 过滤视频请求
                    video_requests = capture.filter_video_requests(requests_list, keywords=keywords)
                    
                    if video_requests:
                        # 优先使用候选URL
                        print(f"\n🎯 选择最佳视频URL...")
                        
                        # 收集所有高质量的视频链接
                        priority_links = []
                        priority_links.extend(candidates['high_confidence'])
                        if keywords:
                            priority_links.extend(candidates['keyword_matches'])
                        priority_links.extend(candidates['medium_confidence'])
                        
                        # 去重
                        priority_links = list(dict.fromkeys(priority_links))
                        
                        if priority_links:
                            print(f"   找到 {len(priority_links)} 个优质视频URL")
                            video_links.extend(priority_links[:args.max_downloads])
                        
                        # 提取流媒体URL
                        streams = capture.extract_stream_urls(video_requests)
                        
                        print(f"\n📊 流媒体分析:")
                        print(f"   HLS流: {len(streams['hls'])} 个")
                        print(f"   DASH流: {len(streams['dash'])} 个")
                        print(f"   直接视频: {len(streams['direct'])} 个")
                        print(f"   视频片段: {len(streams['segments'])} 个")
                        
                        # 处理HLS流
                        if streams['hls'] and not video_links:
                            print(f"\n🎬 发现HLS流，开始下载...")
                            stream_downloader = StreamDownloader(output_dir=args.output, logger=logger)
                            output_file = stream_downloader.download_hls(streams['hls'][0], "hls_video.mp4")
                            if output_file:
                                print(f"✅ HLS流下载完成: {output_file}")
                        
                        # 如果还没有找到视频链接，使用直接链接
                        if not video_links and streams['direct']:
                            video_links.extend(streams['direct'])
                        
                        # 检测分离的音视频流
                        if strategy.get('use_merge', False):
                            separate_result = detector.detect_separate_streams(video_requests)
                            
                            if separate_result['has_separate']:
                                print(f"\n🎵 检测到分离的音视频流")
                                print(f"   视频流: {len(separate_result['video_urls'])} 个")
                                print(f"   音频流: {len(separate_result['audio_urls'])} 个")
                                
                                # 检查FFmpeg
                                merger = MediaMerger(logger=logger)
                                if merger.is_available():
                                    print(f"\n🔧 开始下载并合并音视频...")
                                    stream_downloader = StreamDownloader(output_dir=args.output, logger=logger)
                                    
                                    # 选择最佳质量的视频和音频
                                    video_url = separate_result['video_urls'][0]
                                    audio_url = separate_result['audio_urls'][0]
                                    
                                    output_file = stream_downloader.download_separate_streams(
                                        video_url, audio_url, "merged_video.mp4", merger
                                    )
                                    
                                    if output_file:
                                        print(f"✅ 音视频合并完成: {output_file}")
                                    else:
                                        print("❌ 音视频合并失败")
                                else:
                                    print("⚠️  未找到FFmpeg，无法合并音视频")
                                    print("   提示: 安装FFmpeg以启用音视频合并功能")
                    else:
                        print("⚠️  未找到视频相关请求，尝试HTML解析...")
                        strategy['method'] = 'html_parse'
                else:
                    print("⚠️  未捕获到网络请求，尝试HTML解析...")
                    strategy['method'] = 'html_parse'
        
        # 策略4: HTML解析（默认/回退）
        if strategy['method'] == 'html_parse':
            print("📝 HTML解析模式")
            print("-" * 70)
            
            if not html_content:
                html_content = get_html_content(args.url, args.proxy, logger)
            
            if html_content:
                parser = VideoParser(logger=logger)
                video_links = parser.parse(html_content, args.url)
            else:
                print("❌ 无法获取网页内容")
                logger.error("无法获取网页内容，程序退出")
                sys.exit(1)
        
        # 下载视频链接
        if video_links:
            print(f"\n📹 共找到 {len(video_links)} 个视频文件")
            
            # 显示视频链接列表
            print("\n视频链接列表:")
            for i, link in enumerate(video_links[:args.max_downloads], 1):
                print(f"  {i}. {link}")
            
            # 限制下载数量
            if len(video_links) > args.max_downloads:
                print(f"\n将下载前 {args.max_downloads} 个视频文件")
                video_links = video_links[:args.max_downloads]
            
            # 创建下载器（使用捕获的Cookie和Referer）
            downloader = VideoDownloader(
                output_dir=args.output,
                workers=args.workers,
                retries=args.retries,
                proxy=args.proxy,
                resume=args.resume,
                verify=not args.no_verify,
                logger=logger,
                cookies=captured_cookies,
                referer=captured_referer
            )
            
            # 开始下载
            print(f"\n⬇️  开始下载视频文件...")
            print()
            
            results = downloader.download_videos(video_links)
            
            # 显示下载结果
            print("\n" + "=" * 70)
            print("✅ 下载完成！")
            print("=" * 70)
            print(f"成功: {results['success']} 个")
            print(f"失败: {results['failed']} 个")
            print(f"跳过: {results['skipped']} 个")
            print(f"总计: {len(video_links)} 个")
            print("=" * 70)
            
            logger.info(f"下载完成 - 成功: {results['success']}, 失败: {results['failed']}, 跳过: {results['skipped']}")
            
            # 处理加密视频文件
            if results['success'] > 0:
                print(f"\n🔓 检查并处理加密视频...")
                crypto_handler = EncryptedVideoHandler(logger=logger)
                processed = crypto_handler.batch_process_directory(args.output)
                
                if processed:
                    print(f"✅ 成功解密 {len(processed)} 个加密视频")
                    for file in processed:
                        print(f"   - {os.path.basename(file)}")
        else:
            print("\n⚠️  未找到可下载的视频")
        
        logger.info("程序结束")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断下载")
        logger.warning("用户中断下载")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        logger.error(f"程序异常: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
