"""视频爬虫工具 - GUI界面"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import queue
import os
import sys
from pathlib import Path

# 导入核心模块
from utils import (
    setup_logger,
    VideoParser,
    VideoDownloader,
    NetworkCapture,
    StreamDownloader,
    MediaMerger,
    SmartDetector,
    EncryptedVideoHandler,
    ConfigManager
)
from utils.version import VersionManager


class VideoDownloaderGUI:
    """视频下载器GUI主窗口"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("视频爬虫工具 v4.0")
        self.root.geometry("900x950")
        self.root.resizable(True, True)
        
        # 配置管理器
        self.config = ConfigManager()
        
        # 版本管理器
        self.version_manager = VersionManager()
        
        # 消息队列（用于线程间通信）
        self.log_queue = queue.Queue()
        
        # 下载状态
        self.is_downloading = False
        self.download_thread = None
        
        # 创建界面
        self.create_widgets()
        
        # 启动日志更新
        self.update_log()
        
        # 加载配置
        self.load_config()
    
    def create_widgets(self):
        """创建界面组件"""
        
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # ===== URL输入区域 =====
        url_frame = ttk.LabelFrame(main_frame, text="视频URL", padding="10")
        url_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=("Arial", 10))
        url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        paste_btn = ttk.Button(url_frame, text="粘贴", command=self.paste_url, width=8)
        paste_btn.grid(row=0, column=1)
        
        # ===== 基本设置 =====
        basic_frame = ttk.LabelFrame(main_frame, text="基本设置", padding="10")
        basic_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        basic_frame.columnconfigure(1, weight=1)
        
        # 保存目录
        ttk.Label(basic_frame, text="保存目录:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar(value="downloads")
        output_entry = ttk.Entry(basic_frame, textvariable=self.output_var)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(basic_frame, text="浏览", command=self.browse_output, width=8).grid(row=0, column=2)
        
        # 最大下载数
        ttk.Label(basic_frame, text="最大下载数:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_downloads_var = tk.StringVar(value="10")
        ttk.Entry(basic_frame, textvariable=self.max_downloads_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 并发线程数
        ttk.Label(basic_frame, text="并发线程:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.workers_var = tk.StringVar(value="3")
        ttk.Entry(basic_frame, textvariable=self.workers_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # 关键词
        ttk.Label(basic_frame, text="搜索关键词:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.keywords_var = tk.StringVar(value="")
        ttk.Entry(basic_frame, textvariable=self.keywords_var).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(basic_frame, text="(逗号分隔)", font=("Arial", 8)).grid(row=3, column=2, sticky=tk.W)
        
        # ===== 高级选项 =====
        advanced_frame = ttk.LabelFrame(main_frame, text="高级选项", padding="10")
        advanced_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 选项复选框
        self.force_capture_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(advanced_frame, text="强制使用抓包模式", variable=self.force_capture_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.resume_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="启用断点续传", variable=self.resume_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.auto_merge_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="自动合并音视频", variable=self.auto_merge_var).grid(row=1, column=0, sticky=tk.W, padx=5)
        
        self.auto_decrypt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="自动解密视频", variable=self.auto_decrypt_var).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        self.headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="无头浏览器模式", variable=self.headless_var).grid(row=2, column=0, sticky=tk.W, padx=5)
        
        # 代理设置
        proxy_frame = ttk.Frame(advanced_frame)
        proxy_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.use_proxy_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(proxy_frame, text="使用代理:", variable=self.use_proxy_var).grid(row=0, column=0, sticky=tk.W)
        
        self.proxy_var = tk.StringVar(value="")
        ttk.Entry(proxy_frame, textvariable=self.proxy_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        proxy_frame.columnconfigure(1, weight=1)
        
        # ===== 控制按钮 =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="开始下载", command=self.start_download, width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="停止下载", command=self.stop_download, width=15, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="清空日志", command=self.clear_log, width=15).grid(row=0, column=2, padx=5)
        
        ttk.Button(button_frame, text="打开下载目录", command=self.open_output_dir, width=15).grid(row=0, column=3, padx=5)
        
        # ===== 进度条 =====
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(progress_frame, textvariable=self.status_var, font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # ===== 日志区域 =====
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="5")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置日志颜色标签
        self.log_text.tag_config("INFO", foreground="black")
        self.log_text.tag_config("SUCCESS", foreground="green")
        self.log_text.tag_config("WARNING", foreground="orange")
        self.log_text.tag_config("ERROR", foreground="red")
        
        # ===== 底部信息栏 =====
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=6, column=0, sticky=(tk.W, tk.E))
        
        current_version = self.version_manager.get_current_version()
        ttk.Label(info_frame, text=f"视频爬虫工具 v{current_version} | 支持智能检测、网络抓包、加密解密",
                 font=("Arial", 8), foreground="gray").grid(row=0, column=0, sticky=tk.W)
        
        # 检查更新按钮
        ttk.Button(info_frame, text="检查更新", command=self.check_for_updates, width=10).grid(row=0, column=1, sticky=tk.E, padx=5)
        info_frame.columnconfigure(0, weight=1)
    
    def load_config(self):
        """从配置文件加载设置"""
        try:
            self.output_var.set(self.config.get('download', 'output_dir', 'downloads'))
            self.max_downloads_var.set(str(self.config.getint('download', 'max_downloads', 10)))
            self.workers_var.set(str(self.config.getint('download', 'workers', 3)))
            self.keywords_var.set(self.config.get('capture', 'keywords', ''))
            self.headless_var.set(self.config.getboolean('capture', 'headless', True))
            
            if self.config.getboolean('proxy', 'enabled', False):
                self.use_proxy_var.set(True)
                proxy = self.config.get('proxy', 'http_proxy', '')
                self.proxy_var.set(proxy)
            
            self.log_message("已加载配置文件", "SUCCESS")
        except Exception as e:
            self.log_message(f"加载配置失败: {e}", "WARNING")
    
    def paste_url(self):
        """粘贴URL"""
        try:
            url = self.root.clipboard_get()
            self.url_var.set(url)
            self.log_message("已粘贴URL", "INFO")
        except:
            messagebox.showwarning("警告", "剪贴板为空或无法访问")
    
    def browse_output(self):
        """浏览选择输出目录"""
        directory = filedialog.askdirectory(initialdir=self.output_var.get())
        if directory:
            self.output_var.set(directory)
    
    def open_output_dir(self):
        """打开下载目录"""
        output_dir = self.output_var.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 跨平台打开文件夹
        if sys.platform == 'win32':
            os.startfile(output_dir)
        elif sys.platform == 'darwin':
            os.system(f'open "{output_dir}"')
        else:
            os.system(f'xdg-open "{output_dir}"')
    
    def log_message(self, message, level="INFO"):
        """添加日志消息到队列"""
        self.log_queue.put((message, level))
    
    def update_log(self):
        """更新日志显示"""
        try:
            while True:
                message, level = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, f"[{level}] {message}\n", level)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # 每100ms检查一次
        self.root.after(100, self.update_log)
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("日志已清空", "INFO")
    
    def update_status(self, status, progress=None):
        """更新状态和进度"""
        self.status_var.set(status)
        if progress is not None:
            self.progress_var.set(progress)
    
    def start_download(self):
        """开始下载"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入视频URL")
            return
        
        if self.is_downloading:
            messagebox.showwarning("警告", "正在下载中，请等待完成")
            return
        
        # 验证参数
        try:
            max_downloads = int(self.max_downloads_var.get())
            workers = int(self.workers_var.get())
            if max_downloads <= 0 or workers <= 0:
                raise ValueError()
        except:
            messagebox.showerror("错误", "最大下载数和并发线程数必须是正整数")
            return
        
        # 更新UI状态
        self.is_downloading = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        
        # 启动下载线程
        self.download_thread = threading.Thread(target=self.download_worker, args=(url,), daemon=True)
        self.download_thread.start()
    
    def stop_download(self):
        """停止下载"""
        if self.is_downloading:
            self.is_downloading = False
            self.log_message("正在停止下载...", "WARNING")
            self.update_status("正在停止...")
    
    def download_worker(self, url):
        """下载工作线程"""
        try:
            self.log_message("="*50, "INFO")
            self.log_message(f"开始处理: {url}", "INFO")
            self.update_status("正在分析URL...", 0)
            
            # 获取参数
            output_dir = self.output_var.get()
            max_downloads = int(self.max_downloads_var.get())
            workers = int(self.workers_var.get())
            keywords = [k.strip() for k in self.keywords_var.get().split(',') if k.strip()]
            proxy = self.proxy_var.get() if self.use_proxy_var.get() else None
            
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 设置日志
            logger = setup_logger(log_dir='logs')
            
            # 智能检测
            self.log_message("正在智能检测URL类型...", "INFO")
            detector = SmartDetector(logger=logger)
            url_type = detector.detect_url_type(url)
            self.log_message(f"检测到URL类型: {url_type}", "SUCCESS")
            
            strategy = detector.recommend_strategy(url)
            self.log_message(f"推荐策略: {strategy['method']}", "INFO")
            
            video_urls = []
            cookies = None
            referer = None
            
            # 根据策略下载
            if strategy['use_capture'] or self.force_capture_var.get():
                self.update_status("正在启动浏览器抓包...", 10)
                self.log_message("启动浏览器抓包模式", "INFO")
                
                capture = NetworkCapture(headless=self.headless_var.get(), logger=logger)
                try:
                    video_urls = capture.start_capture(url, wait_time=10)
                    cookies = capture.get_cookies()
                    referer = capture.get_referer()
                    
                    if keywords:
                        self.log_message(f"使用关键词过滤: {', '.join(keywords)}", "INFO")
                        filtered = capture.filter_video_requests(keywords=keywords)
                        if filtered:
                            video_urls = [req['url'] for req in filtered[:max_downloads]]
                    
                    self.log_message(f"抓包完成，找到 {len(video_urls)} 个视频", "SUCCESS")
                except Exception as e:
                    self.log_message(f"抓包失败: {e}", "ERROR")
            
            # 如果没有找到视频，尝试HTML解析
            if not video_urls:
                self.update_status("正在解析HTML...", 20)
                self.log_message("尝试HTML解析模式", "INFO")
                
                parser = VideoParser(logger=logger)
                video_urls = parser.parse(url, proxy=proxy)
                self.log_message(f"HTML解析完成，找到 {len(video_urls)} 个视频", "SUCCESS")
            
            if not video_urls:
                self.log_message("未找到任何视频链接", "ERROR")
                self.update_status("未找到视频", 0)
                messagebox.showerror("错误", "未找到任何视频链接")
                return
            
            # 限制下载数量
            video_urls = video_urls[:max_downloads]
            self.log_message(f"准备下载 {len(video_urls)} 个视频", "INFO")
            
            # 下载视频
            self.update_status(f"正在下载 {len(video_urls)} 个视频...", 30)
            self.log_message(f"准备下载 {len(video_urls)} 个视频", "INFO")
            
            downloader = VideoDownloader(
                output_dir=output_dir,
                workers=workers,
                resume=self.resume_var.get(),
                proxy=proxy,
                logger=logger,
                cookies=cookies,
                referer=referer
            )
            
            try:
                downloaded_files = downloader.download_videos(video_urls)
                self.log_message(f"下载完成，成功 {len(downloaded_files)} 个文件", "SUCCESS")
            except Exception as e:
                self.log_message(f"下载过程出错: {e}", "ERROR")
                downloaded_files = []
            
            # 处理加密视频
            if self.auto_decrypt_var.get() and downloaded_files:
                self.update_status("正在处理加密视频...", 85)
                self.log_message("检查并解密加密视频...", "INFO")
                
                handler = EncryptedVideoHandler(logger=logger)
                decrypted = handler.process_directory(output_dir)
                if decrypted:
                    self.log_message(f"解密了 {len(decrypted)} 个加密视频", "SUCCESS")
            
            # 完成
            self.update_status(f"下载完成！共 {len(downloaded_files)} 个文件", 100)
            self.log_message("="*50, "INFO")
            self.log_message(f"全部完成！成功下载 {len(downloaded_files)} 个视频", "SUCCESS")
            self.log_message(f"保存位置: {os.path.abspath(output_dir)}", "INFO")
            
            messagebox.showinfo("完成", f"下载完成！\n成功: {len(downloaded_files)} 个视频\n保存位置: {os.path.abspath(output_dir)}")
            
        except Exception as e:
            self.log_message(f"发生错误: {e}", "ERROR")
            self.update_status("下载失败", 0)
            messagebox.showerror("错误", f"下载过程中发生错误:\n{e}")
        
        finally:
            # 恢复UI状态
            self.is_downloading = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def check_for_updates(self):
        """检查更新"""
        def check_worker():
            try:
                logger = setup_logger()
                result = self.version_manager.check_for_updates()
                
                if result.get('error'):
                    self.log_message(f"检查更新失败: {result['error']}", "WARNING")
                    return
                
                if result.get('has_update'):
                    latest_version = result['latest_version']
                    current_version = result['current_version']
                    release_notes = result['release_notes']
                    download_url = result['download_url']
                    
                    # 在主线程中显示对话框
                    self.root.after(0, lambda: self.show_update_dialog(
                        latest_version, current_version, release_notes, download_url
                    ))
                else:
                    self.log_message("当前已是最新版本", "SUCCESS")
            
            except Exception as e:
                self.log_message(f"检查更新时发生错误: {e}", "ERROR")
        
        # 在后台线程中检查更新
        threading.Thread(target=check_worker, daemon=True).start()
    
    def show_update_dialog(self, latest_version, current_version, release_notes, download_url):
        """显示更新对话框"""
        message = f"发现新版本！\n\n"
        message += f"当前版本: {current_version}\n"
        message += f"最新版本: {latest_version}\n\n"
        message += f"更新内容:\n{release_notes[:200]}...\n\n"
        message += "是否立即下载并更新？"
        
        if messagebox.askyesno("发现新版本", message):
            self.download_and_install_update(download_url)
    
    def download_and_install_update(self, download_url):
        """下载并安装更新"""
        def update_worker():
            try:
                self.log_message("正在下载更新...", "INFO")
                self.update_status("正在下载更新...", 0)
                
                logger = setup_logger()
                update_file = self.version_manager.download_update(download_url)
                
                if update_file:
                    self.log_message("更新下载完成", "SUCCESS")
                    
                    # 询问是否立即安装
                    self.root.after(0, lambda: self.confirm_install_update(update_file))
                else:
                    self.log_message("更新下载失败", "ERROR")
                    self.root.after(0, lambda: messagebox.showerror("错误", "更新下载失败"))
            
            except Exception as e:
                self.log_message(f"下载更新失败: {e}", "ERROR")
                self.root.after(0, lambda: messagebox.showerror("错误", f"下载更新失败:\n{e}"))
        
        threading.Thread(target=update_worker, daemon=True).start()
    
    def confirm_install_update(self, update_file):
        """确认安装更新"""
        if messagebox.askyesno("安装更新", "更新已下载完成，是否立即安装？\n程序将会重启。"):
            try:
                self.version_manager.install_update(update_file)
            except Exception as e:
                messagebox.showerror("错误", f"安装更新失败:\n{e}")


def main():
    """主函数"""
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    
    # 设置窗口图标（如果有的话）
    try:
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller打包后的路径
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            icon_path = 'icon.ico'
        
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    # 设置窗口关闭事件
    def on_closing():
        if app.is_downloading:
            if messagebox.askokcancel("退出", "正在下载中，确定要退出吗？"):
                app.is_downloading = False
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动主循环
    root.mainloop()


if __name__ == '__main__':
    main()
