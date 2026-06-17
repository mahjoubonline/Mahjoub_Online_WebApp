# coding: utf-8
# 📂 apps/models/sync_log.py - سجل مراقبة المزامنة

from datetime import datetime
from apps.extensions import db

class SyncLog(db.Model):
    __tablename__ = 'sync_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20)) # (success, failed)
    message = db.Column(db.Text)      # تفاصيل الخطأ أو عدد الطلبات المزامنة
    page = db.Column(db.Integer)      # أي صفحة توقفت عندها
    
    def __repr__(self):
        return f"<SyncLog {self.status} at {self.timestamp}>"
