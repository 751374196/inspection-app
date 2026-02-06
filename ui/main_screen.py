from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from services.database_service import db_service
from services.network_service import network_service
from services.upload_service import upload_service
from models.inspection_data import UploadStatus


class MainScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'main'
        self.build_ui()
        Clock.schedule_interval(self.update_status, 2)
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        title_label = Label(
            text='检测设备采数APP',
            font_size=32,
            size_hint_y=None,
            height=60,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        layout.add_widget(title_label)
        
        self.status_label = Label(
            text='网络状态: 检测中...',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.status_label)
        
        self.unuploaded_label = Label(
            text='待上传数据: 0条',
            font_size=18,
            size_hint_y=None,
            height=50,
            color=(0.8, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.unuploaded_label)
        
        scan_btn = Button(
            text='📷 扫描二维码',
            font_size=24,
            size_hint_y=None,
            height=80,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        scan_btn.bind(on_press=self.go_to_scan)
        layout.add_widget(scan_btn)
        
        upload_btn = Button(
            text='⬆️ 上传数据',
            font_size=24,
            size_hint_y=None,
            height=80,
            background_color=(0.3, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        upload_btn.bind(on_press=self.go_to_upload)
        layout.add_widget(upload_btn)
        
        history_btn = Button(
            text='📋 查看历史数据',
            font_size=20,
            size_hint_y=None,
            height=70,
            background_color=(0.9, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        history_btn.bind(on_press=self.go_to_history)
        layout.add_widget(history_btn)
        
        settings_btn = Button(
            text='⚙️ 设置',
            font_size=20,
            size_hint_y=None,
            height=70,
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        settings_btn.bind(on_press=self.go_to_settings)
        layout.add_widget(settings_btn)
        
        self.add_widget(layout)
        self.update_unuploaded_count()
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_status(self, dt):
        status = network_service.get_network_status()
        if status['can_upload']:
            self.status_label.text = '网络状态: 已连接 ✓'
            self.status_label.color = (0.2, 0.8, 0.3, 1)
        else:
            self.status_label.text = '网络状态: 未连接 ✗'
            self.status_label.color = (0.8, 0.3, 0.3, 1)
    
    def update_unuploaded_count(self):
        count = db_service.get_unuploaded_count()
        self.unuploaded_label.text = f'待上传数据: {count}条'
        if count > 0:
            self.unuploaded_label.color = (0.8, 0.3, 0.3, 1)
        else:
            self.unuploaded_label.color = (0.3, 0.8, 0.3, 1)
    
    def go_to_scan(self, instance):
        if self.app_manager:
            self.app_manager.go_to_scan()
    
    def go_to_upload(self, instance):
        if self.app_manager:
            self.app_manager.go_to_upload()
    
    def go_to_history(self, instance):
        if self.app_manager:
            self.app_manager.go_to_history()
    
    def go_to_settings(self, instance):
        if self.app_manager:
            self.app_manager.go_to_settings()
    
    def on_enter(self):
        self.update_unuploaded_count()
