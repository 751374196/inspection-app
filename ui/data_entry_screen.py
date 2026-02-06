from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage
from datetime import datetime
from models.device_info import DeviceInfo
from models.inspection_data import InspectionData, UploadStatus
from services.database_service import db_service
from services.ocr_service import ocr_service
from utils.image_utils import image_utils


class DataEntryScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'data_entry'
        self.device_info = None
        self.image_path = None
        self.recognized_value = None
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
        
        confirm_btn = Button(
            text='✅ 确认保存',
            font_size=18,
            size_hint_x=0.7,
            background_color=(0.3, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        confirm_btn.bind(on_press=self.save_data)
        top_layout.add_widget(confirm_btn)
        
        layout.add_widget(top_layout)
        
        self.device_info_label = Label(
            text='',
            font_size=16,
            size_hint_y=None,
            height=100,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        layout.add_widget(self.device_info_label)
        
        self.image_widget = KivyImage(
            size_hint_y=None,
            height=300,
            allow_stretch=True
        )
        layout.add_widget(self.image_widget)
        
        value_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        value_label = Label(
            text='测量数值:',
            font_size=18,
            size_hint_x=0.3,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        value_layout.add_widget(value_label)
        
        self.value_input = TextInput(
            text='',
            font_size=20,
            size_hint_x=0.7,
            multiline=False,
            input_filter='float',
            font_name='chinese'
        )
        value_layout.add_widget(self.value_input)
        
        layout.add_widget(value_layout)
        
        remark_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        remark_label = Label(
            text='备注:',
            font_size=18,
            size_hint_x=0.2,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        remark_layout.add_widget(remark_label)
        
        self.remark_input = TextInput(
            text='',
            font_size=16,
            size_hint_x=0.8,
            multiline=False,
            font_name='chinese'
        )
        remark_layout.add_widget(self.remark_input)
        
        layout.add_widget(remark_layout)
        
        self.status_label = Label(
            text='',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def set_data(self, device_info: DeviceInfo, image_path: str):
        self.device_info = device_info
        self.image_path = image_path
        
        info_text = (
            f'生产线: {device_info.production_line}\n'
            f'设备: {device_info.device_name}\n'
            f'检测类型: {device_info.inspection_type}\n'
            f'数据单位: {device_info.unit}'
        )
        self.device_info_label.text = info_text
        self.unit_label.text = device_info.unit
        
        try:
            self.image_widget.source = image_path
            self.image_widget.reload()
        except Exception:
            pass
        
        self.status_label.text = '正在识别数值...'
        
        value, engine = ocr_service.recognize_value(image_path)
        self.recognized_value = value
        
        if value is not None:
            self.value_input.text = str(value)
            self.status_label.text = f'识别成功 (使用{engine})'
            self.status_label.color = (0.2, 0.8, 0.3, 1)
        else:
            self.status_label.text = '识别失败，请手动输入'
            self.status_label.color = (0.8, 0.3, 0.3, 1)
    
    def save_data(self, instance):
        if not self.device_info or not self.image_path:
            self.status_label.text = '数据不完整'
            return
        
        value_str = self.value_input.text.strip()
        if not value_str:
            self.status_label.text = '请输入测量数值'
            self.status_label.color = (0.8, 0.3, 0.3, 1)
            return
        
        try:
            measured_value = float(value_str)
        except ValueError:
            self.status_label.text = '数值格式错误'
            self.status_label.color = (0.8, 0.3, 0.3, 1)
            return
        
        remark = self.remark_input.text.strip()
        
        inspection_data = InspectionData(
            id=None,
            device_id=self.device_info.device_id,
            device_name=self.device_info.device_name,
            production_line=self.device_info.production_line,
            inspection_type=self.device_info.inspection_type,
            unit=self.device_info.unit,
            measured_value=measured_value,
            image_path=self.image_path,
            remark=remark,
            capture_time=datetime.now(),
            upload_status=UploadStatus.NOT_UPLOADED,
            upload_time=None
        )
        
        try:
            record_id = db_service.save_inspection_data(inspection_data)
            self.status_label.text = f'保存成功 (ID: {record_id})'
            self.status_label.color = (0.2, 0.8, 0.3, 1)
            
            from kivy.clock import Clock
            Clock.schedule_once(self._go_back_delayed, 1)
        except Exception as e:
            self.status_label.text = f'保存失败: {str(e)}'
            self.status_label.color = (0.8, 0.3, 0.3, 1)
    
    def _go_back_delayed(self, dt):
        self.go_back(None)
    
    def go_back(self, instance):
        if self.app_manager:
            self.app_manager.go_to_main()
