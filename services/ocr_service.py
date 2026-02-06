import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
from typing import Optional, Tuple
from config.app_config import app_config


class OCRService:
    def __init__(self):
        self.config = app_config.get_ocr_config()
        self.engine = self.config.get('engine', 'pytesseract')
        self.language = self.config.get('language', 'eng+chi_sim')
    
    def preprocess_image(self, image_path: str) -> Image.Image:
        image = cv2.imread(image_path)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        kernel = np.ones((2, 2), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return Image.fromarray(processed)
    
    def extract_number_with_pytesseract(self, image: Image.Image) -> Optional[float]:
        try:
            text = pytesseract.image_to_string(
                image,
                lang=self.language,
                config='--psm 6 --oem 3'
            )
            
            number = self._extract_number_from_text(text)
            return number
        except Exception as e:
            print(f"Tesseract OCR error: {e}")
            return None
    
    def _extract_number_from_text(self, text: str) -> Optional[float]:
        patterns = [
            r'[-+]?\d*\.\d+',
            r'[-+]?\d+\.?\d*',
            r'\d+\.\d+',
            r'\d+'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    return float(matches[0])
                except ValueError:
                    continue
        
        return None
    
    def recognize_value(self, image_path: str) -> Tuple[Optional[float], str]:
        try:
            processed_image = self.preprocess_image(image_path)
            
            if self.engine == 'pytesseract':
                value = self.extract_number_with_pytesseract(processed_image)
                if value is not None:
                    return value, 'pytesseract'
            
            text = pytesseract.image_to_string(
                processed_image,
                lang=self.language,
                config='--psm 6 --oem 3'
            )
            
            value = self._extract_number_from_text(text)
            return value, self.engine
            
        except Exception as e:
            print(f"OCR recognition error: {e}")
            return None, 'error'
    
    def recognize_value_from_pil(self, pil_image: Image.Image) -> Tuple[Optional[float], str]:
        try:
            if self.engine == 'pytesseract':
                value = self.extract_number_with_pytesseract(pil_image)
                if value is not None:
                    return value, 'pytesseract'
            
            text = pytesseract.image_to_string(
                pil_image,
                lang=self.language,
                config='--psm 6 --oem 3'
            )
            
            value = self._extract_number_from_text(text)
            return value, self.engine
            
        except Exception as e:
            print(f"OCR recognition error: {e}")
            return None, 'error'


ocr_service = OCRService()
