# file: main.py
import sys
from PySide6.QtWidgets import QApplication
from app.controller import BackgroundRemoverController
from app.view import BackgroundRemoverView
from app.model import BackgroundRemoverModel

def main():
    app = QApplication(sys.argv)
    
    # Khởi tạo model, view và controller
    model = BackgroundRemoverModel()
    view = BackgroundRemoverView()
    controller = BackgroundRemoverController(model, view)
    
    # Hiển thị cửa sổ ứng dụng
    view.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
