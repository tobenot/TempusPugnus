from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

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
        """)
        
        # 设置容器布局
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(10, 10, 10, 10)  # 添加外边距
        container_layout.addWidget(self.container)
        
        # 主布局
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)  # 添加间距
        
        # 添加标题栏
        self._setup_title_bar(title)
        
        # 拖动相关
        self.pressing = False
        self.start_point = None

    def _setup_title_bar(self, title):
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 10)
        title_layout.setSpacing(10)
        
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
        """)
        close_btn.clicked.connect(self.reject)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        
        self.layout.addWidget(title_container)

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