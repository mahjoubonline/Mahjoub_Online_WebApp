# 📂 apps/utils/time_utils.py
from datetime import datetime

def format_full_timestamp(dt):
    """تنسيق موحد للتاريخ والوقت للنظام كامل: YYYY-MM-DD HH:MM:SS"""
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_current_utc():
    """توقيت موحد لكل العمليات الحسابية في النظام"""
    return datetime.utcnow()
