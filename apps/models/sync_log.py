# coding: utf-8
# 📂 apps/models/sync_log.py

from apps.extensions import db
from datetime import datetime
from apps.utils.security import AESCipher

class SyncLog(db.Model):
    __tablename__ = 'sync_logs'
    
    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # 🔗 الربط مع المورد والطلب لتعقب المشاكل بدقة
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True, index=True)
    order_id = db.Column(db.String(100), nullable=True, index=True) # ربط مباشر بالطلب
    
    # ⚡ معلومات العملية
    sync_type = db.Column(db.String(50), nullable=False, index=True) # (orders, inventory, etc.)
    status = db.Column(db.String(20), nullable=False, index=True)    # (success, failed)
    
    # 🔐 تشفير رسالة الخطأ (لحماية البيانات الحساسة داخل سجلات الخطأ)
    _error_message = db.Column('error_message', db.Text, nullable=True)
    
    # ⚡ الفهرسة للبحث الزمني
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # --- منطق التشفير ---
    @property
    def error_message(self):
        try:
            return AESCipher.decrypt(self._error_message) if self._error_message else None
        except:
            return "تعذر فك تشفير السجل"

    @error_message.setter
    def error_message(self, value):
        if value:
            self._error_message = AESCipher.encrypt(str(value))

    def __repr__(self):
        return f'<SyncLog {self.sync_type} | Status: {self.status} | Time: {self.timestamp}>'
