from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
                             QLabel, QTabWidget, QListWidget, QListWidgetItem, QMessageBox,
                             QGridLayout, QFrame, QDialog, QApplication, QInputDialog, QLineEdit, QHeaderView)
from PyQt5.QtCore import Qt, QSettings, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QMovie
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from api_client import APIClient
import matplotlib.pyplot as plt


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
                color: #1e293b;
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
                color: #2563eb;
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
                background: white;
                border-radius: 12px;
                border: 2px solid #e2e8f0;
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
        self.settings = QSettings('ChemViz', 'Theme')
        self.is_dark = self.settings.value('dark_mode', False, type=bool)
        self.setup_styles()
        self.init_ui()
        self.load_summary()
    
    def setup_styles(self):
        if self.is_dark:
            stylesheet = self.get_dark_styles()
        else:
            stylesheet = self.get_light_styles()
        self.setStyleSheet(stylesheet)
    
    def get_light_styles(self):
        return """
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
                color: #0f172a;
                background: none;
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
        """
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)
        
        header = QFrame()
        header.setFrameShape(QFrame.NoFrame)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(10)
        header.setLayout(header_layout)
        
        self.title_label = QLabel('Chemical Equipment Visualizer')
        self.title_label.setObjectName('title')
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Bold)
        self.title_label.setFont(title_font)
        # Explicitly set text color based on theme to prevent gradient issues
        if self.is_dark:
            self.title_label.setStyleSheet('color: #f1f5f9;')
        else:
            self.title_label.setStyleSheet('color: #1e293b;')
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        upload_btn = QPushButton('📤 Upload CSV')
        upload_btn.clicked.connect(self.upload_csv)
        header_layout.addWidget(upload_btn)
        
        pdf_btn = QPushButton('📄 Download PDF')
        pdf_btn.setObjectName('secondary')
        pdf_btn.clicked.connect(self.download_pdf)
        header_layout.addWidget(pdf_btn)
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setObjectName('secondary')
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        self.theme_btn = QPushButton('🌙' if not self.is_dark else '☀️')
        self.theme_btn.setObjectName('secondary')
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        layout.addWidget(header)
        
        tabs = QTabWidget()
        
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
        widget.setAutoFillBackground(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table_style()
        layout.addWidget(self.table)
        
        return widget
    
    def update_table_style(self):
        if self.is_dark:
            self.table.setStyleSheet("""
                QTableWidget {
                    background-color: #1e293b;
                    color: #f1f5f9;
                    gridline-color: #334155;
                    border: none;
                }
                QTableWidget::item {
                    border: none;
                    color: #f1f5f9;
                    padding: 8px;
                    background-color: transparent;
                }
                QTableWidget::item:alternate {
                    background-color: #0f172a;
                }
                QTableWidget::item:selected {
                    background-color: #334155;
                    color: #60a5fa;
                }
                QHeaderView::section {
                    background-color: #0f172a;
                    color: #f1f5f9;
                    padding: 12px;
                    border: none;
                    border-bottom: 1px solid #334155;
                    border-right: 1px solid #334155;
                    font-weight: 600;
                }
                QHeaderView::section:last {
                    border-right: none;
                }
                QTableCornerButton::section {
                    background-color: #0f172a;
                    border: none;
                }
            """)
        else:
            self.table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    color: #1e293b;
                    gridline-color: #e2e8f0;
                    border: none;
                }
                QTableWidget::item {
                    border: none;
                    color: #1e293b;
                    padding: 8px;
                    background-color: transparent;
                }
                QTableWidget::item:alternate {
                    background-color: #f8fafc;
                }
                QTableWidget::item:selected {
                    background-color: #eff6ff;
                    color: #2563eb;
                }
                QHeaderView::section {
                    background-color: #f8fafc;
                    color: #1e293b;
                    padding: 12px;
                    border: none;
                    border-bottom: 1px solid #e2e8f0;
                    border-right: 1px solid #e2e8f0;
                    font-weight: 600;
                }
                QHeaderView::section:last {
                    border-right: none;
                }
                QTableCornerButton::section {
                    background-color: #f8fafc;
                    border: none;
                }
            """)
    
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
        """Refresh data with loading dialog"""
        progress = LoadingDialog('Refreshing data...', self)
        progress.show()
        QApplication.processEvents()
        
        self.worker = APIWorker(self.client.get_summary)
        
        def on_refresh_finished(result):
            progress.close()
            if result:
                self.current_summary = result['summary']
                self.update_ui()
                # Also refresh history
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
            if hasattr(self, 'summary_label'):
                self.summary_label.setText(f'No data available: {error}')
        
        self.worker.finished.connect(on_summary_finished)
        self.worker.error.connect(on_summary_error)
        self.worker.start()
    
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
                item_widget.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item_widget)
        
        self.table.resizeColumnsToContents()
    
    def update_charts(self):
        if not self.current_summary:
            return
        
        self.chart_canvas.figure.clear()
        
        try:
            if self.is_dark:
                plt.style.use('dark_background')
            else:
                try:
                    plt.style.use('seaborn-v0_8-whitegrid')
                except:
                    plt.style.use('default')
        except:
            pass
        
        fig = self.chart_canvas.figure
        if self.is_dark:
            fig.patch.set_facecolor('#1e293b')
        else:
            fig.patch.set_facecolor('#ffffff')
        
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        if self.is_dark:
            ax1.set_facecolor('#1e293b')
            ax2.set_facecolor('#1e293b')
            text_color = '#f1f5f9'
        else:
            text_color = '#1e293b'
        
        type_dist = self.current_summary['type_distribution']
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        
        colors = ['#2563eb', '#7c3aed', '#10b981', '#f59e0b', '#ef4444']
        if self.is_dark:
            colors = ['#3b82f6', '#8b5cf6', '#10b981', '#fbbf24', '#f87171']
        
        ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)], startangle=90,
                textprops={'color': text_color, 'fontweight': 'bold'})
        ax1.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20, color=text_color)
        
        stats = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_summary['avg_flowrate'],
            self.current_summary['avg_pressure'],
            self.current_summary['avg_temperature']
        ]
        
        bar_colors = ['#2563eb', '#10b981', '#f59e0b'] if not self.is_dark else ['#3b82f6', '#10b981', '#fbbf24']
        bars = ax2.bar(stats, values, color=bar_colors)
        ax2.set_title('Average Statistics', fontsize=14, fontweight='bold', pad=20, color=text_color)
        ax2.set_ylabel('Value', fontweight='bold', color=text_color)
        ax2.tick_params(colors=text_color)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold', color=text_color)
        
        fig.tight_layout()
        self.chart_canvas.draw()
    
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
                text = f"📦 Dataset #{item['id']} - {date_str}\n"
                text += f"Total: {item['summary']['total_count']} | "
                text += f"Flowrate: {item['summary']['avg_flowrate']:.2f} | "
                text += f"Pressure: {item['summary']['avg_pressure']:.2f} | "
                text += f"Temp: {item['summary']['avg_temperature']:.2f}"
                
                list_item = QListWidgetItem(text)
                list_item.setFont(QFont('Segoe UI', 11))
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
        
        # Select save location
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
        """Helper method to show message box with proper theming"""
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        if self.is_dark:
            msg.setStyleSheet(
                "QMessageBox { background-color: #0f172a; color: #f1f5f9; } "
                "QLabel { color: #f1f5f9; } "
                "QPushButton { color: #f1f5f9; background-color: #1e293b; border-radius: 6px; padding: 6px 16px; }"
            )
        else:
            msg.setStyleSheet(
                "QMessageBox { background-color: #ffffff; color: #1e293b; } "
                "QLabel { color: #1e293b; } "
                "QPushButton { color: #1e293b; }"
            )
        return msg.exec_()
    
    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.settings.setValue('dark_mode', self.is_dark)
        self.theme_btn.setText('☀️' if self.is_dark else '🌙')
        
        # Update title color
        if self.is_dark:
            self.title_label.setStyleSheet('color: #f1f5f9;')
        else:
            self.title_label.setStyleSheet('color: #1e293b;')
        
        self.setup_styles()
        self.update_table_style()
        self.update_charts()
    
    def get_dark_styles(self):
        return """
            QMainWindow {
                background-color: #0f172a;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #f1f5f9;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 500;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #60a5fa, stop:1 #3b82f6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2563eb, stop:1 #1e40af);
            }
            QPushButton#secondary {
                background: #1e293b;
                color: #f1f5f9;
                border: 1px solid #334155;
            }
            QPushButton#secondary:hover {
                background: #334155;
                border-color: #3b82f6;
                color: #60a5fa;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
                border-radius: 12px;
                background: #1e293b;
                padding: 16px;
            }
            QTabBar::tab {
                background: #0f172a;
                color: #94a3b8;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: #1e293b;
                color: #60a5fa;
                border-bottom: 2px solid #3b82f6;
            }
            QTabBar::tab:hover {
                background: #1e293b;
            }
            QTableWidget {
                border: 1px solid #334155;
                border-radius: 8px;
                background: #1e293b;
                gridline-color: #334155;
                color: #f1f5f9;
            }
            QTableWidget::item {
                padding: 8px;
                color: #f1f5f9;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e293b, stop:1 #0f172a);
                color: #f1f5f9;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #334155;
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
            }
            QListWidget {
                border: 1px solid #334155;
                border-radius: 8px;
                background: #1e293b;
                color: #f1f5f9;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 1px solid #334155;
                border-radius: 8px;
                margin: 4px;
                color: #f1f5f9;
            }
            QListWidget::item:hover {
                background: #334155;
            }
            QListWidget::item:selected {
                background: #1e3a8a;
                color: #60a5fa;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 600;
                color: #f1f5f9;
                background: none;
            }
            QFrame#card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 24px;
            }
            QLabel#summary-label {
                font-size: 16px;
                color: #94a3b8;
                padding: 20px;
            }
        """
