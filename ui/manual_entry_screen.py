# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.core.camera import Camera
from PIL import Image as PILImage
import numpy as np
import cv2
from models.device_info import DeviceInfo
from services.ocr_service import ocr_service
from utils.image_utils import image_utils


class ManualEntryScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'manual_entry'
        self.camera = None
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
        
        title_label = Label(
            text='手动录入设备信息',
            font_size=20,
            size_hint_x=0.7,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        top_layout.add_widget(title_label)
        
        layout.add_widget(top_layout)
        
        self.camera_layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.camera_layout)
        
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        
        self.production_line_input = TextInput(
            hint_text='生产线',
            font_size=16,
            size_hint_y=None,
            height=50,
            multiline=False,
            font_name='chinese'
        )
        form_layout.add_widget(Label(text='生产线:', font_size=14, size_hint_y=None, height=30, font_name='chinese'))
        form_layout.add_widget(self.production_line_input)
        
        self.device_name_input = TextInput(
            hint_text='设备名称',
            font_size=16,
            size_hint_y=None,
            height=50,
            multiline=False,
            font_name='chinese'
        )
        form_layout.add_widget(Label(text='设备名称:', font_size=14, size_hint_y=None, height=30, font_name='chinese'))
        form_layout.add_widget(self.device_name_input)
        
        self.inspection_type_input = TextInput(
            hint_text='检测类型',
            font_size=16,
            size_hint_y=None,
            height=50,
            multiline=False,
            font_name='chinese'
        )
        form_layout.add_widget(Label(text='检测类型:', font_size=14, size_hint_y=None, height=30, font_name='chinese'))
        form_layout.add_widget(self.inspection_type_input)
        
        self.unit_input = TextInput(
            hint_text='数据单位',
            font_size=16,
            size_hint_y=None,
            height=50,
            multiline=False,
            font_name='chinese'
        )
        form_layout.add_widget(Label(text='数据单位:', font_size=14, size_hint_y=None, height=30, font_name='chinese'))
        form_layout.add_widget(self.unit_input)
        
        layout.add_widget(form_layout)
        
        self.info_label = Label(
            text='请填写设备信息，然后拍照识别数值',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.info_label)
        
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        self.capture_btn = Button(
            text='📸 拍照识别',
            font_size=18,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        self.capture_btn.bind(on_press=self.capture_and_recognize)
        action_layout.add_widget(self.capture_btn)
        
        layout.add_widget(action_layout)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        pass
    
    def on_leave(self):
        if self.camera:
            self.camera.play = False
            self.camera_layout.clear_widgets()
            self.camera = None
    
    def capture_and_recognize(self, instance):
        if not self._validate_inputs():
            self.info_label.text = '请填写所有必填字段'
            return
        
        try:
            self.camera = Camera(resolution=(640, 480), play=True)
            self.camera_layout.clear_widgets()
            self.camera_layout.add_widget(self.camera)
            
            Clock.schedule_once(self._capture_delayed, 1)
        except Exception as e:
            self.info_label.text = f'拍照失败: {str(e)}'
    
    def _validate_inputs(self):
        return (
            self.production_line_input.text.strip() and
            self.device_name_input.text.strip() and
            self.inspection_type_input.text.strip() and
            self.unit_input.text.strip()
        )
    
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
                
                if self.camera:
                    self.camera.play = False
                    self.camera_layout.clear_widgets()
                    self.camera = None
                
                self.go_to_data_entry()
        except Exception as e:
            self.info_label.text = f'拍照失败: {str(e)}'
    
    def go_to_data_entry(self):
        if self.app_manager and self.current_image_path:
            device_info = DeviceInfo(
                device_id='manual',
                device_name=self.device_name_input.text.strip(),
                production_line=self.production_line_input.text.strip(),
                inspection_type=self.inspection_type_input.text.strip(),
                unit=self.unit_input.text.strip()
            )
            self.app_manager.go_to_data_entry(device_info, self.current_image_path)
    
    def go_back(self, instance):
        if self.app_manager:
            self.app_manager.go_to_main()
