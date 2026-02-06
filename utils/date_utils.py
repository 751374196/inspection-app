from datetime import datetime


class DateUtils:
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        return dt.strftime(format_str)
    
    @staticmethod
    def format_date(dt: datetime, format_str: str = '%Y-%m-%d') -> str:
        return dt.strftime(format_str)
    
    @staticmethod
    def format_time(dt: datetime, format_str: str = '%H:%M:%S') -> str:
        return dt.strftime(format_str)
    
    @staticmethod
    def get_current_datetime() -> datetime:
        return datetime.now()
    
    @staticmethod
    def get_current_timestamp() -> str:
        return datetime.now().strftime('%Y%m%d_%H%M%S')


date_utils = DateUtils()
