# file: app/model.py
from PIL import Image
from rembg import remove

class BackgroundRemoverModel:
    def __init__(self):
        self.input_image = None
        self.output_image = None
        
    def load_image(self, file_path):
        """Tải ảnh từ đường dẫn"""
        self.input_image = Image.open(file_path)
        return self.input_image
        
    def remove_background(self):
        """Tách nền ảnh sử dụng rembg"""
        if self.input_image is None:
            return None
            
        self.output_image = remove(self.input_image)
        return self.output_image
        
    def save_image(self, file_path):
        """Lưu ảnh đã tách nền"""
        if self.output_image is None:
            return False
            
        # Đảm bảo file có đuôi .png
        if not file_path.endswith('.png'):
            file_path += '.png'
        
        self.output_image.save(file_path, 'PNG')
        return True