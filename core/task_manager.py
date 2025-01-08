import os
import json
import uuid
from datetime import datetime, timedelta
import logging
import sys

class TaskManager:
    def __init__(self):
        # 获取应用根目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            app_root = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            app_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 设置数据目录
        self.data_dir = os.path.join(app_root, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 设置日志
        log_file = os.path.join(self.data_dir, 'task_manager.log')
        self.setup_logger(log_file)
        
        # 设置任务文件
        self.task_file = os.path.join(self.data_dir, "tasks.json")
        self.tasks = []
        self.load_tasks()

    def setup_logger(self, log_file):
        # 创建logger
        logger = logging.getLogger('TaskManager')
        logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式器
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 设置格式器
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # 保存logger引用
        self.logger = logger

    def load_tasks(self):
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                self.logger.error(f"加载任务失败: {str(e)}")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        try:
            with open(self.task_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"保存任务失败: {str(e)}")

    def create_task(self, task_description, deadline):
        task = {
            "id": str(uuid.uuid4()),
            "task": task_description,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "initial_deadline": deadline.strftime("%Y-%m-%d %H:%M:%S"),
            "current_deadline": deadline.strftime("%Y-%m-%d %H:%M:%S"),
            "adjustments": [],
            "completion_time": "",
            "summary": "",
            "status": "进行中",
            "total_adjustments": 0,
            "total_adjusted_time": 0
        }
        self.tasks.append(task)
        self.save_tasks()
        self.logger.info(f'创建任务: "{task_description}"')
        return task

    def adjust_task(self, task_id, new_deadline, reason):
        task = self.get_task_by_id(task_id)
        if task:
            original_deadline = task['current_deadline']
            adjustment = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reason": reason,
                "original_deadline": task['current_deadline'],
                "new_deadline": new_deadline.strftime("%Y-%m-%d %H:%M:%S"),
                "adjustment_count": len(task['adjustments']) + 1
            }
            task['adjustments'].append(adjustment)
            task['current_deadline'] = new_deadline.strftime("%Y-%m-%d %H:%M:%S")
            task['total_adjustments'] = len(task['adjustments'])

            original_dt = datetime.strptime(original_deadline, "%Y-%m-%d %H:%M:%S")
            adjusted_seconds = (new_deadline - original_dt).total_seconds()
            task['total_adjusted_time'] += adjusted_seconds

            self.save_tasks()
            self.logger.info(
                f'调整任务 "{task["task"]}" 的截止时间\n'
                f'  原因: {reason}\n'
                f'  原时间: {original_deadline}\n'
                f'  新时间: {task["current_deadline"]}'
            )
        else:
            self.logger.error(f"未找到任务 {task_id}")

    def complete_task(self, task_id, summary):
        task = self.get_task_by_id(task_id)
        if task:
            task['completion_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task['summary'] = summary
            task['status'] = "已完成"
            self.save_tasks()
            completion_msg = f'完成任务: "{task["task"]}"'
            if summary:
                completion_msg += f'\n  总结: {summary}'
            self.logger.info(completion_msg)
        else:
            self.logger.error(f"未找到任务 {task_id}")

    def update_task_status(self, task_id, status):
        task = self.get_task_by_id(task_id)
        if task:
            task['status'] = status
            self.save_tasks()
            self.logger.info(f'任务 "{task["task"]}" 状态更新为: {status}')
        else:
            self.logger.error(f"未找到任务 {task_id}")

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def get_history_text(self):
        if not self.tasks:
            return "暂无历史记录。"
        history = ""
        for task in self.tasks:
            history += f"任务ID: {task['id']}\n"
            history += f"任务描述: {task['task']}\n"
            history += f"开始时间: {task['start_time']}\n"
            history += f"初始截止时间: {task['initial_deadline']}\n"
            history += f"当前截止时间: {task['current_deadline']}\n"
            history += f"状态: {task['status']}\n"
            if task['completion_time']:
                history += f"完成时间: {task['completion_time']}\n"
            if task['summary']:
                history += f"总结: {task['summary']}\n"
            history += f"总调整次数: {task['total_adjustments']}\n"
            history += f"总调整时长: {timedelta(seconds=int(task['total_adjusted_time']))}\n"
            history += "-" * 40 + "\n"
        return history 

    def get_tasks_by_date(self):
        # 按日期分组的任务字典
        tasks_by_date = {}
        
        for task in self.tasks:
            date = task['start_time'].split()[0]  # 获取日期部分
            if date not in tasks_by_date:
                tasks_by_date[date] = []
            tasks_by_date[date].append(task)
        
        # 按日期倒序排序
        return dict(sorted(tasks_by_date.items(), reverse=True))

    def get_task_detail_text(self, task):
        """获取单个任务的详细信息"""
        detail = f"📝 任务: {task['task']}\n"
        detail += f"⏰ 开始时间: {task['start_time']}\n"
        detail += f"📅 初始截止: {task['initial_deadline']}\n"
        
        if task['adjustments']:
            detail += "\n⚡ 调整记录:\n"
            for adj in task['adjustments']:
                detail += f"  • 时间: {adj['time']}\n"
                detail += f"    原因: {adj['reason']}\n"
                detail += f"    从 {adj['original_deadline']} 改到 {adj['new_deadline']}\n"
        
        if task['completion_time']:
            detail += f"\n✅ 完成时间: {task['completion_time']}\n"
        if task['summary']:
            detail += f"📌 总结: {task['summary']}\n"
        
        detail += f"\n📊 统计:\n"
        detail += f"  总调整次数: {task['total_adjustments']}\n"
        detail += f"  总调整时长: {timedelta(seconds=int(task['total_adjusted_time']))}\n"
        detail += f"  当前状态: {task['status']}"
        
        return detail 