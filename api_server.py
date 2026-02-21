"""Flask API服务器 - 提供RESTful API接口"""

try:
    from flask import Flask, request, jsonify, send_file, send_from_directory
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import threading
from pathlib import Path

from utils import (
    setup_logger,
    ResourceDownloader,
    ResourceDetector,
    DatabaseManager,
    TaskManager,
    TaskStatus
)


class APIServer:
    """API服务器"""
    
    def __init__(self, host='0.0.0.0', port=5000, debug=False):
        """
        初始化API服务器
        
        Args:
            host: 主机地址
            port: 端口号
            debug: 调试模式
        """
        self.app = Flask(__name__, static_folder='web/static', template_folder='web/templates')
        CORS(self.app)  # 启用CORS
        
        self.host = host
        self.port = port
        self.debug = debug
        
        # 初始化组件
        self.logger = setup_logger()
        self.db = DatabaseManager(logger=self.logger)
        self.task_manager = TaskManager(max_workers=5, logger=self.logger)
        self.resource_detector = ResourceDetector(logger=self.logger)
        self.resource_downloader = ResourceDownloader(logger=self.logger)
        
        # 设置任务回调
        self.task_manager.on_task_complete = self._on_task_complete
        self.task_manager.on_task_failed = self._on_task_failed
        
        # 启动任务管理器
        self.task_manager.start(self._download_task)
        
        # 注册路由
        self._register_routes()
    
    def _register_routes(self):
        """注册API路由"""
        
        # 首页
        @self.app.route('/')
        def index():
            return send_file('web/index.html')
        
        # ===== 资源检测 =====
        @self.app.route('/api/detect', methods=['POST'])
        def detect_resources():
            """检测页面资源"""
            data = request.json
            url = data.get('url')
            
            if not url:
                return jsonify({'error': '缺少URL参数'}), 400
            
            try:
                resources = self.resource_detector.detect_all_resources(url)
                stats = self.resource_detector.get_resource_statistics(resources)
                
                return jsonify({
                    'success': True,
                    'resources': resources,
                    'statistics': stats
                })
            
            except Exception as e:
                self.logger.error(f"资源检测失败: {e}")
                return jsonify({'error': str(e)}), 500
        
        # ===== 任务管理 =====
        @self.app.route('/api/tasks', methods=['POST'])
        def create_task():
            """创建下载任务"""
            data = request.json
            url = data.get('url')
            resource_type = data.get('resource_type', 'unknown')
            output_path = data.get('output_path', '')
            
            if not url:
                return jsonify({'error': '缺少URL参数'}), 400
            
            try:
                task_id = self.task_manager.add_task(url, resource_type, output_path)
                
                # 记录到数据库
                self.db.add_download_record(task_id, url, resource_type, output_path)
                
                return jsonify({
                    'success': True,
                    'task_id': task_id
                })
            
            except Exception as e:
                self.logger.error(f"创建任务失败: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/batch', methods=['POST'])
        def create_batch_tasks():
            """批量创建任务"""
            data = request.json
            urls = data.get('urls', [])
            resource_type = data.get('resource_type', 'unknown')
            
            if not urls:
                return jsonify({'error': '缺少URLs参数'}), 400
            
            try:
                task_ids = self.task_manager.add_batch_tasks(urls, resource_type)
                
                # 记录到数据库
                for task_id, url in zip(task_ids, urls):
                    self.db.add_download_record(task_id, url, resource_type)
                
                return jsonify({
                    'success': True,
                    'task_ids': task_ids,
                    'count': len(task_ids)
                })
            
            except Exception as e:
                self.logger.error(f"批量创建任务失败: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks', methods=['GET'])
        def get_tasks():
            """获取所有任务"""
            try:
                tasks = self.task_manager.get_all_tasks()
                return jsonify({
                    'success': True,
                    'tasks': [task.to_dict() for task in tasks]
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/<task_id>', methods=['GET'])
        def get_task(task_id):
            """获取单个任务"""
            try:
                task = self.task_manager.get_task(task_id)
                if task:
                    return jsonify({
                        'success': True,
                        'task': task.to_dict()
                    })
                else:
                    return jsonify({'error': '任务不存在'}), 404
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/<task_id>/pause', methods=['POST'])
        def pause_task(task_id):
            """暂停任务"""
            try:
                self.task_manager.pause_task(task_id)
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/<task_id>/resume', methods=['POST'])
        def resume_task(task_id):
            """恢复任务"""
            try:
                self.task_manager.resume_task(task_id)
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/<task_id>/cancel', methods=['POST'])
        def cancel_task(task_id):
            """取消任务"""
            try:
                self.task_manager.cancel_task(task_id)
                self.db.update_download_status(task_id, 'cancelled')
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/<task_id>/retry', methods=['POST'])
        def retry_task(task_id):
            """重试任务"""
            try:
                self.task_manager.retry_task(task_id)
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tasks/statistics', methods=['GET'])
        def get_task_statistics():
            """获取任务统计"""
            try:
                stats = self.task_manager.get_statistics()
                return jsonify({
                    'success': True,
                    'statistics': stats
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # ===== 下载历史 =====
        @self.app.route('/api/history', methods=['GET'])
        def get_history():
            """获取下载历史"""
            try:
                limit = int(request.args.get('limit', 100))
                offset = int(request.args.get('offset', 0))
                status = request.args.get('status')
                resource_type = request.args.get('resource_type')
                
                records = self.db.get_download_history(limit, offset, status, resource_type)
                
                return jsonify({
                    'success': True,
                    'records': records,
                    'count': len(records)
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/history/search', methods=['GET'])
        def search_history():
            """搜索下载历史"""
            try:
                keyword = request.args.get('keyword', '')
                limit = int(request.args.get('limit', 50))
                
                records = self.db.search_downloads(keyword, limit)
                
                return jsonify({
                    'success': True,
                    'records': records,
                    'count': len(records)
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/statistics', methods=['GET'])
        def get_statistics():
            """获取统计信息"""
            try:
                stats = self.db.get_statistics()
                return jsonify({
                    'success': True,
                    'statistics': stats
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # ===== 文件管理 =====
        @self.app.route('/api/files/<path:filename>', methods=['GET'])
        def download_file(filename):
            """下载文件"""
            try:
                downloads_dir = 'downloads'
                return send_from_directory(downloads_dir, filename, as_attachment=True)
            except Exception as e:
                return jsonify({'error': str(e)}), 404
        
        # ===== 系统信息 =====
        @self.app.route('/api/info', methods=['GET'])
        def get_info():
            """获取系统信息"""
            return jsonify({
                'success': True,
                'info': {
                    'version': '4.0',
                    'name': '视频爬虫工具',
                    'features': [
                        '智能资源检测',
                        '多类型资源下载',
                        '任务队列管理',
                        '下载历史记录',
                        'RESTful API'
                    ]
                }
            })
    
    def _download_task(self, task_id, url, output_path, progress_callback):
        """执行下载任务"""
        try:
            # 更新数据库状态
            self.db.update_download_status(task_id, 'running')
            
            # 执行下载
            result = self.resource_downloader.download_resource(
                url, 
                output_path,
                progress_callback
            )
            
            if result:
                # 获取文件大小
                file_size = os.path.getsize(result) if os.path.exists(result) else 0
                self.db.update_download_status(task_id, 'completed', file_size=file_size)
                return True
            else:
                self.db.update_download_status(task_id, 'failed', error_message='下载失败')
                return False
        
        except Exception as e:
            self.db.update_download_status(task_id, 'failed', error_message=str(e))
            return False
    
    def _on_task_complete(self, task):
        """任务完成回调"""
        self.logger.info(f"任务完成: {task.id}")
    
    def _on_task_failed(self, task):
        """任务失败回调"""
        self.logger.error(f"任务失败: {task.id} - {task.error_message}")
    
    def run(self):
        """启动服务器"""
        self.logger.info(f"API服务器启动: http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=self.debug, threaded=True)
    
    def stop(self):
        """停止服务器"""
        self.task_manager.stop()
        self.logger.info("API服务器已停止")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='视频爬虫工具 - API服务器')
    parser.add_argument('--host', default='0.0.0.0', help='主机地址')
    parser.add_argument('--port', type=int, default=5000, help='端口号')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    server = APIServer(host=args.host, port=args.port, debug=args.debug)
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
        server.stop()


if __name__ == '__main__':
    main()
