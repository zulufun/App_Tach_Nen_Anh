# file: app/view.py
from PySide6.QtWidgets import (QMainWindow, QLabel, QPushButton, 
                              QVBoxLayout, QHBoxLayout, QFileDialog, 
                              QWidget, QMessageBox)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal
from io import BytesIO

class BackgroundRemoverView(QMainWindow):
    # Signals
    load_image_signal = Signal(str)
    process_image_signal = Signal()
    save_image_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Ứng dụng tách nền ảnh')
        self.setGeometry(100, 100, 800, 600)
        
        # Tạo widget chính và layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Layout hiển thị ảnh
        image_layout = QHBoxLayout()
        
        # Layout bên trái - ảnh gốc
        left_layout = QVBoxLayout()
        self.input_label = QLabel('Ảnh gốc')
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_image_label = QLabel()
        self.input_image_label.setAlignment(Qt.AlignCenter)
        self.input_image_label.setMinimumSize(300, 300)
        self.input_image_label.setStyleSheet("border: 1px solid #ccc;")
        left_layout.addWidget(self.input_label)
        left_layout.addWidget(self.input_image_label)
        
        # Layout bên phải - ảnh đã tách nền
        right_layout = QVBoxLayout()
        self.output_label = QLabel('Ảnh đã tách nền')
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_image_label = QLabel()
        self.output_image_label.setAlignment(Qt.AlignCenter)
        self.output_image_label.setMinimumSize(300, 300)
        self.output_image_label.setStyleSheet("border: 1px solid #ccc;")
        right_layout.addWidget(self.output_label)
        right_layout.addWidget(self.output_image_label)
        
        # Thêm layout trái phải vào layout hiển thị ảnh
        image_layout.addLayout(left_layout)
        image_layout.addLayout(right_layout)
        
        # Các nút chức năng
        button_layout = QHBoxLayout()
        
        self.load_button = QPushButton('Tải ảnh')
        self.load_button.clicked.connect(self.on_load_button_clicked)
        
        self.process_button = QPushButton('Tách nền')
        self.process_button.clicked.connect(self.on_process_button_clicked)
        self.process_button.setEnabled(False)
        
        self.save_button = QPushButton('Lưu ảnh')
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.save_button.setEnabled(False)
        
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        
        # Thêm các layout vào layout chính
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def on_load_button_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Chọn ảnh', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if file_path:
            self.load_image_signal.emit(file_path)
    
    def on_process_button_clicked(self):
        self.process_image_signal.emit()
    
    def on_save_button_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Lưu ảnh', '', 'PNG Files (*.png)')
        if file_path:
            self.save_image_signal.emit(file_path)
    
    def display_input_image(self, image):
        """Hiển thị ảnh đầu vào lên giao diện"""
        if isinstance(image, str):  # Nếu là đường dẫn file
            pixmap = QPixmap(image)
        else:  # Nếu là ảnh PIL
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            img = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(img)
        
        # Thay đổi kích thước ảnh nếu quá lớn
        if pixmap.width() > 300 or pixmap.height() > 300:
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.input_image_label.setPixmap(pixmap)
        self.process_button.setEnabled(True)
    
    def display_output_image(self, image):
        """Hiển thị ảnh đầu ra lên giao diện"""
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        
        img = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(img)
        
        # Thay đổi kích thước ảnh nếu quá lớn
        if pixmap.width() > 300 or pixmap.height() > 300:
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.output_image_label.setPixmap(pixmap)
        self.save_button.setEnabled(True)
    
    def show_error(self, title, message):
        """Hiển thị thông báo lỗi"""
        QMessageBox.critical(self, title, message)
    
    def show_info(self, title, message):
        """Hiển thị thông báo thành công"""
        QMessageBox.information(self, title, message)
    
    def reset_output_view(self):
        """Xóa ảnh đầu ra và vô hiệu hóa nút lưu"""
        self.output_image_label.clear()
        self.save_button.setEnabled(False)
