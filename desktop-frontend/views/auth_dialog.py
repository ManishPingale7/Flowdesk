from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QFrame, QStackedWidget, QWidget, QApplication)
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QFont
from api_client import APIClient


class LoadingDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Loading')
        self.setModal(True)
        self.setFixedSize(300, 120)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 500;
                color: #f1f5f9;
            }
        """)
        layout.addWidget(self.label)
        
        self.dots_label = QLabel('...')
        self.dots_label.setAlignment(Qt.AlignCenter)
        self.dots_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #f97316;
            }
        """)
        layout.addWidget(self.dots_label)
        
        self.setLayout(layout)
        
        self.dot_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_dots)
        self.timer.start(300)
        
        self.setStyleSheet("""
            QDialog {
                background: #09090b;
                border-radius: 20px;
                border: 1px solid #27272a;
            }
        """)
    
    def animate_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        self.dots_label.setText('.' * (self.dot_count + 1))
    
    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)


class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setFixedSize(550, 680)
        self.username = None
        self.password = None
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: #020204;
            }
            QFrame#card {
                background: #09090b;
                border: 1px solid #27272a;
                border-radius: 20px;
            }
            QLabel {
                color: #a1a1aa;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: 700;
                color: #fafafa;
                background: transparent;
                letter-spacing: -1px;
            }
            QLabel#subtitle {
                color: #a1a1aa;
                font-size: 15px;
                font-weight: 400;
            }
            QLabel#field-label {
                color: #e4e4e7;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 4px;
            }
            QLineEdit {
                padding: 14px 18px;
                border: 1px solid #27272a;
                border-radius: 10px;
                font-size: 15px;
                background: #18181b;
                color: #fafafa;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #f97316;
                background: #18181b;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #71717a;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #18181b, stop:1 #09090b);
                color: #fafafa;
                border: 1px solid #27272a;
                border-radius: 20px;
                padding: 14px 28px;
                font-weight: 600;
                font-size: 16px;
                min-height: 24px;
            }
            QPushButton:hover {
                border-color: #f97316;
                background: #27272a;
            }
            QPushButton:pressed {
                background: #3f3f46;
            }
            QPushButton#link {
                background: transparent;
                color: #f97316;
                font-weight: 600;
                text-decoration: none;
                padding: 4px;
                border: none;
            }
            QPushButton#link:hover {
                color: #fb923c;
                text-decoration: underline;
                border: none;
                background: transparent;
            }
        """)
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        card = QFrame()
        card.setObjectName('card')
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(0)
        card.setLayout(card_layout)
        
        header = QVBoxLayout()
        header.setSpacing(12)
        
        title = QLabel('Chemical Equipment\nVisualizer')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont('Segoe UI', 24, QFont.Bold)
        title.setFont(title_font)
        # title.setStyleSheet("color: #2563eb;") # Removed to let stylesheet handle it
        header.addWidget(title)
        
        self.subtitle = QLabel('Welcome back!')
        self.subtitle.setObjectName('subtitle')
        self.subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont('Segoe UI', 14)
        self.subtitle.setFont(subtitle_font)
        header.addWidget(self.subtitle)
        
        card_layout.addLayout(header)
        card_layout.addSpacing(30)
        
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
        layout.setSpacing(16)
        widget.setLayout(layout)
        
        username_container = QVBoxLayout()
        username_container.setSpacing(6)
        
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
        password_container.setSpacing(6)
        
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
        
        layout.addSpacing(16)
        
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
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        widget.setLayout(layout)
        
        username_container = QVBoxLayout()
        username_container.setSpacing(0)
        
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
        email_container.setSpacing(0)
        
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
        password_container.setSpacing(0)
        
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
        confirm_container.setSpacing(0)
        
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
        
        layout.addSpacing(6)

        register_btn = QPushButton('Sign Up')
        register_btn.clicked.connect(self.handle_register)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setMinimumHeight(46)
        layout.addWidget(register_btn)
        
        layout.addSpacing(10)
        
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
        layout.addStretch()
        
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
            self.show_message(QMessageBox.Warning, 'Error', 'Please enter username and password')
            return
        
        progress = LoadingDialog('Logging in...', self)
        progress.show()
        QApplication.processEvents()
        
        try:
            client = APIClient()
            client.set_auth(username, password)
            client.get_history()
            
            progress.close()
            self.username = username
            self.password = password
            self.accept()
        except Exception as e:
            progress.close()
            self.show_message(QMessageBox.Critical, 'Login Failed', f'Invalid credentials: {str(e)}')
    
    def handle_register(self):
        username = self.register_username.text()
        email = self.register_email.text()
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()
        
        if not username or not email or not password or not password_confirm:
            self.show_message(QMessageBox.Warning, 'Error', 'Please fill in all fields')
            return
        
        if password != password_confirm:
            self.show_message(QMessageBox.Warning, 'Error', 'Passwords do not match')
            return
        
        if len(password) < 8:
            self.show_message(QMessageBox.Warning, 'Error', 'Password must be at least 8 characters')
            return
        
        progress = LoadingDialog('Creating account...', self)
        progress.show()
        QApplication.processEvents()
        
        try:
            client = APIClient()
            client.register(username, email, password)
            
            progress.close()
            self.username = username
            self.password = password
            self.accept()
        except Exception as e:
            progress.close()
            error_msg = str(e)
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    if isinstance(error_data, dict):
                        error_msg = ', '.join([f"{k}: {', '.join(v) if isinstance(v, list) else v}" 
                                             for k, v in error_data.items()])
                except:
                    pass
            self.show_message(QMessageBox.Critical, 'Registration Failed', f'Registration failed: {error_msg}')
    
    def get_credentials(self):
        return self.username, self.password

    def show_message(self, icon, title, text):
        dialog = QMessageBox(self)
        dialog.setIcon(icon)
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.setStyleSheet(
            'QMessageBox { background-color: #0f172a; border-radius: 12px; } '
            'QLabel { color: #f1f5f9; font-size: 14px; } '
            'QPushButton { color: #f1f5f9; font-weight: 600; background: #111827; border-radius: 6px; padding: 6px 14px; }'
        )
        return dialog.exec_()

