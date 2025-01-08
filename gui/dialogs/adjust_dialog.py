from PyQt6.QtWidgets import QLabel, QPushButton, QTextEdit, QDateTimeEdit, QMessageBox
from PyQt6.QtCore import Qt, QDateTime
from .base_dialog import BaseDialog
from .task_dialog import TimeEditEventFilter

class AdjustTimeDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("⏰ 调整时限", parent)
        self._setup_ui()
        self._setup_time_editor()

    def _setup_ui(self):
        reason_label = QLabel("💭 调整原因:")
        self.reason_input = QTextEdit()
        self.reason_input.setMaximumHeight(80)

        deadline_label = QLabel("📅 新的截止时间:")
        self.new_deadline_input = QDateTimeEdit()
        
        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        self.layout.addWidget(reason_label)
        self.layout.addWidget(self.reason_input)
        self.layout.addWidget(deadline_label)
        self.layout.addWidget(self.new_deadline_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _setup_time_editor(self):
        current = QDateTime.currentDateTime()
        default_time = current.addSecs(15 * 60)
        self.new_deadline_input.setDateTime(default_time)
        
        self.new_deadline_input.setDisplayFormat("HH   :   mm")
        self.new_deadline_input.setButtonSymbols(QDateTimeEdit.ButtonSymbols.NoButtons)
        
        # 添加滚轮事件过滤器
        self.time_filter = TimeEditEventFilter(self)
        self.new_deadline_input.installEventFilter(self.time_filter)
        
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

    def accept(self):
        selected_time = self.new_deadline_input.dateTime()
        current_time = QDateTime.currentDateTime()
        
        if selected_time.time() <= current_time.time():
            selected_time = selected_time.addDays(1)
        
        self.reason = self.reason_input.toPlainText().strip()
        self.deadline_str = selected_time.toString("yyyy-MM-dd HH:mm:ss")
        
        if not self.reason:
            QMessageBox.warning(self, "提示", "请输入调整原因")
            return
            
        super().accept() 