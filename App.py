import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, QMessageBox)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import numpy as np
from PIL import Image
from rembg import remove
from io import BytesIO

class BackgroundRemoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_image = None
        self.output_image = None
        
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
        self.load_button.clicked.connect(self.load_image)
        
        self.process_button = QPushButton('Tách nền')
        self.process_button.clicked.connect(self.remove_background)
        self.process_button.setEnabled(False)
        
        self.save_button = QPushButton('Lưu ảnh')
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        
        # Thêm các layout vào layout chính
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Chọn ảnh', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        
        if file_path:
            try:
                # Lưu đường dẫn ảnh để xử lý sau này
                self.input_image_path = file_path
                
                # Hiển thị ảnh
                pixmap = QPixmap(file_path)
                
                # Thay đổi kích thước ảnh nếu quá lớn
                if pixmap.width() > 300 or pixmap.height() > 300:
                    pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                self.input_image_label.setPixmap(pixmap)
                
                # Lưu ảnh numpy để xử lý
                self.input_image = Image.open(file_path)
                
                # Kích hoạt nút xử lý
                self.process_button.setEnabled(True)
                
                # Reset ảnh đầu ra
                self.output_image_label.clear()
                self.save_button.setEnabled(False)
                
            except Exception as e:
                QMessageBox.critical(self, 'Lỗi', f'Không thể tải ảnh: {str(e)}')
    
    def remove_background(self):
        if self.input_image is None:
            return
            
        try:
            # Xử lý ảnh với rembg
            output = remove(self.input_image)
            self.output_image = output
            
            # Chuyển đổi ảnh PIL thành QPixmap để hiển thị
            buffer = BytesIO()
            output.save(buffer, format='PNG')
            buffer.seek(0)
            
            img = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(img)
            
            # Thay đổi kích thước ảnh nếu quá lớn
            if pixmap.width() > 300 or pixmap.height() > 300:
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
            # Hiển thị ảnh đã xử lý
            self.output_image_label.setPixmap(pixmap)
            
            # Kích hoạt nút lưu
            self.save_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, 'Lỗi', f'Lỗi khi tách nền: {str(e)}')
    
    def save_image(self):
        if self.output_image is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, 'Lưu ảnh', '', 'PNG Files (*.png)')
        
        if file_path:
            try:
                # Đảm bảo file có đuôi .png
                if not file_path.endswith('.png'):
                    file_path += '.png'
                
                # Lưu ảnh
                self.output_image.save(file_path, 'PNG')
                QMessageBox.information(self, 'Thành công', 'Đã lưu ảnh thành công!')
                
            except Exception as e:
                QMessageBox.critical(self, 'Lỗi', f'Không thể lưu ảnh: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BackgroundRemoverApp()
    window.show()
    sys.exit(app.exec())