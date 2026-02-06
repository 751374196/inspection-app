# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Tuple, Callable
from models.inspection_data import InspectionData, UploadStatus
from services.database_service import db_service
from services.network_service import network_service
from config.app_config import app_config
import json


class UploadService:
    def __init__(self):
        self.config = app_config.get_upload_config()
        self.retry_count = self.config.get('retry_count', 3)
    
    def upload_to_sql_server(self, data: InspectionData) -> Tuple[bool, str]:
        try:
            import pyodbc
            sql_config = app_config.get_sql_server_config()
            
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={sql_config.host};'
                f'DATABASE={sql_config.database};'
                f'UID={sql_config.username};'
                f'PWD={sql_config.password}'
            )
            
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO inspection_records (
                    GUID_MAIN, device_id, device_name, production_line, inspection_type,
                    unit, measured_value, remark, capture_time, upload_time,
                    IsDelete, START_MEMBER_ID, START_DATE,
                    MODIFY_MEMBER_ID, MODIFY_DATE, MODIFY_LOGS
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.guid_main,
                data.device_id,
                data.device_name,
                data.production_line,
                data.inspection_type,
                data.unit,
                data.measured_value,
                data.remark,
                data.capture_time,
                datetime.now(),
                0,
                data.start_member_id,
                data.start_date,
                data.modify_member_id,
                data.modify_date,
                data.modify_logs
            ))
            
            conn.commit()
            conn.close()
            
            return True, "SQL Server上传成功"
        except ImportError:
            return False, "pyodbc未安装"
        except Exception as e:
            return False, f"SQL Server上传失败: {str(e)}"
    
    def upload_single_data(self, data: InspectionData) -> Tuple[bool, str]:
        for attempt in range(self.retry_count):
            sql_ok, sql_msg = self.upload_to_sql_server(data)
            if sql_ok:
                return True, sql_msg
        
        return False, "SQL Server上传失败"
    
    def upload_all_unuploaded(self, progress_callback: Callable[[int, int, str], None] = None) -> Tuple[int, int, List[str]]:
        unuploaded_data = db_service.get_data_by_status(UploadStatus.NOT_UPLOADED)
        
        if not unuploaded_data:
            return 0, 0, []
        
        total = len(unuploaded_data)
        success_count = 0
        failed_count = 0
        logs = []
        
        for i, data in enumerate(unuploaded_data):
            db_service.update_upload_status(data.id, UploadStatus.UPLOADING)
            
            if progress_callback:
                progress_callback(i + 1, total, f"正在上传: {data.device_name}")
            
            success, message = self.upload_single_data(data)
            
            if success:
                db_service.update_upload_status(data.id, UploadStatus.UPLOADED, datetime.now())
                success_count += 1
                logs.append(f"✓ {data.device_name} 上传成功")
            else:
                db_service.update_upload_status(data.id, UploadStatus.FAILED)
                failed_count += 1
                logs.append(f"✗ {data.device_name} 上传失败: {message}")
            
            if progress_callback:
                progress_callback(i + 1, total, message)
        
        return success_count, failed_count, logs
    
    def upload_selected_data(self, data_ids: List[int], progress_callback: Callable[[int, int, str], None] = None) -> Tuple[int, int, List[str]]:
        success_count = 0
        failed_count = 0
        logs = []
        total = len(data_ids)
        
        for i, data_id in enumerate(data_ids):
            data = db_service.get_data_by_id(data_id)
            if not data:
                continue
            
            db_service.update_upload_status(data_id, UploadStatus.UPLOADING)
            
            if progress_callback:
                progress_callback(i + 1, total, f"正在上传: {data.device_name}")
            
            success, message = self.upload_single_data(data)
            
            if success:
                db_service.update_upload_status(data_id, UploadStatus.UPLOADED, datetime.now())
                success_count += 1
                logs.append(f"✓ {data.device_name} 上传成功")
            else:
                db_service.update_upload_status(data_id, UploadStatus.FAILED)
                failed_count += 1
                logs.append(f"✗ {data.device_name} 上传失败: {message}")
            
            if progress_callback:
                progress_callback(i + 1, total, message)
        
        return success_count, failed_count, logs
    
    def get_unuploaded_count(self) -> int:
        return db_service.get_unuploaded_count()
    
    def can_upload(self) -> bool:
        status = network_service.get_network_status()
        return status['can_upload']


upload_service = UploadService()
