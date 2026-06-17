# 📂 apps/models/sync_log.py
from datetime import datetime
from apps.extensions import db

class SyncLog(db.Model):
    """
    سجل عمليات المزامنة: لضمان الرقابة على الطلبات القادمة من سلة.
    يستخدم لتتبع نجاح أو فشل الويب هوك والعمليات التلقائية.
    """
    __tablename__ = 'sync_logs'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50))      # مثلاً: 'webhook_received', 'manual_sync', 'auto_sync'
    status = db.Column(db.String(20))          # 'success' أو 'failed'
    order_id = db.Column(db.String(100), nullable=True) # لربط السجل بطلب معين
    message = db.Column(db.Text, nullable=True) # تفاصيل الخطأ في حال الفشل
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SyncLog {self.event_type} - {self.status}>"
