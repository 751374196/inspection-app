from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.camera import Camera
from PIL import Image as PILImage
import numpy as np
import cv2
from models.device_info import DeviceInfo
from services.qr_scanner import qr_scanner
from services.ocr_service import ocr_service
from utils.image_utils import image_utils


class ScanScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'scan'
        self.scanning = False
        self.camera = None
        self.current_device_info = None
        self.current_image = None
        self.current_image_path = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        
        back_btn = Button(
            text='🔙 返回',
            font_size=18,
            size_hint_x=0.3,
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        back_btn.bind(on_press=self.go_back)
        top_layout.add_widget(back_btn)
        
        self.mode_label = Label(
            text='扫描二维码',
            font_size=20,
            size_hint_x=0.7,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        top_layout.add_widget(self.mode_label)
        
        layout.add_widget(top_layout)
        
        self.camera_layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.camera_layout)
        
        self.info_label = Label(
            text='将设备二维码对准相机',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.info_label)
        
        self.device_info_label = Label(
            text='',
            font_size=14,
            size_hint_y=None,
            height=80,
            color=(0.2, 0.6, 0.2, 1),
            font_name='chinese'
        )
        layout.add_widget(self.device_info_label)
        
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        self.capture_btn = Button(
            text='📸 拍照识别',
            font_size=18,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            disabled=True,
            font_name='chinese'
        )
        self.capture_btn.bind(on_press=self.capture_and_recognize)
        action_layout.add_widget(self.capture_btn)
        
        self.rescan_btn = Button(
            text='🔄 重新扫描',
            font_size=18,
            background_color=(0.9, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            disabled=True,
            font_name='chinese'
        )
        self.rescan_btn.bind(on_press=self.rescan_qr)
        action_layout.add_widget(self.rescan_btn)
        
        layout.add_widget(action_layout)
        
        manual_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        manual_btn = Button(
            text='✏️ 手动录入',
            font_size=18,
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        manual_btn.bind(on_press=self.go_to_manual_entry)
        manual_layout.add_widget(manual_btn)
        
        layout.add_widget(manual_layout)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        self.start_camera()
    
    def on_leave(self):
        self.stop_camera()
    
    def start_camera(self):
        try:
            self.camera = Camera(resolution=(640, 480), play=True)
            self.camera_layout.clear_widgets()
            self.camera_layout.add_widget(self.camera)
            self.scanning = True
            Clock.schedule_interval(self.scan_qr_code, 0.5)
        except Exception as e:
            self.info_label.text = f'相机启动失败: {str(e)}'
    
    def stop_camera(self):
        if self.camera:
            self.camera.play = False
            self.camera_layout.clear_widgets()
            self.camera = None
        self.scanning = False
        Clock.unschedule(self.scan_qr_code)
    
    def scan_qr_code(self, dt):
        if not self.scanning or not self.camera:
            return
        
        try:
            texture = self.camera.texture
            if texture:
                pixels = texture.pixels
                image_array = np.frombuffer(pixels, dtype=np.uint8)
                image_array = image_array.reshape(texture.height, texture.width, 4)
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
                
                device_info = qr_scanner.scan_from_frame(image_array)
                
                if device_info:
                    self.current_device_info = device_info
                    self.stop_camera()
                    self.show_device_info()
        except Exception:
            pass
    
    def show_device_info(self):
        if self.current_device_info:
            info_text = (
                f'生产线: {self.current_device_info.production_line}\n'
                f'设备: {self.current_device_info.device_name}\n'
                f'检测类型: {self.current_device_info.inspection_type}\n'
                f'数据单位: {self.current_device_info.unit}'
            )
            self.device_info_label.text = info_text
            self.info_label.text = '二维码识别成功，请拍照识别数值'
            self.capture_btn.disabled = False
            self.rescan_btn.disabled = False
    
    def capture_and_recognize(self, instance):
        try:
            self.camera = Camera(resolution=(640, 480), play=True)
            self.camera_layout.clear_widgets()
            self.camera_layout.add_widget(self.camera)
            
            Clock.schedule_once(self._capture_delayed, 1)
        except Exception as e:
            self.info_label.text = f'拍照失败: {str(e)}'
    
    def _capture_delayed(self, dt):
        try:
            if self.camera and self.camera.texture:
                texture = self.camera.texture
                pixels = texture.pixels
                image_array = np.frombuffer(pixels, dtype=np.uint8)
                image_array = image_array.reshape(texture.height, texture.width, 4)
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
                
                pil_image = PILImage.fromarray(image_array)
                self.current_image_path = image_utils.save_image(pil_image, 'capture')
                self.current_image = pil_image
                
                self.stop_camera()
                self.go_to_data_entry()
        except Exception as e:
            self.info_label.text = f'拍照失败: {str(e)}'
    
    def rescan_qr(self, instance):
        self.current_device_info = None
        self.current_image = None
        self.current_image_path = None
        self.device_info_label.text = ''
        self.info_label.text = '将设备二维码对准相机'
        self.capture_btn.disabled = True
        self.rescan_btn.disabled = True
        self.start_camera()
    
    def go_to_data_entry(self):
        if self.app_manager and self.current_device_info and self.current_image_path:
            self.app_manager.go_to_data_entry(
                self.current_device_info,
                self.current_image_path
            )
    
    def go_to_manual_entry(self, instance):
        if self.app_manager:
            self.app_manager.go_to_manual_entry()
    
    def go_back(self, instance):
        if self.app_manager:
            self.app_manager.go_to_main()
