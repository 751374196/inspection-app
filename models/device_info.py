# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class DeviceInfo:
    device_id: str
    device_name: str
    production_line: str
    inspection_type: str
    unit: str
    
    @classmethod
    def from_json(cls, json_str: str) -> Optional['DeviceInfo']:
        try:
            data = json.loads(json_str)
            return cls(
                device_id=data.get('device_id', ''),
                device_name=data.get('device_name', ''),
                production_line=data.get('production_line', ''),
                inspection_type=data.get('inspection_type', ''),
                unit=data.get('unit', '')
            )
        except Exception:
            return None
    
    def to_dict(self) -> dict:
        return {
            'device_id': self.device_id,
            'device_name': self.device_name,
            'production_line': self.production_line,
            'inspection_type': self.inspection_type,
            'unit': self.unit
        }
