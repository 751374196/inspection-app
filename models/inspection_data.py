# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid


class UploadStatus(Enum):
    NOT_UPLOADED = 'not_uploaded'
    UPLOADING = 'uploading'
    UPLOADED = 'uploaded'
    FAILED = 'failed'


@dataclass
class InspectionData:
    id: Optional[int]
    device_id: str
    device_name: str
    production_line: str
    inspection_type: str
    unit: str
    measured_value: float
    image_path: str
    remark: str
    capture_time: datetime
    upload_status: UploadStatus
    upload_time: Optional[datetime]
    guid_main: Optional[str] = None
    start_member_id: Optional[str] = None
    start_date: Optional[datetime] = None
    modify_member_id: Optional[str] = None
    modify_date: Optional[datetime] = None
    modify_logs: Optional[str] = None
    
    def __post_init__(self):
        if self.guid_main is None:
            self.guid_main = str(uuid.uuid4())
        if self.start_date is None:
            self.start_date = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'production_line': self.production_line,
            'inspection_type': self.inspection_type,
            'unit': self.unit,
            'measured_value': self.measured_value,
            'image_path': self.image_path,
            'remark': self.remark,
            'capture_time': self.capture_time.isoformat() if self.capture_time else None,
            'upload_status': self.upload_status.value,
            'upload_time': self.upload_time.isoformat() if self.upload_time else None,
            'guid_main': self.guid_main,
            'start_member_id': self.start_member_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'modify_member_id': self.modify_member_id,
            'modify_date': self.modify_date.isoformat() if self.modify_date else None,
            'modify_logs': self.modify_logs
        }
