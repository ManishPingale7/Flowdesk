from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette
from api_client import APIClient


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login - Chemical Equipment Visualizer')
        self.setFixedSize(480, 520)
        self.username = None
        self.password = None
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QFrame#card {
                background: white;
                border-radius: 20px;
            }
            QLabel {
                color: #1e293b;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: 700;
                color: #2563eb;
                background: transparent;
            }
            QLabel#subtitle {
                color: #64748b;
                font-size: 15px;
                font-weight: 400;
            }
            QLabel#field-label {
                color: #1e293b;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 4px;
            }
            QLineEdit {
                padding: 14px 18px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                font-size: 15px;
                background: white;
                color: #1e293b;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2563eb, stop:1 #3b82f6);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 28px;
                font-weight: 600;
                font-size: 16px;
                min-height: 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e40af, stop:1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e3a8a, stop:1 #1e40af);
            }
        """)
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        card = QFrame()
        card.setObjectName('card')
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(48, 56, 48, 56)
        card_layout.setSpacing(0)
        card.setLayout(card_layout)
        
        title = QLabel('Chemical Equipment\nVisualizer')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont('Segoe UI', 28, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2563eb;")
        card_layout.addWidget(title)
        
        card_layout.addSpacing(12)
        
        subtitle = QLabel('Login to continue')
        subtitle.setObjectName('subtitle')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont('Segoe UI', 15)
        subtitle.setFont(subtitle_font)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(40)
        
        username_container = QVBoxLayout()
        username_container.setSpacing(8)
        
        username_label = QLabel('Username')
        username_label.setObjectName('field-label')
        username_label_font = QFont('Segoe UI', 13, QFont.Bold)
        username_label.setFont(username_label_font)
        username_container.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        username_container.addWidget(self.username_input)
        
        card_layout.addLayout(username_container)
        
        card_layout.addSpacing(24)
        
        password_container = QVBoxLayout()
        password_container.setSpacing(8)
        
        password_label = QLabel('Password')
        password_label.setObjectName('field-label')
        password_label_font = QFont('Segoe UI', 13, QFont.Bold)
        password_label.setFont(password_label_font)
        password_container.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_container.addWidget(self.password_input)
        
        card_layout.addLayout(password_container)
        
        card_layout.addSpacing(32)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        login_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(login_btn)
        
        main_layout.addWidget(card)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            client = APIClient()
            client.set_auth(username, password)
            client.get_history()
            
            self.username = username
            self.password = password
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Login Failed', f'Invalid credentials: {str(e)}')
    
    def get_credentials(self):
        return self.username, self.password
