from typing import Optional, Callable
from models.device_info import DeviceInfo
import cv2
import numpy as np
from PIL import Image


class QRScanner:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()
    
    def scan_from_image(self, image_path: str) -> Optional[DeviceInfo]:
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            decoded_text, points, _ = self.detector.detectAndDecode(image)
            
            if decoded_text:
                device_info = DeviceInfo.from_json(decoded_text)
                return device_info
            
            return None
        except Exception as e:
            print(f"QR scan error: {e}")
            return None
    
    def scan_from_frame(self, frame: np.ndarray) -> Optional[DeviceInfo]:
        try:
            decoded_text, points, _ = self.detector.detectAndDecode(frame)
            
            if decoded_text:
                device_info = DeviceInfo.from_json(decoded_text)
                return device_info
            
            return None
        except Exception as e:
            print(f"QR scan error: {e}")
            return None
    
    def scan_from_pil_image(self, pil_image: Image) -> Optional[DeviceInfo]:
        try:
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return self.scan_from_frame(opencv_image)
        except Exception as e:
            print(f"QR scan error: {e}")
            return None


qr_scanner = QRScanner()
