from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QFrame, QStackedWidget, QWidget)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont
from api_client import APIClient


class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setFixedSize(500, 600)
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
            QPushButton#link {
                background: transparent;
                color: #2563eb;
                font-weight: 600;
                text-decoration: underline;
                padding: 4px;
            }
            QPushButton#link:hover {
                color: #1e40af;
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
        
        header = QVBoxLayout()
        header.setSpacing(8)
        
        title = QLabel('Chemical Equipment\nVisualizer')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont('Segoe UI', 28, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2563eb;")
        header.addWidget(title)
        
        self.subtitle = QLabel('Welcome back!')
        self.subtitle.setObjectName('subtitle')
        self.subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont('Segoe UI', 15)
        self.subtitle.setFont(subtitle_font)
        header.addWidget(self.subtitle)
        
        card_layout.addLayout(header)
        card_layout.addSpacing(40)
        
        self.stacked = QStackedWidget()
        
        login_widget = self.create_login_widget()
        register_widget = self.create_register_widget()
        
        self.stacked.addWidget(login_widget)
        self.stacked.addWidget(register_widget)
        
        card_layout.addWidget(self.stacked)
        
        main_layout.addWidget(card)
    
    def create_login_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        widget.setLayout(layout)
        
        username_container = QVBoxLayout()
        username_container.setSpacing(8)
        
        username_label = QLabel('Username')
        username_label.setObjectName('field-label')
        username_label_font = QFont('Segoe UI', 13, QFont.Bold)
        username_label.setFont(username_label_font)
        username_container.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Enter your username')
        username_container.addWidget(self.login_username)
        
        layout.addLayout(username_container)
        
        password_container = QVBoxLayout()
        password_container.setSpacing(8)
        
        password_label = QLabel('Password')
        password_label.setObjectName('field-label')
        password_label_font = QFont('Segoe UI', 13, QFont.Bold)
        password_label.setFont(password_label_font)
        password_container.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Enter your password')
        self.login_password.setEchoMode(QLineEdit.Password)
        password_container.addWidget(self.login_password)
        
        layout.addLayout(password_container)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        login_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(login_btn)
        
        layout.addSpacing(24)
        
        footer = QHBoxLayout()
        footer.addStretch()
        footer_text = QLabel("Don't have an account? ")
        footer_text.setStyleSheet("color: #64748b; font-size: 14px;")
        footer.addWidget(footer_text)
        
        switch_btn = QPushButton('Sign Up')
        switch_btn.setObjectName('link')
        switch_btn.clicked.connect(lambda: self.switch_mode(1))
        footer.addWidget(switch_btn)
        footer.addStretch()
        
        layout.addLayout(footer)
        
        return widget
    
    def create_register_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        widget.setLayout(layout)
        
        username_container = QVBoxLayout()
        username_container.setSpacing(8)
        
        username_label = QLabel('Username')
        username_label.setObjectName('field-label')
        username_label_font = QFont('Segoe UI', 13, QFont.Bold)
        username_label.setFont(username_label_font)
        username_container.addWidget(username_label)
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText('Choose a username')
        username_container.addWidget(self.register_username)
        
        layout.addLayout(username_container)
        
        email_container = QVBoxLayout()
        email_container.setSpacing(8)
        
        email_label = QLabel('Email')
        email_label.setObjectName('field-label')
        email_label_font = QFont('Segoe UI', 13, QFont.Bold)
        email_label.setFont(email_label_font)
        email_container.addWidget(email_label)
        
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText('Enter your email')
        email_container.addWidget(self.register_email)
        
        layout.addLayout(email_container)
        
        password_container = QVBoxLayout()
        password_container.setSpacing(8)
        
        password_label = QLabel('Password')
        password_label.setObjectName('field-label')
        password_label_font = QFont('Segoe UI', 13, QFont.Bold)
        password_label.setFont(password_label_font)
        password_container.addWidget(password_label)
        
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText('Create a password (min 8 characters)')
        self.register_password.setEchoMode(QLineEdit.Password)
        password_container.addWidget(self.register_password)
        
        layout.addLayout(password_container)
        
        confirm_container = QVBoxLayout()
        confirm_container.setSpacing(8)
        
        confirm_label = QLabel('Confirm Password')
        confirm_label.setObjectName('field-label')
        confirm_label_font = QFont('Segoe UI', 13, QFont.Bold)
        confirm_label.setFont(confirm_label_font)
        confirm_container.addWidget(confirm_label)
        
        self.register_password_confirm = QLineEdit()
        self.register_password_confirm.setPlaceholderText('Confirm your password')
        self.register_password_confirm.setEchoMode(QLineEdit.Password)
        confirm_container.addWidget(self.register_password_confirm)
        
        layout.addLayout(confirm_container)
        
        register_btn = QPushButton('Sign Up')
        register_btn.clicked.connect(self.handle_register)
        register_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(register_btn)
        
        layout.addSpacing(24)
        
        footer = QHBoxLayout()
        footer.addStretch()
        footer_text = QLabel('Already have an account? ')
        footer_text.setStyleSheet("color: #64748b; font-size: 14px;")
        footer.addWidget(footer_text)
        
        switch_btn = QPushButton('Login')
        switch_btn.setObjectName('link')
        switch_btn.clicked.connect(lambda: self.switch_mode(0))
        footer.addWidget(switch_btn)
        footer.addStretch()
        
        layout.addLayout(footer)
        
        return widget
    
    def switch_mode(self, index):
        self.stacked.setCurrentIndex(index)
        if index == 0:
            self.subtitle.setText('Welcome back!')
        else:
            self.subtitle.setText('Create your account')
    
    def handle_login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        
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
    
    def handle_register(self):
        username = self.register_username.text()
        email = self.register_email.text()
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()
        
        if not username or not email or not password or not password_confirm:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return
        
        if password != password_confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, 'Error', 'Password must be at least 8 characters')
            return
        
        try:
            client = APIClient()
            client.register(username, email, password)
            
            self.username = username
            self.password = password
            self.accept()
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    if isinstance(error_data, dict):
                        error_msg = ', '.join([f"{k}: {', '.join(v) if isinstance(v, list) else v}" 
                                             for k, v in error_data.items()])
                except:
                    pass
            QMessageBox.critical(self, 'Registration Failed', f'Registration failed: {error_msg}')
    
    def get_credentials(self):
        return self.username, self.password

