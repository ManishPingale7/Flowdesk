from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from api_client import APIClient


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login - Chemical Equipment Visualizer')
        self.setFixedSize(420, 320)
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
            QLabel {
                color: #1e293b;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: 700;
                color: #2563eb;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2563eb, stop:1 #7c3aed);
                -webkit-background-clip: text;
            }
            QLabel#subtitle {
                color: #64748b;
                font-size: 15px;
                font-weight: 400;
            }
            QLineEdit {
                padding: 12px 16px;
                border: 1.5px solid #e2e8f0;
                border-radius: 8px;
                font-size: 15px;
                background: white;
                color: #1e293b;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2563eb, stop:1 #3b82f6);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 500;
                font-size: 15px;
                margin-top: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e40af, stop:1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e3a8a, stop:1 #1e40af);
            }
            QFrame#card {
                background: white;
                border-radius: 16px;
                padding: 48px;
            }
        """)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        card = QFrame()
        card.setObjectName('card')
        card_layout = QVBoxLayout()
        card_layout.setSpacing(24)
        card.setLayout(card_layout)
        
        title = QLabel('Chemical Equipment\nVisualizer')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(QFont.Bold)
        title.setFont(title_font)
        card_layout.addWidget(title)
        
        subtitle = QLabel('Login to continue')
        subtitle.setObjectName('subtitle')
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        
        username_label = QLabel('Username:')
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        card_layout.addWidget(self.username_input)
        
        password_label = QLabel('Password:')
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)
        
        card_layout.addStretch()
        layout.addWidget(card)
    
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
