from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from services.database_service import db_service
from models.inspection_data import UploadStatus
from utils.date_utils import date_utils


class HistoryScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'history'
        self.current_filter = 'all'
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
            text='历史数据',
            font_size=20,
            size_hint_x=0.7,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        top_layout.add_widget(title_label)
        
        layout.add_widget(top_layout)
        
        filter_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        
        all_btn = Button(
            text='全部',
            font_size=16,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        all_btn.bind(on_press=lambda x: self.filter_data('all'))
        filter_layout.add_widget(all_btn)
        
        unuploaded_btn = Button(
            text='未上传',
            font_size=16,
            background_color=(0.9, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        unuploaded_btn.bind(on_press=lambda x: self.filter_data('unuploaded'))
        filter_layout.add_widget(unuploaded_btn)
        
        uploaded_btn = Button(
            text='已上传',
            font_size=16,
            background_color=(0.3, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        uploaded_btn.bind(on_press=lambda x: self.filter_data('uploaded'))
        filter_layout.add_widget(uploaded_btn)
        
        layout.add_widget(filter_layout)
        
        scroll = ScrollView()
        self.data_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.data_layout.bind(minimum_height=self.data_layout.setter('height'))
        scroll.add_widget(self.data_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        self.load_data()
    
    def filter_data(self, filter_type):
        self.current_filter = filter_type
        self.load_data()
    
    def load_data(self):
        self.data_layout.clear_widgets()
        
        if self.current_filter == 'all':
            data_list = db_service.get_all_data()
        elif self.current_filter == 'unuploaded':
            data_list = db_service.get_data_by_status(UploadStatus.NOT_UPLOADED)
        elif self.current_filter == 'uploaded':
            data_list = db_service.get_data_by_status(UploadStatus.UPLOADED)
        else:
            data_list = []
        
        if not data_list:
            empty_label = Label(
                text='暂无数据',
                font_size=18,
                size_hint_y=None,
                height=100,
                color=(0.5, 0.5, 0.5, 1),
                font_name='chinese'
            )
            self.data_layout.add_widget(empty_label)
            return
        
        for data in data_list:
            item_layout = self.create_data_item(data)
            self.data_layout.add_widget(item_layout)
    
    def create_data_item(self, data):
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=5, spacing=3)
        
        with layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=lambda instance, value: setattr(bg_rect, 'size', value))
        layout.bind(pos=lambda instance, value: setattr(bg_rect, 'pos', value))
        
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        
        device_label = Label(
            text=f'{data.device_name} - {data.inspection_type}',
            font_size=16,
            size_hint_x=0.7,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        header_layout.add_widget(device_label)
        
        status_text = '未上传' if data.upload_status == UploadStatus.NOT_UPLOADED else '已上传'
        status_color = (0.9, 0.7, 0.2, 1) if data.upload_status == UploadStatus.NOT_UPLOADED else (0.3, 0.8, 0.4, 1)
        
        status_label = Label(
            text=status_text,
            font_size=14,
            size_hint_x=0.3,
            color=status_color,
            font_name='chinese'
        )
        header_layout.add_widget(status_label)
        
        layout.add_widget(header_layout)
        
        info_text = (
            f'生产线: {data.production_line} | '
            f'数值: {data.measured_value} {data.unit} | '
            f'时间: {date_utils.format_datetime(data.capture_time)}'
        )
        
        info_label = Label(
            text=info_text,
            font_size=14,
            size_hint_y=None,
            height=30,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(info_label)
        
        if data.remark:
            remark_label = Label(
                text=f'备注: {data.remark}',
                font_size=12,
                size_hint_y=None,
                height=25,
                color=(0.5, 0.5, 0.5, 1),
                font_name='chinese'
            )
            layout.add_widget(remark_label)
        
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35, spacing=5)
        
        delete_btn = Button(
            text='删除',
            font_size=14,
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        delete_btn.bind(on_press=lambda x: self.delete_data(data.id))
        action_layout.add_widget(delete_btn)
        
        layout.add_widget(action_layout)
        
        return layout
    
    def delete_data(self, data_id):
        db_service.delete_data(data_id)
        self.load_data()
    
    def go_back(self, instance):
        if self.app_manager:
            self.app_manager.go_to_main()
