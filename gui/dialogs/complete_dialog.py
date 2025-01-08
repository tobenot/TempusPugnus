from PyQt6.QtWidgets import QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
from .base_dialog import BaseDialog

class CompleteTaskDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("✅ 完成任务", parent)
        self._setup_ui()

    def _setup_ui(self):
        summary_label = QLabel("📝 任务总结 (可选):")
        self.summary_input = QTextEdit()
        self.summary_input.setMaximumHeight(150)

        confirm_btn = QPushButton("确定")
        confirm_btn.clicked.connect(self.accept)
        
        self.layout.addWidget(summary_label)
        self.layout.addWidget(self.summary_input)
        self.layout.addWidget(confirm_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def accept(self):
        self.summary = self.summary_input.toPlainText().strip()
        super().accept() 