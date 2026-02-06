# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.clock import Clock
import os
from datetime import datetime
from ui.main_screen import MainScreen
from ui.scan_screen import ScanScreen
from ui.manual_entry_screen import ManualEntryScreen
from ui.data_entry_screen import DataEntryScreen
from ui.upload_screen import UploadScreen
from ui.history_screen import HistoryScreen
from ui.settings_screen import SettingsScreen
from services.database_service import db_service

# 注册微软雅黑字体以支持中文显示
def register_chinese_font():
    try:
        # Windows 系统下微软雅黑字体路径
        font_paths = [
            r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
            r'C:\Windows\Fonts\msyh.ttf',  # 微软雅黑
            r'C:\Windows\Fonts\simsun.ttc', # 宋字（备用）
            r'C:\Windows\Fonts\simhei.ttf', # 黑体（备用）
        ]
        
        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            LabelBase.register(name='chinese', fn_regular=font_path)
            print(f'成功注册中文字体: {font_path}')
        else:
            print('警告: 未找到中文字体，中文可能无法正常显示')
    except Exception as e:
        print(f'注册中文字体时出错: {e}')


class AppManager:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
    
    def go_to_main(self):
        self.screen_manager.current = 'main'
    
    def go_to_scan(self):
        self.screen_manager.current = 'scan'
    
    def go_to_manual_entry(self):
        self.screen_manager.current = 'manual_entry'
    
    def go_to_data_entry(self, device_info, image_path):
        data_entry_screen = self.screen_manager.get_screen('data_entry')
        data_entry_screen.set_data(device_info, image_path)
        self.screen_manager.current = 'data_entry'
    
    def go_to_upload(self):
        self.screen_manager.current = 'upload'
    
    def go_to_history(self):
        self.screen_manager.current = 'history'
    
    def go_to_settings(self):
        self.screen_manager.current = 'settings'


class InspectionApp(App):
    def build(self):
        # 设置应用图标
        self.icon = 'assets/icon.png'
        
        # 注册中文字体
        register_chinese_font()
        
        sm = ScreenManager()
        
        app_manager = AppManager(sm)
        
        main_screen = MainScreen(app_manager=app_manager)
        scan_screen = ScanScreen(app_manager=app_manager)
        manual_entry_screen = ManualEntryScreen(app_manager=app_manager)
        data_entry_screen = DataEntryScreen(app_manager=app_manager)
        upload_screen = UploadScreen(app_manager=app_manager)
        history_screen = HistoryScreen(app_manager=app_manager)
        settings_screen = SettingsScreen(app_manager=app_manager)
        
        sm.add_widget(main_screen)
        sm.add_widget(scan_screen)
        sm.add_widget(manual_entry_screen)
        sm.add_widget(data_entry_screen)
        sm.add_widget(upload_screen)
        sm.add_widget(history_screen)
        sm.add_widget(settings_screen)
        
        # 启动定时清理任务，每天执行一次
        Clock.schedule_interval(self.cleanup_old_data, 86400)  # 86400秒 = 24小时
        
        # 应用启动时立即执行一次清理
        Clock.schedule_once(self.cleanup_old_data, 60)  # 60秒后执行
        
        return sm
    
    def cleanup_old_data(self, dt):
        try:
            deleted_count = db_service.cleanup_old_data(days=7)
            if deleted_count > 0:
                print(f'已清理 {deleted_count} 条7天前的已上传数据')
        except Exception as e:
            print(f'清理旧数据时出错: {e}')


if __name__ == '__main__':
    InspectionApp().run()
