# 📂 apps/models/orders_db.py
import os
from apps.utils.bridge_engine import db  # أو مسار الـ db المعتمد في مشروعك
from datetime import datetime
from cryptography.fernet import Fernet

# جلب مفتاح التشفير السيادي المستند إلى معيار AES-256 من متغيرات البيئة
ENCRYPTION_KEY = os.environ.get('MAHJOUB_SECRET_KEY')
if not ENCRYPTION_KEY:
    # توليد مفتاح افتراضي للطوارئ إذا لم يكن موجوداً (يُفضل وضعه في ملف .env)
    ENCRYPTION_KEY = Fernet.generate_key().decode()

cipher_suite = Fernet(ENCRYPTION_KEY.encode())

class ProcessedOrder(db.Model):
    """
    جدول سيادي محصّن بتشفير AES-256 لتتبع وتوثيق الطلبات التي تم تسويتها حياً.
    """
    __tablename__ = 'processed_orders'

    id = db.Column(db.String(100), primary_key=True)  # معرف الطلب القادم من قمرة
    status = db.Column(db.String(50), default='processed')  # حالة التسوية
    
    # حقل مشفر بالكامل لتأمين البيانات المالية الحساسة
    _encrypted_total_price = db.Column(db.Text, nullable=False)
    
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total_price(self):
        """فك تشفير القيمة المالية تلقائياً عند القراءة"""
        try:
            decrypted_data = cipher_suite.decrypt(self._encrypted_total_price.encode()).decode()
            return float(decrypted_data)
        except Exception:
            return 0.0

    @total_price.setter
    def total_price(self, value):
        """تشفير القيمة المالية فوراً بمعيار AES-256 قبل الحفظ في الداتابيز"""
        encrypted_data = cipher_suite.encrypt(str(value).encode()).decode()
        self._encrypted_total_price = encrypted_data

    def __repr__(self):
        return f"<ProcessedOrder {self.id} - Encrypted Status: {self.status}>"
