# coding: utf-8
# 📂 apps/models/orders_db.py - نموذج الطلبات التفصيلي والمشفر

import base64
import hashlib
import logging
from datetime import datetime
from decimal import Decimal
from cryptography.fernet import Fernet
from apps.extensions import db
from config import Config

logger = logging.getLogger(__name__)

# 1. إعداد التشفير الآمن
try:
    raw_key = Config.ENCRYPTION_KEY
    hashed_key = hashlib.sha256(raw_key.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(hashed_key)
    cipher_suite = Fernet(fernet_key)
except Exception as e:
    logger.critical(f"❌ فشل إعداد محرك التشفير: {e}")
    raise e

class ProcessedOrder(db.Model):
    __tablename__ = 'processed_orders'

    # البيانات الأساسية (تم استخدام id كـ orderId القادم من قمرة)
    id = db.Column(db.String(100), primary_key=True) 
    status = db.Column(db.String(50), default='pending')
    
    # حقول إضافية من بيانات قمرة الدقيقة
    customer_name = db.Column(db.String(255), nullable=True)
    items_count = db.Column(db.Integer, default=0)
    created_at_api = db.Column(db.DateTime, nullable=True) # تاريخ الطلب من قمرة
    processed_at = db.Column(db.DateTime, default=datetime.utcnow) # تاريخ المزامنة المحلي
    
    # الحقل المشفر للقيمة المالية
    _encrypted_total_price = db.Column(db.Text, nullable=False)

    # 2. إدارة التشفير
    @property
    def total_price(self):
        try:
            decrypted_val = cipher_suite.decrypt(self._encrypted_total_price.encode()).decode()
            return Decimal(decrypted_val)
        except Exception as e:
            logger.error(f"⚠️ خطأ أثناء فك تشفير السعر للطلب {self.id}: {e}")
            return Decimal('0.0')

    @total_price.setter
    def total_price(self, value):
        try:
            self._encrypted_total_price = cipher_suite.encrypt(str(value).encode()).decode()
        except Exception as e:
            logger.error(f"❌ خطأ أثناء تشفير السعر للطلب {self.id}: {e}")
            raise ValueError("فشل تشفير القيمة المالية")

    def __repr__(self):
        return f"<ProcessedOrder {self.id} - Status: {self.status}>"

# 3. جدول المنتجات المترابط
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), db.ForeignKey('processed_orders.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(10, 2), default=0.0)
    
    order = db.relationship(
        'ProcessedOrder', 
        backref=db.backref('items', lazy='dynamic', cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<OrderItem {self.product_name} - Qty: {self.quantity}>"
