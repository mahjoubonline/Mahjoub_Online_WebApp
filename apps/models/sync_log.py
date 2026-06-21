# coding: utf-8
# 📂 apps/models/sync_log_db.py - سجل المزامنة السيادي (مؤمن ومفهرس للتحمل المليوني)

from apps.extensions import db
from datetime import datetime
from apps.utils.security import AESCipher

class SyncLog(db.Model):
    __tablename__ = 'sync_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # ⚡ الفهرسة للفلترة السريعة (تصفية الناجح من الفاشل في أجزاء من الثانية)
    status = db.Column(db.String(20), nullable=False, index=True) 
    
    # 🔐 تشفير رسائل الخطأ الحساسة (إن وجدت)
    _error_message = db.Column('error_message', db.Text, nullable=True)
    
    # ⚡ الفهرسة للبحث الزمني (تتبع أخطاء آخر ساعة أو يوم)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    @property
    def error_message(self):
        return AESCipher.decrypt(self._error_message) if self._error_message else None

    @error_message.setter
    def error_message(self, value):
        self._error_message = AESCipher.encrypt(str(value)) if value else None

    def __repr__(self):
        return f'<SyncLog {self.status} at {self.timestamp}>'
