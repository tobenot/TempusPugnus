# tempusPugnusHelper.py
import sys
import os
import json
import uuid
from datetime import datetime, timedelta
import logging

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QDialog, QDialogButtonBox, QLineEdit, QTextEdit, QHBoxLayout,
    QDateTimeEdit
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, QObject, QEvent
from PyQt6.QtGui import QIcon

class TimeFistGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.current_task = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.pressing = False
        self.start_point = None
        self.init_ui()
        # 初始化时隐藏倒计时标签
        self.countdown_label.hide()

    def init_ui(self):
        # 设置无边框窗口
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 允许窗口透明
        
        self.setGeometry(100, 100, 380, 220)  # 增加宽度到380
        self.setMinimumSize(380, 220)

        # 更新主窗口样式
        self.setStyleSheet("""
            /* 主窗口背景 */
            QWidget#centralWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1a1a2e, stop:1 #16213e);
                border: 2px solid #DAA520;
                border-radius: 10px;
            }
            
            /* 标签样式 */
            QLabel {
                color: #FFD700;
                font-size: 14px;
                padding: 5px;
                font-weight: bold;
                background: transparent;
            }
            
            /* 按钮基础样式 */
            QPushButton {
                background-color: rgba(44, 62, 80, 180);
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: rgba(52, 73, 94, 180);
                border: 1px solid #FFD700;
            }
            QPushButton:pressed {
                background-color: rgba(44, 62, 80, 220);
            }
            QPushButton:disabled {
                background-color: rgba(44, 62, 80, 100);
                color: #808080;
                border: 1px solid #808080;
            }
        """)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")  # 设置对象名以应用样式
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # 顶部标题区域
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(5, 0, 5, 0)
        
        title_label = QLabel("⚛️ Tempus Pugnus")
        title_label.setStyleSheet("""
            font-size: 14px;
            color: #FFD700;
            font-weight: bold;
            padding: 0;
        """)
        
        # 添加关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)  # 增大尺寸
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #DAA520;
                font-size: 20px;  # 增大字号
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                color: #FFD700;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_container)

        # 任务显示区域
        self.task_label = QLabel("🎯 无任务")
        self.task_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2ECC71;
                background: rgba(26, 26, 46, 180);
                border: 1px solid #DAA520;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.task_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 创建倒计时标签
        self.countdown_label = QLabel("")
        self.countdown_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #E74C3C;
                font-weight: bold;
                background: rgba(26, 26, 46, 180);
                border: 1px solid #DAA520;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.countdown_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # 底部 - 控制区
        button_container = QWidget()
        button_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(2)  # 减小按钮间距
        button_layout.setContentsMargins(0, 5, 0, 5)  # 调整边距

        # 更新按钮基础样式和布局
        button_base_style = """
            QPushButton {
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 3px 5px;  /* 减小内边距 */
                font-size: 12px;   /* 稍微减小字号 */
                font-weight: bold;
                min-width: 60px;   /* 减小最小宽度 */
                max-width: 60px;   /* 减小最大宽度 */
            }
            QPushButton:hover {
                border: 1px solid #FFD700;
            }
            QPushButton:disabled {
                color: #808080;
                border: 1px solid #808080;
                background-color: rgba(44, 62, 80, 100);
            }
        """

        # 创建按钮并设置固定宽度
        self.new_task_btn = QPushButton("✨新建")
        self.complete_task_btn = QPushButton("✅完成")
        self.adjust_time_btn = QPushButton("⏰重设")
        self.history_btn = QPushButton("📜记录")

        # 设置每个按钮的固定宽度
        for btn in [self.new_task_btn, self.complete_task_btn, 
                    self.adjust_time_btn, self.history_btn]:
            btn.setFixedWidth(60)  # 减小固定宽度

        # 设置按钮特定样式
        self.new_task_btn.setStyleSheet(button_base_style + """
            QPushButton {
                background-color: rgba(46, 204, 113, 160);
            }
            QPushButton:hover {
                background-color: rgba(46, 204, 113, 200);
            }
        """)

        self.complete_task_btn.setStyleSheet(button_base_style + """
            QPushButton {
                background-color: rgba(52, 152, 219, 160);
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 200);
            }
        """)

        self.adjust_time_btn.setStyleSheet(button_base_style + """
            QPushButton {
                background-color: rgba(241, 196, 15, 160);
            }
            QPushButton:hover {
                background-color: rgba(241, 196, 15, 200);
            }
        """)

        self.history_btn.setStyleSheet(button_base_style + """
            QPushButton {
                background-color: rgba(155, 89, 182, 160);
            }
            QPushButton:hover {
                background-color: rgba(155, 89, 182, 200);
            }
        """)

        # 设置按钮初始状态
        self.complete_task_btn.setEnabled(False)
        self.adjust_time_btn.setEnabled(False)

        # 调整按钮布局的间距
        button_layout.setSpacing(1)  # 减小按钮间距
        button_layout.setContentsMargins(2, 5, 2, 5)  # 减小边距

        # 使用更小的固定间距
        button_layout.addSpacing(2)  # 左边距
        button_layout.addWidget(self.new_task_btn)
        button_layout.addSpacing(1)  # 按钮间距
        button_layout.addWidget(self.complete_task_btn)
        button_layout.addSpacing(1)  # 按钮间距
        button_layout.addWidget(self.adjust_time_btn)
        button_layout.addSpacing(1)  # 按钮间距
        button_layout.addWidget(self.history_btn)
        button_layout.addSpacing(2)  # 右边距

        layout.addWidget(button_container)

        # 连接信号
        self.new_task_btn.clicked.connect(self.create_new_task)
        self.complete_task_btn.clicked.connect(self.complete_task)
        self.adjust_time_btn.clicked.connect(self.adjust_task_time)
        self.history_btn.clicked.connect(self.view_history)

        # 设置托盘图标（如果需要的话）
        # self.tray_icon = QSystemTrayIcon(QIcon('icon.png'), self)
        # self.tray_icon.show()

    def create_new_task(self):
        if self.current_task:
            QMessageBox.warning(self, "提示", "请先完成当前任务！")
            return

        dialog = TaskDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_description = dialog.task_description
            deadline_str = dialog.deadline_str
            
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
                self.current_task = self.task_manager.create_task(task_description, deadline)
                # 显示倒计时标签
                self.countdown_label.show()
                self.task_label.setText(f"🎯 {self.current_task['task']}")
                self.update_countdown()
                self.timer.start(1000)
                self.complete_task_btn.setEnabled(True)
                self.adjust_time_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建任务失败: {str(e)}")

    def update_countdown(self):
        if self.current_task:
            now = datetime.now()
            deadline = datetime.strptime(self.current_task['current_deadline'], "%Y-%m-%d %H:%M:%S")
            remaining = deadline - now
            if remaining.total_seconds() > 0:
                self.countdown_label.setText(str(remaining).split('.')[0])
            else:
                self.countdown_label.setText("时间到！")
                self.timer.stop()
                self.handle_timeout()

    def handle_timeout(self):
        response = QMessageBox.question(self, "任务超时", "任务已经超时，是否调整时限？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            self.adjust_task_time()
        else:
            self.task_manager.update_task_status(self.current_task['id'], "已超时")
            self.reset_task_ui()
            QMessageBox.information(self, "提示", "任务已标记为超时")

    def adjust_task_time(self):
        dialog = AdjustTimeDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取当前日期和选择的时间
            selected_datetime = dialog.new_deadline_input.dateTime()
            reason = dialog.reason_input.toPlainText().strip()
            
            if reason:
                try:
                    # 直接使用 QDateTime 对象，不需要格式转换
                    new_deadline = selected_datetime.toPython()  # 转换为 Python datetime 对象
                    self.task_manager.adjust_task(self.current_task['id'], new_deadline, reason)
                    self.current_task = self.task_manager.get_task_by_id(self.current_task['id'])
                    self.update_countdown()
                    self.timer.start(1000)
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"调整时间失败: {str(e)}")
            else:
                QMessageBox.warning(self, "提示", "请输入调整原因")

    def complete_task(self):
        dialog = CompleteTaskDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            summary = dialog.summary_input.toPlainText().strip()
            self.task_manager.complete_task(self.current_task['id'], summary)
            self.reset_task_ui()
            QMessageBox.information(self, "恭喜", "任务已完成！")

    def reset_task_ui(self):
        self.current_task = None
        self.task_label.setText("🎯 当前没有进行中的任务")
        # 只隐藏倒计时标签
        self.countdown_label.hide()
        self.timer.stop()
        self.complete_task_btn.setEnabled(False)
        self.adjust_time_btn.setEnabled(False)

    def view_history(self):
        history_text = self.task_manager.get_history_text()
        QMessageBox.information(self, "历史记录", history_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.start_point:
                movement = event.pos() - self.start_point
                self.move(self.pos() + movement)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = False
            self.start_point = None

class BaseDialog(QDialog):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        # 设置无边框和透明背景
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建背景容器
        self.container = QWidget(self)
        self.container.setObjectName("dialogContainer")
        
        # 基础样式
        self.setStyleSheet("""
            #dialogContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1a1a2e, stop:1 #16213e);
                border: 2px solid #DAA520;
                border-radius: 10px;
            }
            QLabel {
                color: #FFD700;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
            }
            QLineEdit, QTextEdit {
                background-color: rgba(44, 62, 80, 180);
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
            QPushButton {
                background-color: rgba(44, 62, 80, 180);
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: rgba(44, 62, 80, 220);
                border: 1px solid #FFD700;
            }
            QPushButton:pressed {
                background-color: rgba(44, 62, 80, 255);
            }
            QDialogButtonBox {
                background: transparent;
            }
        """)
        
        # 设置容器布局
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.container)
        
        # 主布局
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加标题栏
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 10)
        title_layout.setSpacing(10)  # 增加标题和关闭按钮之间的间距
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #FFD700; font-weight: bold;")
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(44, 62, 80, 180);
                color: #DAA520;
                font-size: 20px;
                font-weight: bold;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 0;
                margin: 0;
            }
            QPushButton:hover {
                background-color: rgba(44, 62, 80, 220);
                color: #FFD700;
                border: 1px solid #FFD700;
            }
            QPushButton:pressed {
                background-color: rgba(44, 62, 80, 255);
            }
        """)
        close_btn.clicked.connect(self.reject)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        
        self.layout.addWidget(title_container)
        
        # 拖动相关
        self.pressing = False
        self.start_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.start_point:
                movement = event.pos() - self.start_point
                self.move(self.pos() + movement)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = False
            self.start_point = None

class TaskDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("✨ 新建任务", parent)
        
        # 其他控件
        task_label = QLabel("📝 任务描述:")
        self.task_input = QTextEdit()
        self.task_input.setMaximumHeight(80)

        deadline_label = QLabel("⏰ 截止时间:")
        self.deadline_input = QDateTimeEdit()
        
        # 设置默认时间为当前时间加15分钟
        current = QDateTime.currentDateTime()
        default_time = current.addSecs(15 * 60)
        self.deadline_input.setDateTime(default_time)
        
        # 只显示时和分
        self.deadline_input.setDisplayFormat("HH   :   mm")
        self.deadline_input.setButtonSymbols(QDateTimeEdit.ButtonSymbols.NoButtons)

        # 设置时间范围
        self.deadline_input.setMinimumDateTime(current)
        self.deadline_input.setMaximumDateTime(current.addDays(2))

        # 更新时间编辑器的样式
        self.deadline_input.setStyleSheet("""
            QDateTimeEdit {
                background-color: rgba(44, 62, 80, 180);
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 16px;  /* 增大字号 */
                font-weight: bold;
                min-width: 120px;
            }
            /* 选中时的样式 */
            QDateTimeEdit:focus {
                border: 1px solid #FFD700;
                background-color: rgba(44, 62, 80, 220);
            }
            /* 分隔符样式 */
            QDateTimeEdit::section {
                color: #DAA520;
                font-weight: bold;
            }
            /* 鼠标悬停时的样式 */
            QDateTimeEdit:hover {
                background-color: rgba(44, 62, 80, 200);
            }
        """)

        # 设置步进值
        self.deadline_input.setCurrentSectionIndex(0)  # 默认选中小时
        self.deadline_input.setDisplayFormat("HH   :   mm")  # 使用更宽的分隔符

        # 添加事件过滤器来处理鼠标滚轮事件
        class TimeEditEventFilter(QObject):
            def eventFilter(self, obj, event):
                if event.type() == QEvent.Type.Wheel:
                    section = obj.currentSectionIndex()
                    delta = event.angleDelta().y()
                    if section == 0:  # 小时部分
                        if delta > 0:
                            obj.setTime(obj.time().addSecs(3600))  # 增加1小时
                        else:
                            obj.setTime(obj.time().addSecs(-3600))  # 减少1小时
                    elif section == 1:  # 分钟部分
                        if delta > 0:
                            obj.setTime(obj.time().addSecs(300))  # 增加5分钟
                        else:
                            obj.setTime(obj.time().addSecs(-300))  # 减少5分钟
                    return True
                return False  # 修改这里，返回 False 让其他事件继续传递

        # 安装事件过滤器
        self.time_filter = TimeEditEventFilter(self)  # 修改这里，改为 self
        self.deadline_input.installEventFilter(self.time_filter)

        # 连接信号以在点击时自动选择相应部分
        def handle_section_clicked(original_event):
            pos = original_event.pos()
            if pos.x() < self.deadline_input.width() / 2:
                self.deadline_input.setCurrentSectionIndex(0)  # 选中小时
            else:
                self.deadline_input.setCurrentSectionIndex(1)  # 选中分钟
            # 调用原始的鼠标按下事件
            QDateTimeEdit.mousePressEvent(self.deadline_input, original_event)

        self.deadline_input.mousePressEvent = handle_section_clicked

        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        self.layout.addWidget(task_label)
        self.layout.addWidget(self.task_input)
        self.layout.addWidget(deadline_label)
        self.layout.addWidget(self.deadline_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    # 添加拖动功能
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'pressing') and self.pressing:
            if hasattr(self, 'start_point'):
                movement = event.pos() - self.start_point
                self.move(self.pos() + movement)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = False

    def accept(self):
        selected_time = self.deadline_input.dateTime()
        current_time = QDateTime.currentDateTime()
        
        # 如果选择的时间小于当前时间，说明是明天的这个时间点
        if selected_time.time() <= current_time.time():
            selected_time = selected_time.addDays(1)
        
        self.task_description = self.task_input.toPlainText().strip()
        self.deadline_str = selected_time.toString("yyyy-MM-dd HH:mm:ss")
        
        if not self.task_description:
            QMessageBox.warning(self, "提示", "请输入任务描述")
            return
            
        super().accept()

class AdjustTimeDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("⏰ 调整时限", parent)
        
        # 使用基类的布局
        reason_label = QLabel("💭 调整原因:")
        self.reason_input = QTextEdit()
        self.reason_input.setMaximumHeight(80)

        new_deadline_label = QLabel("📅 新的截止时间:")
        self.new_deadline_input = QDateTimeEdit()
        
        # 设置默认时间为当前时间加15分钟
        current = QDateTime.currentDateTime()
        default_time = current.addSecs(15 * 60)
        self.new_deadline_input.setDateTime(default_time)
        
        # 使用相同的时间选择器样式
        self.new_deadline_input.setDisplayFormat("HH   :   mm")
        self.new_deadline_input.setButtonSymbols(QDateTimeEdit.ButtonSymbols.NoButtons)
        self.new_deadline_input.setStyleSheet("""
            QDateTimeEdit {
                background-color: rgba(44, 62, 80, 180);
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QDateTimeEdit:focus {
                border: 1px solid #FFD700;
                background-color: rgba(44, 62, 80, 220);
            }
            QDateTimeEdit::section {
                color: #DAA520;
                font-weight: bold;
            }
            QDateTimeEdit:hover {
                background-color: rgba(44, 62, 80, 200);
            }
        """)

        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        self.layout.addWidget(reason_label)
        self.layout.addWidget(self.reason_input)
        self.layout.addWidget(new_deadline_label)
        self.layout.addWidget(self.new_deadline_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def accept(self):
        selected_time = self.new_deadline_input.dateTime()
        current_time = QDateTime.currentDateTime()
        
        if selected_time.time() <= current_time.time():
            selected_time = selected_time.addDays(1)
        
        self.reason = self.reason_input.toPlainText().strip()
        self.deadline_str = selected_time.toString("yyyy-MM-dd HH:mm:ss")
        
        if self.reason:
            super().accept()
        else:
            QMessageBox.warning(self, "提示", "请输入调整原因")

class CompleteTaskDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("✅ 完成任务", parent)
        
        summary_label = QLabel("📝 任务总结 (可选):")
        self.summary_input = QTextEdit()
        self.summary_input.setMaximumHeight(150)

        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        self.layout.addWidget(summary_label)
        self.layout.addWidget(self.summary_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def accept(self):
        # 移除总结必填的验证，直接接受对话框
        self.summary = self.summary_input.toPlainText().strip()
        super().accept()

class TaskManager:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.task_file = os.path.join(self.data_dir, "tasks.json")
        self.tasks = []

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.data_dir, 'task_manager.log')),
                logging.StreamHandler()
            ]
        )

        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.task_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

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
            "total_adjusted_time": 0  # 秒数
        }
        self.tasks.append(task)
        self.save_tasks()
        logging.info(f"创建新任务: {task_description}")
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

            # 计算调整的总时长
            original_dt = datetime.strptime(original_deadline, "%Y-%m-%d %H:%M:%S")
            new_dt = new_deadline
            adjusted_seconds = (new_dt - original_dt).total_seconds()
            task['total_adjusted_time'] += adjusted_seconds

            self.save_tasks()
            logging.info(f"调整任务 {task_id} 的截止时间, 原时间: {original_deadline}, 新时间: {task['current_deadline']}")
        else:
            logging.error(f"未找到任务 {task_id}")

    def complete_task(self, task_id, summary):
        task = self.get_task_by_id(task_id)
        if task:
            task['completion_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task['summary'] = summary
            task['status'] = "已完成"
            self.save_tasks()
            logging.info(f"任务 {task_id} 已完成")
        else:
            logging.error(f"未找到任务 {task_id}")

    def update_task_status(self, task_id, status):
        task = self.get_task_by_id(task_id)
        if task:
            task['status'] = status
            self.save_tasks()
            logging.info(f"任务 {task_id} 状态更新为 {status}")
        else:
            logging.error(f"未找到任务 {task_id}")

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

def main():
    app = QApplication(sys.argv)
    gui = TimeFistGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()