import os
from datetime import datetime
from PIL import Image
from config.app_config import app_config


class ImageUtils:
    @staticmethod
    def save_image(pil_image: Image.Image, prefix: str = 'capture') -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"{prefix}_{timestamp}.jpg"
        filepath = os.path.join(app_config.images_dir, filename)
        
        pil_image.save(filepath, 'JPEG', quality=95)
        return filepath
    
    @staticmethod
    def load_image(image_path: str) -> Image.Image:
        return Image.open(image_path)
    
    @staticmethod
    def delete_image(image_path: str) -> bool:
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def resize_image(image: Image.Image, max_size: tuple = (800, 800)) -> Image.Image:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image


image_utils = ImageUtils()
