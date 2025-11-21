from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
                             QLabel, QTabWidget, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from api_client import APIClient


class MainWindow(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.client = APIClient()
        self.client.set_auth(username, password)
        self.current_summary = None
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()
        self.load_summary()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        header = QHBoxLayout()
        title = QLabel('Chemical Equipment Visualizer')
        title.setStyleSheet('font-size: 20px; font-weight: bold;')
        header.addWidget(title)
        header.addStretch()
        
        upload_btn = QPushButton('Upload CSV')
        upload_btn.clicked.connect(self.upload_csv)
        header.addWidget(upload_btn)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.load_summary)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        tabs = QTabWidget()
        
        summary_tab = self.create_summary_tab()
        tabs.addTab(summary_tab, 'Summary')
        
        table_tab = self.create_table_tab()
        tabs.addTab(table_tab, 'Equipment Table')
        
        charts_tab = self.create_charts_tab()
        tabs.addTab(charts_tab, 'Charts')
        
        history_tab = self.create_history_tab()
        tabs.addTab(history_tab, 'History')
        
        layout.addWidget(tabs)
    
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.summary_label = QLabel('No data available')
        self.summary_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_label)
        
        return widget
    
    def create_table_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        return widget
    
    def create_charts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.chart_canvas = FigureCanvas(Figure(figsize=(10, 6)))
        layout.addWidget(self.chart_canvas)
        
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
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
            self.summary_label.setText(f'No data available: {str(e)}')
    
    def update_ui(self):
        if not self.current_summary:
            return
        
        summary_text = f"""
        Total Equipment: {self.current_summary['total_count']}
        Average Flowrate: {self.current_summary['avg_flowrate']:.2f}
        Average Pressure: {self.current_summary['avg_pressure']:.2f}
        Average Temperature: {self.current_summary['avg_temperature']:.2f}
        """
        self.summary_label.setText(summary_text)
        
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
                self.table.setItem(row, col, QTableWidgetItem(value))
        
        self.table.resizeColumnsToContents()
    
    def update_charts(self):
        if not self.current_summary:
            return
        
        self.chart_canvas.figure.clear()
        
        fig = self.chart_canvas.figure
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        type_dist = self.current_summary['type_distribution']
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        
        ax1.pie(counts, labels=types, autopct='%1.1f%%')
        ax1.set_title('Equipment Type Distribution')
        
        stats = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_summary['avg_flowrate'],
            self.current_summary['avg_pressure'],
            self.current_summary['avg_temperature']
        ]
        
        ax2.bar(stats, values)
        ax2.set_title('Average Statistics')
        ax2.set_ylabel('Value')
        
        fig.tight_layout()
        self.chart_canvas.draw()
    
    def load_history(self):
        try:
            history = self.client.get_history()
            self.history_list.clear()
            
            for item in history:
                date_str = item['uploaded_at'][:19].replace('T', ' ')
                text = f"Dataset #{item['id']} - {date_str}\n"
                text += f"Total: {item['summary']['total_count']} | "
                text += f"Flowrate: {item['summary']['avg_flowrate']:.2f} | "
                text += f"Pressure: {item['summary']['avg_pressure']:.2f} | "
                text += f"Temp: {item['summary']['avg_temperature']:.2f}"
                
                list_item = QListWidgetItem(text)
                self.history_list.addItem(list_item)
        except Exception as e:
            pass

