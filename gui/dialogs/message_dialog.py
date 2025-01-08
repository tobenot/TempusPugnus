from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from .base_dialog import BaseDialog

class MessageDialog(BaseDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(title, parent)
        self._setup_ui(message)

    def _setup_ui(self, message):
        # 消息文本
        msg_label = QLabel(message)
        msg_label.setStyleSheet("""
            color: #FFD700;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        msg_label.setWordWrap(True)
        
        # 确定按钮
        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
            background-color: rgba(44, 62, 80, 180);
            color: #FFD700;
            border: 1px solid #DAA520;
            border-radius: 4px;
            padding: 3px 6px;
            font-size: 14px;
            font-weight: bold;
            min-width: 50px;
        """)
        confirm_btn.clicked.connect(self.accept)
        
        # 添加到布局
        self.layout.addWidget(msg_label)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter) 