from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QHBoxLayout, QDialog
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from datetime import datetime, timedelta

from TempusPugnus.gui.dialogs import TaskDialog, AdjustTimeDialog, CompleteTaskDialog, HistoryDialog, ReminderDialog, MessageDialog
from TempusPugnus.core.task_manager import TaskManager

class TimeFistGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.current_task = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.pressing = False
        self.start_point = None
        self.reminders = []  # 存储所有提醒
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(1000)  # 每秒检查一次
        self.init_ui()
        self.countdown_label.hide()

    def init_ui(self):
        # 设置无边框窗口
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setGeometry(100, 100, 380, 180)  # 减小窗口高度
        self.setMinimumSize(380, 180)

        # 创建中心部件和布局
        self._setup_central_widget()
        self._setup_title_bar()
        self._setup_task_area()
        self._setup_control_buttons()
        self._setup_styles()
        self._connect_signals()

    def _setup_central_widget(self):
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 5, 10, 5)  # 减小上下边距
        self.main_layout.setSpacing(5)  # 减小间距

    def _setup_title_bar(self):
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
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #DAA520;
                font-size: 20px;
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
        
        self.main_layout.addWidget(title_container)

    def _setup_task_area(self):
        # 创建任务信息容器
        task_container = QWidget()
        task_layout = QHBoxLayout(task_container)
        task_layout.setContentsMargins(0, 0, 0, 0)
        task_layout.setSpacing(5)

        # 任务标签
        self.task_label = QLabel("🎯 当前没有进行中的任务")
        self.task_label.setStyleSheet("""
            background-color: rgba(26, 26, 46, 180);
            color: #2ECC71;
            border: 1px solid #DAA520;
            border-radius: 5px;
            padding: 5px 8px;
            font-size: 16px;
            font-weight: bold;
        """)
        
        # 倒计时标签
        self.countdown_label = QLabel("")
        self.countdown_label.setStyleSheet("""
            background-color: rgba(26, 26, 46, 180);
            color: #E74C3C;
            border: 1px solid #DAA520;
            border-radius: 5px;
            padding: 5px 8px;
            font-size: 32px;
            font-weight: bold;
            min-width: 160px;
            text-align: center;
        """)
        
        # 添加到水平布局，1:1 比例
        task_layout.addWidget(self.task_label, stretch=1)
        task_layout.addWidget(self.countdown_label, stretch=1)
        
        # 添加到主布局
        self.main_layout.addWidget(task_container)

    def _setup_control_buttons(self):
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(1)
        button_layout.setContentsMargins(2, 0, 2, 2)

        self.new_task_btn = QPushButton("🌟新建")
        self.complete_task_btn = QPushButton("🏁完成")
        self.adjust_time_btn = QPushButton("🔄重设")
        self.history_btn = QPushButton("📜记录")
        self.reminder_btn = QPushButton("⏲️提醒")

        # 设置按钮样式
        button_style = """
            background-color: rgba(44, 62, 80, 180);
            color: #FFD700;
            border: 1px solid #DAA520;
            border-radius: 4px;
            padding: 3px 6px;
            font-size: 14px;
            font-weight: bold;
            min-width: 50px;
        """

        for btn in [self.new_task_btn, self.complete_task_btn, 
                   self.adjust_time_btn, self.history_btn, self.reminder_btn]:
            btn.setFixedWidth(50)
            btn.setStyleSheet(button_style)
            button_layout.addWidget(btn)

        self.complete_task_btn.setEnabled(False)
        self.adjust_time_btn.setEnabled(False)

        self.main_layout.addWidget(button_container)

    def _setup_styles(self):
        from .styles.default import MAIN_WINDOW_STYLE
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def _connect_signals(self):
        self.new_task_btn.clicked.connect(self.create_new_task)
        self.complete_task_btn.clicked.connect(self.complete_task)
        self.adjust_time_btn.clicked.connect(self.adjust_task_time)
        self.history_btn.clicked.connect(self.view_history)
        self.reminder_btn.clicked.connect(self.set_reminder)

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
        # 使用 QMessageBox.StandardButton 创建三个按钮选项
        adjust_btn = QMessageBox.StandardButton.Yes
        complete_btn = QMessageBox.StandardButton.Apply
        timeout_btn = QMessageBox.StandardButton.No

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("任务超时")
        msg_box.setText("任务已经超时，请选择操作：")
        msg_box.setStandardButtons(adjust_btn | complete_btn | timeout_btn)
        
        # 自定义按钮文本
        msg_box.button(adjust_btn).setText("调整时限")
        msg_box.button(complete_btn).setText("标记完成")
        msg_box.button(timeout_btn).setText("标记超时")

        response = msg_box.exec()

        if response == adjust_btn:
            self.adjust_task_time()
        elif response == complete_btn:
            self.complete_task()
        else:  # timeout_btn
            self.task_manager.update_task_status(self.current_task['id'], "已超时")
            self.reset_task_ui()
            QMessageBox.information(self, "提示", "任务已标记为超时")

    def adjust_task_time(self):
        dialog = AdjustTimeDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                selected_datetime = dialog.new_deadline_input.dateTime()
                reason = dialog.reason_input.toPlainText().strip()
                
                # 将 QDateTime 转换为 Python datetime
                current_date = datetime.now().date()
                selected_time = selected_datetime.time().toPyTime()
                new_deadline = datetime.combine(current_date, selected_time)
                
                # 如果选择的时间早于当前时间，说明是明天的时间
                if new_deadline <= datetime.now():
                    new_deadline += timedelta(days=1)
                
                self.task_manager.adjust_task(self.current_task['id'], new_deadline, reason)
                self.current_task = self.task_manager.get_task_by_id(self.current_task['id'])
                self.update_countdown()
                self.timer.start(1000)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"调整时间失败: {str(e)}")

    def complete_task(self):
        dialog = CompleteTaskDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            summary = dialog.summary
            self.task_manager.complete_task(self.current_task['id'], summary)
            self.reset_task_ui()

    def reset_task_ui(self):
        self.current_task = None
        self.task_label.setText("🎯 当前没有进行中的任务")
        self.countdown_label.hide()
        self.timer.stop()
        self.complete_task_btn.setEnabled(False)
        self.adjust_time_btn.setEnabled(False)

    def view_history(self):
        dialog = HistoryDialog(self.task_manager, None)
        dialog.exec()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.pressing and self.start_point:
            movement = event.pos() - self.start_point
            self.move(self.pos() + movement)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = False
            self.start_point = None

    def set_reminder(self):
        dialog = ReminderDialog(None)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            minutes = dialog.get_minutes()
            reminder_time = datetime.now() + timedelta(minutes=minutes)
            self.reminders.append({
                'time': reminder_time,
                'minutes': minutes
            })
            
            # 使用自定义消息对话框，父窗口设为 None
            msg_dialog = MessageDialog(
                "⏲️ 提醒已设置",
                f"将在 {minutes} 分钟后提醒您\n({reminder_time.strftime('%H:%M:%S')})",
                None
            )
            msg_dialog.exec()

    def check_reminders(self):
        now = datetime.now()
        remaining_reminders = []
        triggered_reminders = []

        for reminder in self.reminders:
            if now >= reminder['time']:
                triggered_reminders.append(reminder)
            else:
                remaining_reminders.append(reminder)

        self.reminders = remaining_reminders

        for reminder in triggered_reminders:
            # 使用自定义消息对话框，父窗口设为 None
            msg_dialog = MessageDialog(
                "⏰ 来了！",
                f"您设置的 {reminder['minutes']} 分钟提醒时间到了！",
                None
            )
            msg_dialog.exec()

    # ... 其他方法继续拆分 ... 