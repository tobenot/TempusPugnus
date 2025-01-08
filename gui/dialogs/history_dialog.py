from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QListWidget, QListWidgetItem, 
    QTextEdit
)
from PyQt6.QtCore import Qt
from .base_dialog import BaseDialog

class HistoryDialog(BaseDialog):
    def __init__(self, task_manager, parent=None):
        super().__init__("📜 历史记录", parent)
        self.task_manager = task_manager
        self._setup_ui()
        self._load_tasks()

    def _setup_ui(self):
        # 内容区域
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)
        
        # 左侧任务列表
        self.task_list = QListWidget()
        self.task_list.setFixedWidth(200)
        
        # 右侧详情区域
        self.detail_area = QTextEdit()
        self.detail_area.setReadOnly(True)
        self.detail_area.setFixedWidth(300)
        
        content_layout.addWidget(self.task_list)
        content_layout.addWidget(self.detail_area)
        
        # 确定按钮
        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        # 添加到主布局
        self.layout.addLayout(content_layout)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 连接信号
        self.task_list.itemClicked.connect(self._show_task_detail)

    def _load_tasks(self):
        tasks_by_date = self.task_manager.get_tasks_by_date()
        
        for date, tasks in tasks_by_date.items():
            # 添加日期标题
            date_item = QListWidgetItem(f"📅 {date}")
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.task_list.addItem(date_item)
            
            # 添加当天的任务
            for task in tasks:
                status_emoji = "✅" if task["status"] == "已完成" else "⏳"
                task_item = QListWidgetItem(f"{status_emoji} {task['task']}")
                task_item.setData(Qt.ItemDataRole.UserRole, task)
                self.task_list.addItem(task_item)

    def _show_task_detail(self, item):
        task = item.data(Qt.ItemDataRole.UserRole)
        if task:  # 确保不是日期项
            detail_text = self.task_manager.get_task_detail_text(task)
            self.detail_area.setText(detail_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'pressing') and self.pressing:
            self.move(self.pos() + event.pos() - self.start_point)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = False 