from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
                             QLabel, QTabWidget, QListWidget, QListWidgetItem, QMessageBox,
                             QGridLayout, QFrame, QDialog, QApplication, QInputDialog, QLineEdit, QHeaderView,
                             QScrollArea, QProgressBar)
from PyQt5.QtCore import Qt, QSettings, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QMovie
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from api_client import APIClient
import matplotlib.pyplot as plt
import random # For demo trend data


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
        
        # Message label
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
        
        # Animated dots
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
        
        # Animate dots
        self.dot_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_dots)
        self.timer.start(300)
        
        # Style
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


class APIWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.client = APIClient()
        self.client.set_auth(username, password)
        self.current_summary = None
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.is_dark = True  # Enforce dark mode
        self.setup_styles()
        self.init_ui()
        self.load_summary()
    
    def setup_styles(self):
        stylesheet = self.get_dark_styles()
        self.setStyleSheet(stylesheet)
    
    def get_dark_styles(self):
        return """
            QMainWindow {
                background-color: #020204;
            }
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #a1a1aa;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #18181b, stop:1 #09090b);
                color: #fafafa;
                border: 1px solid #27272a;
                border-radius: 20px;
                padding: 10px 24px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                border-color: #f97316;
                background: #27272a;
            }
            QPushButton:pressed {
                background: #3f3f46;
            }
            QPushButton#secondary {
                background: transparent;
                color: #a1a1aa;
                border: 1px solid #27272a;
            }
            QPushButton#secondary:hover {
                color: #f97316;
                border-color: #f97316;
                background: rgba(249, 115, 22, 0.1);
            }
            QTabWidget::pane {
                border: none;
                background: #020204;
            }
            QTabBar::tab {
                background: transparent;
                color: #71717a;
                padding: 12px 24px;
                margin-right: 16px;
                font-weight: 600;
                border-bottom: 2px solid transparent;
                font-size: 15px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                color: #f97316;
                border-bottom: 2px solid #f97316;
            }
            QTabBar::tab:hover {
                color: #a1a1aa;
            }
            QTableWidget {
                border: none;
                border-radius: 8px;
                background-color: #09090b;
                gridline-color: transparent;
                color: #e4e4e7;
                selection-background-color: #27272a;
                selection-color: #f97316;
                outline: none;
            }
            QTableWidget::item {
                padding: 14px;
                border-bottom: 1px solid #27272a;
                color: #e4e4e7;
            }
            QTableWidget::item:selected {
                background-color: #27272a;
                color: #f97316;
            }
            QHeaderView::section {
                background-color: #09090b;
                color: #a1a1aa;
                padding: 14px;
                border: none;
                border-bottom: 1px solid #27272a;
                font-weight: 700;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QListWidget {
                border: 1px solid #27272a;
                border-radius: 20px;
                background: #09090b;
                color: #e4e4e7;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 1px solid #27272a;
                color: #e4e4e7;
            }
            QListWidget::item:hover {
                background: #18181b;
                color: #f97316;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 700;
                color: #fafafa;
                background: none;
                letter-spacing: -0.5px;
            }
            QFrame#card {
                background-color: #09090b;
                border: 1px solid #27272a;
                border-radius: 20px;
            }
            QFrame#card:hover {
                border: 1px solid #3f3f46;
            }
            QWidget#central_widget {
                background-color: #020204;
            }
            QWidget#scroll_content {
                background-color: #020204;
            }
            QScrollArea {
                border: none;
                background-color: #020204;
            }
            QScrollBar:vertical {
                border: none;
                background: #020204;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #27272a;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QProgressBar {
                border: none;
                background-color: #27272a;
                border-radius: 4px;
                text-align: center;
                color: transparent;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fb923c, stop:1 #ea580c);
                border-radius: 4px;
            }
        """
    
    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background: rgba(9, 9, 11, 0.8); border-bottom: 1px solid rgba(255, 255, 255, 0.1);")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(32, 20, 32, 20)
        header_layout.setSpacing(16)
        header.setLayout(header_layout)
        
        self.title_label = QLabel('Chemical Equipment Visualizer')
        self.title_label.setObjectName('title')
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        upload_btn = QPushButton('Upload CSV')
        upload_btn.clicked.connect(self.upload_csv)
        header_layout.addWidget(upload_btn)
        
        pdf_btn = QPushButton('Download PDF')
        pdf_btn.setObjectName('secondary')
        pdf_btn.clicked.connect(self.download_pdf)
        header_layout.addWidget(pdf_btn)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.setObjectName('secondary')
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header)
        layout.addSpacing(24)
        
        # Tabs
        tabs = QTabWidget()
        
        dashboard_tab = self.create_dashboard_tab()
        tabs.addTab(dashboard_tab, 'Dashboard')
        
        history_tab = self.create_history_tab()
        tabs.addTab(history_tab, 'History')
        
        layout.addWidget(tabs)
    
    def create_dashboard_tab(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        content_widget = QWidget()
        content_widget.setObjectName("scroll_content")
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)
        content_widget.setLayout(layout)
        
        # Summary Cards
        self.summary_section = self.create_summary_section()
        layout.addWidget(self.summary_section)
        
        # Charts Section
        self.charts_section = self.create_charts_section()
        layout.addWidget(self.charts_section)
        
        # Table Section
        self.table_section = self.create_table_section()
        layout.addWidget(self.table_section)
        
        layout.addStretch()
        scroll_area.setWidget(content_widget)
        return scroll_area

    def create_summary_section(self):
        widget = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        widget.setLayout(layout)
        
        self.summary_cards = []
        card_data = [
            ('Total Equipment', 'total_count', '#f97316', '📊'),
            ('Avg Flowrate', 'avg_flowrate', '#8b5cf6', '💧'),
            ('Avg Pressure', 'avg_pressure', '#f97316', '⚡'),
            ('Avg Temperature', 'avg_temperature', '#ef4444', '🌡️')
        ]
        
        for i, (label, key, color, icon) in enumerate(card_data):
            card = self.create_summary_card(label, key, color, icon)
            layout.addWidget(card, 0, i)
            self.summary_cards.append(card)
            
        return widget
    
    def create_summary_card(self, label, key, color, icon):
        card = QFrame()
        card.setObjectName('card')
        # Gradient background handled in stylesheet
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        card.setLayout(layout)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 18px; color: {color};")
        header_layout.addWidget(icon_label)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            color: #a1a1aa;
            font-size: 13px;
            font-weight: 500;
        """)
        header_layout.addWidget(label_widget)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        value_label = QLabel('0')
        value_label.setStyleSheet("""
            color: #fafafa;
            font-size: 24px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: -0.5px;
        """)
        value_label.setObjectName(f'value_{key}')
        layout.addWidget(value_label)
        
        return card

    def create_charts_section(self):
        container = QFrame()
        container.setObjectName('card')
        layout = QHBoxLayout() # Horizontal layout for Pie + Progress Bars
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(32)
        container.setLayout(layout)
        
        # Left: Pie Chart
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_widget.setLayout(left_layout)
        
        pie_title = QLabel("Equipment Distribution")
        pie_title.setStyleSheet("font-size: 15px; font-weight: 600; color: #fafafa; margin-bottom: 10px;")
        left_layout.addWidget(pie_title)

        self.chart_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.chart_canvas.figure.patch.set_facecolor('#09090b') # Match bg
        self.chart_canvas.setMinimumHeight(400)
        left_layout.addWidget(self.chart_canvas)
        
        layout.addWidget(left_widget, 1) # Stretch factor 1
        
        # Right: Progress Bars (Analytics Overview)
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(24)
        right_widget.setLayout(right_layout)
        
        stats_title = QLabel("Average Statistics")
        stats_title.setStyleSheet("font-size: 15px; font-weight: 600; color: #fafafa; margin-bottom: 10px;")
        right_layout.addWidget(stats_title)
        
        self.progress_bars = {}
        stats_config = [
            ('Flowrate', 'avg_flowrate', 200), # Max value approx
            ('Pressure', 'avg_pressure', 20),
            ('Temperature', 'avg_temperature', 300)
        ]
        
        for label, key, max_val in stats_config:
            stat_container = QWidget()
            stat_layout = QVBoxLayout()
            stat_layout.setSpacing(8)
            stat_layout.setContentsMargins(0, 0, 0, 0)
            stat_container.setLayout(stat_layout)
            
            # Label Row
            label_row = QHBoxLayout()
            name_label = QLabel(label)
            name_label.setStyleSheet("color: #a1a1aa; font-size: 13px; font-weight: 500;")
            label_row.addWidget(name_label)
            
            val_label = QLabel("0.00")
            val_label.setObjectName(f"val_{key}")
            val_label.setStyleSheet("color: #fafafa; font-size: 13px; font-weight: 600; font-family: 'Consolas', monospace;")
            label_row.addWidget(val_label)
            stat_layout.addLayout(label_row)
            
            # Progress Bar
            pbar = QProgressBar()
            pbar.setRange(0, max_val)
            pbar.setValue(0)
            pbar.setFixedHeight(6) # Thin and sleek
            # Use global stylesheet for gradient
            self.progress_bars[key] = pbar
            stat_layout.addWidget(pbar)
            
            right_layout.addWidget(stat_container)
            
        right_layout.addStretch()
        layout.addWidget(right_widget, 1) # Stretch factor 1
        
        return container

    def create_table_section(self):
        container = QFrame()
        container.setObjectName('card')
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        container.setLayout(layout)
        
        title = QLabel("Equipment Data")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #fafafa;")
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setMinimumHeight(400)
        layout.addWidget(self.table)
        
        return container
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        widget.setLayout(layout)
        
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        
        return widget
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if file_path:
            progress = LoadingDialog('Uploading CSV file...', self)
            progress.show()
            QApplication.processEvents()
            
            self.worker = APIWorker(self.client.upload_csv, file_path)
            
            def on_upload_finished(result):
                progress.close()
                self.current_summary = result['summary']
                self.update_ui()
                self.load_history(show_loading=False)
                self.show_message(QMessageBox.Information, 'Success', 'CSV uploaded successfully')
            
            def on_upload_error(error):
                progress.close()
                self.show_message(QMessageBox.Critical, 'Error', f'Upload failed: {error}')
            
            self.worker.finished.connect(on_upload_finished)
            self.worker.error.connect(on_upload_error)
            self.worker.start()
    
    def refresh_data(self):
        progress = LoadingDialog('Refreshing data...', self)
        progress.show()
        QApplication.processEvents()
        
        self.worker = APIWorker(self.client.get_summary)
        
        def on_refresh_finished(result):
            progress.close()
            if result:
                self.current_summary = result['summary']
                self.update_ui()
                self.load_history(show_loading=False)
                self.show_message(QMessageBox.Information, 'Success', 'Data refreshed successfully!')
        
        def on_refresh_error(error):
            if hasattr(progress, 'close'):
                progress.close()
            self.show_message(QMessageBox.Warning, 'Error', f'Failed to refresh data: {error}')
        
        self.worker.finished.connect(on_refresh_finished)
        self.worker.error.connect(on_refresh_error)
        self.worker.start()
    
    def load_summary(self, show_loading=True):
        if show_loading:
            progress = LoadingDialog('Loading data...', self)
            progress.show()
            QApplication.processEvents()
        else:
            progress = None
        
        self.worker = APIWorker(self.client.get_summary)
        
        def on_summary_finished(data):
            if progress:
                progress.close()
            self.current_summary = data['summary']
            self.update_ui()
            self.load_history(show_loading=show_loading)
        
        def on_summary_error(error):
            if progress:
                progress.close()
        
        self.worker.finished.connect(on_summary_finished)
        self.worker.error.connect(on_summary_error)
        self.worker.start()
    
    def update_ui(self):
        if not self.current_summary:
            return
        
        # Update Summary Cards
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
        
        # Monospace font for numbers
        mono_font = QFont("Consolas", 10)
        
        for row, item in enumerate(data):
            # Equipment Name
            name_item = QTableWidgetItem(str(item.get('Equipment Name', '')))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(str(item.get('Type', '')))
            type_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 1, type_item)
            
            # Numerical columns
            for col, key in enumerate(['Flowrate', 'Pressure', 'Temperature'], start=2):
                val = item.get(key, 0)
                # Format to 2 decimal places
                val_str = f"{float(val):.2f}" if val else "0.00"
                
                num_item = QTableWidgetItem(val_str)
                num_item.setFont(mono_font)
                num_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, col, num_item)
        
        # self.table.resizeColumnsToContents()
    
    def update_charts(self):
        if not self.current_summary:
            return
        
        # 1. Update Pie Chart
        self.chart_canvas.figure.clear()
        
        # Dark theme chart styling
        plt.style.use('dark_background')
        
        fig = self.chart_canvas.figure
        fig.patch.set_facecolor('#09090b')
        
        ax = fig.add_subplot(111)
        ax.set_facecolor('#09090b')
        
        type_dist = self.current_summary['type_distribution']
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        
        # Orange and Purple palette
        colors = ['#f97316', '#8b5cf6', '#fb923c', '#a78bfa', '#fdba74']
        
        wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)], 
                startangle=90, textprops={'color': '#a1a1aa'}, radius=1.1)
        
        plt.setp(autotexts, size=10, weight="bold", color="#fafafa")
        plt.setp(texts, size=10)
        
        fig.tight_layout()
        self.chart_canvas.draw()
        
        # 2. Update Progress Bars
        stats_map = {
            'avg_flowrate': 200,
            'avg_pressure': 20,
            'avg_temperature': 300
        }
        
        for key, max_val in stats_map.items():
            if key in self.current_summary:
                val = self.current_summary[key]
                
                # Update Label
                val_label = self.findChild(QLabel, f"val_{key}")
                if val_label:
                    val_label.setText(f"{val:.2f}")
                
                # Update Progress Bar
                if hasattr(self, 'progress_bars') and key in self.progress_bars:
                    pbar = self.progress_bars[key]
                    pbar.setValue(int(min(val, max_val)))
    
    def load_history(self, show_loading=True):
        if show_loading:
            progress = LoadingDialog('Loading history...', self)
            progress.show()
            QApplication.processEvents()
        else:
            progress = None
        
        self.history_worker = APIWorker(self.client.get_history)
        
        def on_history_finished(history):
            if progress:
                progress.close()
            self.history_list.clear()
            
            for item in history:
                date_str = item['uploaded_at'][:19].replace('T', ' ')
                text = f"Dataset #{item['id']} - {date_str}\n"
                text += f"Total: {item['summary']['total_count']} | "
                text += f"Flowrate: {item['summary']['avg_flowrate']:.2f} | "
                text += f"Pressure: {item['summary']['avg_pressure']:.2f} | "
                text += f"Temp: {item['summary']['avg_temperature']:.2f}"
                
                list_item = QListWidgetItem(text)
                list_item.setFont(QFont('Segoe UI', 10))
                self.history_list.addItem(list_item)
        
        def on_history_error(error):
            if progress:
                progress.close()
        
        self.history_worker.finished.connect(on_history_finished)
        self.history_worker.error.connect(on_history_error)
        self.history_worker.start()
    
    def download_pdf(self):
        if not self.current_summary:
            self.show_message(QMessageBox.Warning, 'No Data', 'Please upload a CSV file first')
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF Report', 'equipment_report.pdf', 'PDF Files (*.pdf)'
        )
        
        if save_path:
            progress = LoadingDialog('Generating PDF report...', self)
            progress.show()
            QApplication.processEvents()
            
            self.pdf_worker = APIWorker(self.client.download_pdf, save_path)
            
            def on_pdf_finished(result):
                progress.close()
                self.show_message(
                    QMessageBox.Information,
                    'Success',
                    f'PDF report saved to:\n{save_path}'
                )
            
            def on_pdf_error(error):
                progress.close()
                self.show_message(QMessageBox.Critical, 'Error', f'Failed to generate PDF: {str(error)}')
            
            self.pdf_worker.finished.connect(on_pdf_finished)
            self.pdf_worker.error.connect(on_pdf_error)
            self.pdf_worker.start()
    
    def show_message(self, icon, title, text):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet(
            "QMessageBox { background-color: #18181b; color: #fafafa; } "
            "QLabel { color: #fafafa; } "
            "QPushButton { color: #fafafa; background-color: #27272a; border: 1px solid #3f3f46; border-radius: 6px; padding: 6px 16px; }"
            "QPushButton:hover { background-color: #3f3f46; }"
        )
        return msg.exec_()

