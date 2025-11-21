from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
                             QLabel, QTabWidget, QListWidget, QListWidgetItem, QMessageBox,
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from api_client import APIClient
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.client = APIClient()
        self.client.set_auth(username, password)
        self.current_summary = None
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1400, 900)
        self.setup_styles()
        self.init_ui()
        self.load_summary()
    
    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
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
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e40af, stop:1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e3a8a, stop:1 #1e40af);
            }
            QPushButton#secondary {
                background: white;
                color: #1e293b;
                border: 1px solid #e2e8f0;
            }
            QPushButton#secondary:hover {
                background: #f8fafc;
                border-color: #2563eb;
                color: #2563eb;
            }
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                background: white;
                padding: 16px;
            }
            QTabBar::tab {
                background: #f8fafc;
                color: #64748b;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: white;
                color: #2563eb;
                border-bottom: 2px solid #2563eb;
            }
            QTabBar::tab:hover {
                background: #f1f5f9;
            }
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8fafc, stop:1 #f1f5f9);
                color: #1e293b;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
            }
            QListWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 1px solid #e2e8f0;
                border-radius: 8px;
                margin: 4px;
            }
            QListWidget::item:hover {
                background: #f8fafc;
            }
            QListWidget::item:selected {
                background: #eff6ff;
                color: #2563eb;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 600;
                color: #1e293b;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2563eb, stop:1 #7c3aed);
                -webkit-background-clip: text;
                color: transparent;
            }
            QFrame#card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 24px;
            }
            QLabel#summary-label {
                font-size: 16px;
                color: #64748b;
                padding: 20px;
            }
        """)
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)
        
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #e2e8f0;
                padding: 20px 32px;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header.setLayout(header_layout)
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setObjectName('title')
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2563eb;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        upload_btn = QPushButton('📤 Upload CSV')
        upload_btn.clicked.connect(self.upload_csv)
        header_layout.addWidget(upload_btn)
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setObjectName('secondary')
        refresh_btn.clicked.connect(self.load_summary)
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #f8fafc;
            }
        """)
        
        summary_tab = self.create_summary_tab()
        tabs.addTab(summary_tab, '📊 Summary')
        
        table_tab = self.create_table_tab()
        tabs.addTab(table_tab, '📋 Equipment Table')
        
        charts_tab = self.create_charts_tab()
        tabs.addTab(charts_tab, '📈 Charts')
        
        history_tab = self.create_history_tab()
        tabs.addTab(history_tab, '📜 History')
        
        layout.addWidget(tabs)
    
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        widget.setLayout(layout)
        
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        
        self.summary_cards = []
        card_data = [
            ('Total Equipment', 'total_count', '#2563eb', '📊'),
            ('Avg Flowrate', 'avg_flowrate', '#10b981', '💧'),
            ('Avg Pressure', 'avg_pressure', '#f59e0b', '⚡'),
            ('Avg Temperature', 'avg_temperature', '#ef4444', '🌡️')
        ]
        
        for i, (label, key, color, icon) in enumerate(card_data):
            card = self.create_summary_card(label, key, color, icon)
            cards_layout.addWidget(card, i // 2, i % 2)
            self.summary_cards.append(card)
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        
        return widget
    
    def create_summary_card(self, label, key, color, icon):
        card = QFrame()
        card.setObjectName('card')
        card.setStyleSheet(f"""
            QFrame#card {{
                background: white;
                border: 1px solid #e2e8f0;
                border-left: 4px solid {color};
                border-radius: 12px;
                padding: 24px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        card.setLayout(layout)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon_label)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            color: #64748b;
            font-size: 13px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(label_widget)
        
        value_label = QLabel('0')
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 32px;
            font-weight: 700;
        """)
        value_label.setObjectName(f'value_{key}')
        layout.addWidget(value_label)
        
        return card
    
    def create_table_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        widget.setLayout(layout)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
            }
            QTableWidget::item {
                border: none;
            }
            QTableWidget::item:alternate {
                background: #f8fafc;
            }
        """)
        layout.addWidget(self.table)
        
        return widget
    
    def create_charts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        widget.setLayout(layout)
        
        self.chart_canvas = FigureCanvas(Figure(figsize=(12, 6)))
        self.chart_canvas.figure.patch.set_facecolor('#ffffff')
        layout.addWidget(self.chart_canvas)
        
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        widget.setLayout(layout)
        
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        
        return widget
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if file_path:
            try:
                result = self.client.upload_csv(file_path)
                self.current_summary = result['summary']
                self.update_ui()
                QMessageBox.information(self, 'Success', 'CSV uploaded successfully')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def load_summary(self):
        try:
            data = self.client.get_summary()
            self.current_summary = data['summary']
            self.update_ui()
            self.load_history()
        except Exception as e:
            if hasattr(self, 'summary_label'):
                self.summary_label.setText(f'No data available: {str(e)}')
    
    def update_ui(self):
        if not self.current_summary:
            return
        
        if hasattr(self, 'summary_cards'):
            card_keys = ['total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
            for i, card in enumerate(self.summary_cards):
                key = card_keys[i]
                value_widget = card.findChild(QLabel, f'value_{key}')
                if value_widget:
                    if key == 'total_count':
                        value_widget.setText(str(self.current_summary[key]))
                    else:
                        value_widget.setText(f"{self.current_summary[key]:.2f}")
        
        self.update_table()
        self.update_charts()
    
    def update_table(self):
        if not self.current_summary or 'equipment_data' not in self.current_summary:
            return
        
        data = self.current_summary['equipment_data']
        if not data:
            return
        
        headers = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            for col, header in enumerate(headers):
                value = str(item.get(header, ''))
                item_widget = QTableWidgetItem(value)
                self.table.setItem(row, col, item_widget)
        
        self.table.resizeColumnsToContents()
    
    def update_charts(self):
        if not self.current_summary:
            return
        
        self.chart_canvas.figure.clear()
        
        plt.style.use('seaborn-v0_8-whitegrid')
        fig = self.chart_canvas.figure
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        type_dist = self.current_summary['type_distribution']
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        
        colors = ['#2563eb', '#7c3aed', '#10b981', '#f59e0b', '#ef4444']
        ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)], startangle=90)
        ax1.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20)
        
        stats = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_summary['avg_flowrate'],
            self.current_summary['avg_pressure'],
            self.current_summary['avg_temperature']
        ]
        
        bars = ax2.bar(stats, values, color=['#2563eb', '#10b981', '#f59e0b'])
        ax2.set_title('Average Statistics', fontsize=14, fontweight='bold', pad=20)
        ax2.set_ylabel('Value', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
        
        fig.tight_layout()
        self.chart_canvas.draw()
    
    def load_history(self):
        try:
            history = self.client.get_history()
            self.history_list.clear()
            
            for item in history:
                date_str = item['uploaded_at'][:19].replace('T', ' ')
                text = f"📦 Dataset #{item['id']} - {date_str}\n"
                text += f"Total: {item['summary']['total_count']} | "
                text += f"Flowrate: {item['summary']['avg_flowrate']:.2f} | "
                text += f"Pressure: {item['summary']['avg_pressure']:.2f} | "
                text += f"Temp: {item['summary']['avg_temperature']:.2f}"
                
                list_item = QListWidgetItem(text)
                list_item.setFont(QFont('Segoe UI', 11))
                self.history_list.addItem(list_item)
        except Exception as e:
            pass
