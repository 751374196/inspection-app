# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from typing import Dict
import json


@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    db_type: str


class AppConfig:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.images_dir = os.path.join(self.data_dir, 'images')
        self.db_path = os.path.join(self.data_dir, 'app.db')
        self.config_file = os.path.join(self.data_dir, 'config.json')
        
        self._ensure_directories()
        self._load_config()
    
    def _ensure_directories(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
    
    def _load_config(self):
        default_config = {
            'sql_server': {
                'host': 'zjzx.cpicfiber.com',
                'port': 1433,
                'database': 'CPIC_QMI',
                'username': 'sa',
                'password': 'Cpic1234$',
                'db_type': 'sql_server'
            },
            'mysql_server': {
                'host': '10.12.0.130',
                'port': 9030,
                'database': 'cpic_doris',
                'username': 'root',
                'password': 'root',
                'db_type': 'mysql'
            },
            'admin': {
                'username': 'CPIC',
                'password': 'CPIC'
            },
            'ocr': {
                'engine': 'pytesseract',
                'language': 'eng+chi_sim',
                'image_quality': 'high'
            },
            'upload': {
                'auto_upload': True,
                'retry_count': 3,
                'timeout': 30
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception:
                self.config = default_config
                self._save_config()
        else:
            self.config = default_config
            self._save_config()
    
    def _save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_sql_server_config(self) -> DatabaseConfig:
        cfg = self.config['sql_server']
        return DatabaseConfig(
            host=cfg['host'],
            port=cfg['port'],
            database=cfg['database'],
            username=cfg['username'],
            password=cfg['password'],
            db_type=cfg['db_type']
        )
    
    def get_mysql_config(self) -> DatabaseConfig:
        cfg = self.config['mysql_server']
        return DatabaseConfig(
            host=cfg['host'],
            port=cfg['port'],
            database=cfg['database'],
            username=cfg['username'],
            password=cfg['password'],
            db_type=cfg['db_type']
        )
    
    def get_admin_credentials(self) -> tuple:
        return self.config['admin']['username'], self.config['admin']['password']
    
    def get_ocr_config(self) -> Dict:
        return self.config['ocr']
    
    def get_upload_config(self) -> Dict:
        return self.config['upload']
    
    def update_config(self, key: str, value):
        self.config[key] = value
        self._save_config()


app_config = AppConfig()
