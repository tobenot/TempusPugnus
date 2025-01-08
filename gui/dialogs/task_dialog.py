from PyQt6.QtWidgets import QLabel, QPushButton, QTextEdit, QDateTimeEdit, QMessageBox, QDialog
from PyQt6.QtCore import Qt, QDateTime, QObject, QEvent
from .base_dialog import BaseDialog

class TaskDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("✨ 新建任务", parent)
        
        self._setup_ui()
        self._setup_time_editor()

    def _setup_ui(self):
        task_label = QLabel("📝 任务描述:")
        self.task_input = QTextEdit()
        self.task_input.setMaximumHeight(80)

        deadline_label = QLabel("⏰ 截止时间:")
        self.deadline_input = QDateTimeEdit()
        
        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        self.layout.addWidget(task_label)
        self.layout.addWidget(self.task_input)
        self.layout.addWidget(deadline_label)
        self.layout.addWidget(self.deadline_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _setup_time_editor(self):
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
        
        # 添加滚轮事件过滤器
        self.time_filter = TimeEditEventFilter(self)
        self.deadline_input.installEventFilter(self.time_filter)
        
        # 设置样式
        self._setup_time_editor_style()

    def _setup_time_editor_style(self):
        self.deadline_input.setStyleSheet("""
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

    def accept(self):
        selected_time = self.deadline_input.dateTime()
        current_time = QDateTime.currentDateTime()
        
        if selected_time.time() <= current_time.time():
            selected_time = selected_time.addDays(1)
        
        self.task_description = self.task_input.toPlainText().strip()
        self.deadline_str = selected_time.toString("yyyy-MM-dd HH:mm:ss")
        
        if not self.task_description:
            QMessageBox.warning(self, "提示", "请输入任务描述")
            return
            
        super().accept()

class TimeEditEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            section = obj.currentSectionIndex()
            delta = event.angleDelta().y()
            if section == 0:  # 小时部分
                if delta > 0:
                    obj.setTime(obj.time().addSecs(3600))
                else:
                    obj.setTime(obj.time().addSecs(-3600))
            elif section == 1:  # 分钟部分
                if delta > 0:
                    obj.setTime(obj.time().addSecs(300))
                else:
                    obj.setTime(obj.time().addSecs(-300))
            return True
        return False 