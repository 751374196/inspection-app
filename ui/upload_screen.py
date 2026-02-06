from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from services.database_service import db_service
from services.network_service import network_service
from services.upload_service import upload_service
from models.inspection_data import UploadStatus


class UploadScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'upload'
        self.uploading = False
        self.build_ui()
        Clock.schedule_once(self.update_status, 0.5)
    
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
            text='数据上传',
            font_size=20,
            size_hint_x=0.7,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        top_layout.add_widget(title_label)
        
        layout.add_widget(top_layout)
        
        self.network_label = Label(
            text='网络状态: 检测中...',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.network_label)
        
        self.count_label = Label(
            text='待上传数据: 0条',
            font_size=18,
            size_hint_y=None,
            height=50,
            color=(0.8, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.count_label)
        
        self.progress_label = Label(
            text='',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(self.progress_label)
        
        self.upload_btn = Button(
            text='⬆️ 开始上传',
            font_size=24,
            size_hint_y=None,
            height=80,
            background_color=(0.3, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        self.upload_btn.bind(on_press=self.start_upload)
        layout.add_widget(self.upload_btn)
        
        log_label = Label(
            text='上传日志:',
            font_size=16,
            size_hint_y=None,
            height=30,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(log_label)
        
        scroll = ScrollView()
        self.log_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        scroll.add_widget(self.log_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        self.update_status()
        self.update_count()
    
    def update_status(self, dt=None):
        status = network_service.get_network_status()
        if status['can_upload']:
            self.network_label.text = '网络状态: 已连接 ✓'
            self.network_label.color = (0.2, 0.8, 0.3, 1)
        else:
            self.network_label.text = '网络状态: 未连接 ✗'
            self.network_label.color = (0.8, 0.3, 0.3, 1)
    
    def update_count(self):
        count = db_service.get_unuploaded_count()
        self.count_label.text = f'待上传数据: {count}条'
        if count > 0:
            self.count_label.color = (0.8, 0.3, 0.3, 1)
            if not self.uploading:
                self.upload_btn.disabled = False
        else:
            self.count_label.text = '所有数据已上传'
            self.count_label.color = (0.2, 0.8, 0.3, 1)
            self.upload_btn.disabled = True
    
    def start_upload(self, instance):
        if self.uploading:
            return
        
        if not upload_service.can_upload():
            self.progress_label.text = '网络未连接，无法上传'
            self.progress_label.color = (0.8, 0.3, 0.3, 1)
            return
        
        self.uploading = True
        self.upload_btn.disabled = True
        self.upload_btn.text = '上传中...'
        self.log_layout.clear_widgets()
        
        success_count, failed_count, logs = upload_service.upload_all_unuploaded(
            progress_callback=self.update_progress
        )
        
        self.show_upload_result(success_count, failed_count, logs)
    
    def update_progress(self, current, total, message):
        self.progress_label.text = f'进度: {current}/{total} - {message}'
        self.progress_label.color = (0.2, 0.4, 0.8, 1)
    
    def show_upload_result(self, success_count, failed_count, logs):
        self.uploading = False
        self.upload_btn.text = '⬆️ 开始上传'
        
        result_text = f'上传完成: 成功 {success_count} 条, 失败 {failed_count} 条'
        self.progress_label.text = result_text
        
        if failed_count == 0:
            self.progress_label.color = (0.2, 0.8, 0.3, 1)
        else:
            self.progress_label.color = (0.8, 0.3, 0.3, 1)
        
        for log in logs:
            log_label = Label(
                text=log,
                font_size=14,
                size_hint_y=None,
                height=30,
                color=(0.3, 0.3, 0.3, 1),
                font_name='chinese'
            )
            self.log_layout.add_widget(log_label)
        
        self.update_count()
    
    def go_back(self, instance):
        if self.app_manager:
            self.app_manager.go_to_main()
