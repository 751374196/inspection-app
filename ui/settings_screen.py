from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from config.app_config import app_config


class SettingsScreen(Screen):
    def __init__(self, app_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.name = 'settings'
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
            text='设置',
            font_size=20,
            size_hint_x=0.7,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        top_layout.add_widget(title_label)
        
        layout.add_widget(top_layout)
        
        sql_config = app_config.get_sql_server_config()
        
        sql_label = Label(
            text='SQL Server 配置',
            font_size=18,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        layout.add_widget(sql_label)
        
        self.sql_host_input = self.create_input_field('主机地址', sql_config.host)
        layout.add_widget(self.sql_host_input)
        
        self.sql_db_input = self.create_input_field('数据库名', sql_config.database)
        layout.add_widget(self.sql_db_input)
        
        self.sql_user_input = self.create_input_field('用户名', sql_config.username)
        layout.add_widget(self.sql_user_input)
        
        self.sql_pass_input = self.create_input_field('密码', sql_config.password, password=True)
        layout.add_widget(self.sql_pass_input)
        
        mysql_config = app_config.get_mysql_config()
        
        mysql_label = Label(
            text='MySQL 配置',
            font_size=18,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1),
            font_name='chinese'
        )
        layout.add_widget(mysql_label)
        
        self.mysql_host_input = self.create_input_field('主机地址', mysql_config.host)
        layout.add_widget(self.mysql_host_input)
        
        self.mysql_db_input = self.create_input_field('数据库名', mysql_config.database)
        layout.add_widget(self.mysql_db_input)
        
        self.mysql_user_input = self.create_input_field('用户名', mysql_config.username)
        layout.add_widget(self.mysql_user_input)
        
        self.mysql_pass_input = self.create_input_field('密码', mysql_config.password, password=True)
        layout.add_widget(self.mysql_pass_input)
        
        save_btn = Button(
            text='💾 保存配置',
            font_size=20,
            size_hint_y=None,
            height=60,
            background_color=(0.3, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        save_btn.bind(on_press=self.save_config)
        layout.add_widget(save_btn)
        
        test_btn = Button(
            text='🔍 测试连接',
            font_size=20,
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        test_btn.bind(on_press=self.test_connection)
        layout.add_widget(test_btn)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def create_input_field(self, label_text, default_value, password=False):
        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        label = Label(
            text=label_text,
            font_size=16,
            size_hint_x=0.3,
            color=(0.3, 0.3, 0.3, 1),
            font_name='chinese'
        )
        layout.add_widget(label)
        
        text_input = TextInput(
            text=default_value,
            font_size=16,
            size_hint_x=0.7,
            multiline=False,
            password=password,
            font_name='chinese'
        )
        layout.add_widget(text_input)
        
        return layout
    
    def save_config(self, instance):
        try:
            sql_host = self.sql_host_input.children[0].text
            sql_db = self.sql_db_input.children[0].text
            sql_user = self.sql_user_input.children[0].text
            sql_pass = self.sql_pass_input.children[0].text
            
            mysql_host = self.mysql_host_input.children[0].text
            mysql_db = self.mysql_db_input.children[0].text
            mysql_user = self.mysql_user_input.children[0].text
            mysql_pass = self.mysql_pass_input.children[0].text
            
            app_config.config['sql_server']['host'] = sql_host
            app_config.config['sql_server']['database'] = sql_db
            app_config.config['sql_server']['username'] = sql_user
            app_config.config['sql_server']['password'] = sql_pass
            
            app_config.config['mysql_server']['host'] = mysql_host
            app_config.config['mysql_server']['database'] = mysql_db
            app_config.config['mysql_server']['username'] = mysql_user
            app_config.config['mysql_server']['password'] = mysql_pass
            
            app_config._save_config()
            
            self.show_popup('保存成功', '配置已保存')
        except Exception as e:
            self.show_popup('保存失败', str(e))
    
    def test_connection(self, instance):
        from services.network_service import network_service
        
        sql_ok, sql_msg = network_service.check_sql_server_connection()
        mysql_ok, mysql_msg = network_service.check_mysql_connection()
        
        message = f'SQL Server: {sql_msg}\nMySQL: {mysql_msg}'
        self.show_popup('连接测试结果', message)
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text=message,
            font_size=16,
            size_hint_y=None,
            height=100,
            font_name='chinese'
        )
        content.add_widget(label)
        
        close_btn = Button(
            text='关闭',
            font_size=16,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name='chinese'
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        if self.app_manager:
            self.app_manager.go_to_main()
