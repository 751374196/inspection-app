# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Optional
from models.inspection_data import InspectionData, UploadStatus
from config.app_config import app_config


class DatabaseService:
    def __init__(self):
        self.db_path = app_config.db_path
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inspection_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                device_name TEXT NOT NULL,
                production_line TEXT NOT NULL,
                inspection_type TEXT NOT NULL,
                unit TEXT NOT NULL,
                measured_value REAL NOT NULL,
                image_path TEXT NOT NULL,
                remark TEXT,
                capture_time TEXT NOT NULL,
                upload_status TEXT NOT NULL,
                upload_time TEXT,
                guid_main TEXT,
                start_member_id TEXT,
                start_date TEXT,
                modify_member_id TEXT,
                modify_date TEXT,
                modify_logs TEXT
            )
        ''')
        
        self._migrate_database(cursor)
        
        conn.commit()
        conn.close()
    
    def _migrate_database(self, cursor):
        cursor.execute("PRAGMA table_info(inspection_data)")
        columns = [row[1] for row in cursor.fetchall()]
        
        new_columns = {
            'guid_main': 'TEXT',
            'start_member_id': 'TEXT',
            'start_date': 'TEXT',
            'modify_member_id': 'TEXT',
            'modify_date': 'TEXT',
            'modify_logs': 'TEXT'
        }
        
        for column_name, column_type in new_columns.items():
            if column_name not in columns:
                try:
                    cursor.execute(f'ALTER TABLE inspection_data ADD COLUMN {column_name} {column_type}')
                    print(f'已添加列: {column_name}')
                except sqlite3.OperationalError as e:
                    print(f'添加列 {column_name} 失败: {e}')
    
    def save_inspection_data(self, data: InspectionData) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO inspection_data (
                device_id, device_name, production_line, inspection_type,
                unit, measured_value, image_path, remark, capture_time,
                upload_status, upload_time, guid_main, start_member_id,
                start_date, modify_member_id, modify_date, modify_logs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.device_id,
            data.device_name,
            data.production_line,
            data.inspection_type,
            data.unit,
            data.measured_value,
            data.image_path,
            data.remark,
            data.capture_time.isoformat(),
            data.upload_status.value,
            data.upload_time.isoformat() if data.upload_time else None,
            data.guid_main,
            data.start_member_id,
            data.start_date.iso() if data.start_date else None,
            data.modify_member_id,
            data.modify_date.isoformat() if data.modify_date else None,
            data.modify_logs
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    def get_all_data(self) -> List[InspectionData]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, device_id, device_name, production_line, inspection_type,
                   unit, measured_value, image_path, remark, capture_time,
                   upload_status, upload_time, guid_main, start_member_id,
                   start_date, modify_member_id, modify_date, modify_logs
            FROM inspection_data
            ORDER BY capture_time DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_inspection_data(row) for row in rows]
    
    def get_data_by_status(self, status: UploadStatus) -> List[InspectionData]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, device_id, device_name, production_line, inspection_type,
                   unit, measured_value, image_path, remark, capture_time,
                   upload_status, upload_time, guid_main, start_member_id,
                   start_date, modify_member_id, modify_date, modify_logs
            FROM inspection_data
            WHERE upload_status = ?
            ORDER BY capture_time DESC
        ''', (status.value,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_inspection_data(row) for row in rows]
    
    def get_data_by_id(self, data_id: int) -> Optional[InspectionData]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, device_id, device_name, production_line, inspection_type,
                   unit, measured_value, image_path, remark, capture_time,
                   upload_status, upload_time, guid_main, start_member_id,
                   start_date, modify_member_id, modify_date, modify_logs
            FROM inspection_data
            WHERE id = ?
        ''', (data_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_inspection_data(row)
        return None
    
    def update_upload_status(self, data_id: int, status: UploadStatus, upload_time: Optional[datetime] = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE inspection_data
            SET upload_status = ?, upload_time = ?
            WHERE id = ?
        ''', (status.value, upload_time.isoformat() if upload_time else None, data_id))
        
        conn.commit()
        conn.close()
    
    def delete_data(self, data_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM inspection_data WHERE id = ?', (data_id,))
        
        conn.commit()
        conn.close()
    
    def delete_all_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM inspection_data')
        
        conn.commit()
        conn.close()
    
    def get_unuploaded_count(self) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM inspection_data
            WHERE upload_status = ?
        ''', (UploadStatus.NOT_UPLOADED.value,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def cleanup_old_data(self, days: int = 7) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_date_str = cutoff_date.isoformat()
        
        cursor.execute('''
            DELETE FROM inspection_data
            WHERE upload_status = ?
            AND capture_time < ?
        ''', (UploadStatus.UPLOADED.value, cutoff_date_str))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def _row_to_inspection_data(self, row) -> InspectionData:
        return InspectionData(
            id=row[0],
            device_id=row[1],
            device_name=row[2],
            production_line=row[3],
            inspection_type=row[4],
            unit=row[5],
            measured_value=row[6],
            image_path=row[7],
            remark=row[8],
            capture_time=datetime.fromisoformat(row[9]),
            upload_status=UploadStatus(row[10]),
            upload_time=datetime.fromisoformat(row[11]) if row[11] else None,
            guid_main=row[12] if len(row) > 12 else None,
            start_member_id=row[13] if len(row) > 13 else None,
            start_date=datetime.fromisoformat(row[14]) if len(row) > 14 and row[14] else None,
            modify_member_id=row[15] if len(row) > 15 else None,
            modify_date=datetime.fromisoformat(row[16]) if len(row) > 16 and row[16] else None,
            modify_logs=row[17] if len(row) > 17 else None
        )


db_service = DatabaseService()
