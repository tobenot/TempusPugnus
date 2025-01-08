from PyQt6.QtWidgets import QSpinBox, QPushButton, QLabel
from PyQt6.QtCore import Qt
from .base_dialog import BaseDialog

class ReminderDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("⏲️ 设置提醒", parent)
        self.minutes = 1  # 默认1分钟
        self._setup_ui()

    def _setup_ui(self):
        # 创建说明标签
        desc_label = QLabel("设置提醒时间（分钟）:")
        
        # 创建分钟数输入框
        self.minute_input = QSpinBox()
        self.minute_input.setRange(1, 1440)  # 1分钟到24小时
        self.minute_input.setValue(1)
        self.minute_input.setStyleSheet("""
            QSpinBox {
                background-color: rgba(44, 62, 80, 180);
                color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
                min-width: 80px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: rgba(44, 62, 80, 220);
                border: 1px solid #DAA520;
                border-radius: 2px;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: rgba(44, 62, 80, 255);
                border: 1px solid #FFD700;
            }
        """)

        # 确定按钮
        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)

        # 添加到布局
        self.layout.addWidget(desc_label)
        self.layout.addWidget(self.minute_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def get_minutes(self):
        return self.minute_input.value() 