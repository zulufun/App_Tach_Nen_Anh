# file: app/controller.py
class BackgroundRemoverController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Kết nối signals từ view đến controller
        self.view.load_image_signal.connect(self.load_image)
        self.view.process_image_signal.connect(self.remove_background)
        self.view.save_image_signal.connect(self.save_image)
    
    def load_image(self, file_path):
        """Xử lý sự kiện tải ảnh"""
        try:
            image = self.model.load_image(file_path)
            self.view.display_input_image(image)
            self.view.reset_output_view()
        except Exception as e:
            self.view.show_error('Lỗi', f'Không thể tải ảnh: {str(e)}')
    
    def remove_background(self):
        """Xử lý sự kiện tách nền"""
        try:
            output_image = self.model.remove_background()
            if output_image:
                self.view.display_output_image(output_image)
        except Exception as e:
            self.view.show_error('Lỗi', f'Lỗi khi tách nền: {str(e)}')
    
    def save_image(self, file_path):
        """Xử lý sự kiện lưu ảnh"""
        try:
            success = self.model.save_image(file_path)
            if success:
                self.view.show_info('Thành công', 'Đã lưu ảnh thành công!')
        except Exception as e:
            self.view.show_error('Lỗi', f'Không thể lưu ảnh: {str(e)}')