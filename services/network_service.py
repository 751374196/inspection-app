import socket
import requests
from typing import Tuple, Optional
from config.app_config import app_config


class NetworkService:
    def __init__(self):
        self.sql_server_config = app_config.get_sql_server_config()
        self.mysql_config = app_config.get_mysql_config()
        self.timeout = app_config.get_upload_config().get('timeout', 30)
    
    def check_internet_connection(self) -> bool:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def check_sql_server_connection(self) -> Tuple[bool, str]:
        try:
            import pyodbc
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={self.sql_server_config.host};'
                f'DATABASE={self.sql_server_config.database};'
                f'UID={self.sql_server_config.username};'
                f'PWD={self.sql_server_config.password}'
            )
            
            conn = pyodbc.connect(conn_str, timeout=self.timeout)
            conn.close()
            return True, "SQL Server连接成功"
        except ImportError:
            return False, "pyodbc未安装"
        except Exception as e:
            return False, f"SQL Server连接失败: {str(e)}"
    
    def check_mysql_connection(self) -> Tuple[bool, str]:
        try:
            import pymysql
            conn = pymysql.connect(
                host=self.mysql_config.host,
                port=self.mysql_config.port,
                user=self.mysql_config.username,
                password=self.mysql_config.password,
                database=self.mysql_config.database,
                connect_timeout=self.timeout
            )
            conn.close()
            return True, "MySQL连接成功"
        except ImportError:
            return False, "pymysql未安装"
        except Exception as e:
            return False, f"MySQL连接失败: {str(e)}"
    
    def check_any_database_connection(self) -> Tuple[bool, str, str]:
        sql_ok, sql_msg = self.check_sql_server_connection()
        if sql_ok:
            return True, "sql_server", sql_msg
        
        mysql_ok, mysql_msg = self.check_mysql_connection()
        if mysql_ok:
            return True, "mysql", mysql_msg
        
        return False, "none", "所有数据库连接失败"
    
    def test_http_connection(self, url: str) -> Tuple[bool, str]:
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return True, "HTTP连接成功"
            else:
                return False, f"HTTP状态码: {response.status_code}"
        except Exception as e:
            return False, f"HTTP连接失败: {str(e)}"
    
    def get_network_status(self) -> dict:
        internet_ok = self.check_internet_connection()
        sql_ok, sql_msg = self.check_sql_server_connection()
        mysql_ok, mysql_msg = self.check_mysql_connection()
        
        return {
            'internet': internet_ok,
            'sql_server': sql_ok,
            'sql_server_message': sql_msg,
            'mysql': mysql_ok,
            'mysql_message': mysql_msg,
            'can_upload': sql_ok or mysql_ok
        }


network_service = NetworkService()
