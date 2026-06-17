# coding: utf-8
# 📂 apps/models/orders_db.py - نموذج الطلبات المشفر

import os
import base64
import hashlib
from apps.extensions import db
from datetime import datetime
from cryptography.fernet import Fernet
# استيراد Config لضمان استخدام نفس المفتاح دائماً
from config import Config

# تهيئة المحرك الأمني باستخدام المفتاح المركزي المعتمد
raw_key = Config.ENCRYPTION_KEY
hashed_key = hashlib.sha256(raw_key.encode()).digest()
fernet_key = base64.urlsafe_b64encode(hashed_key)
cipher_suite = Fernet(fernet_key)

class ProcessedOrder(db.Model):
    __tablename__ = 'processed_orders'

    # معرف الطلب (String لأن قمرا قد تستخدم معرفات نصية أو رقمية طويلة)
    id = db.Column(db.String(100), primary_key=True) 
    
    # حالة الطلب (مثال: paid, pending, settled)
    status = db.Column(db.String(50), default='paid')
    
    # الحقل المشفر للقيمة المالية (لا يظهر كأرقام واضحة في قاعدة البيانات)
    _encrypted_total_price = db.Column(db.Text, nullable=False)
    
    # وقت معالجة الطلب
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total_price(self):
        """فك تشفير القيمة المالية عند القراءة من قاعدة البيانات"""
        try:
            return float(cipher_suite.decrypt(self._encrypted_total_price.encode()).decode())
        except Exception:
            return 0.0

    @total_price.setter
    def total_price(self, value):
        """تشفير القيمة المالية تلقائياً عند حفظها في قاعدة البيانات"""
        self._encrypted_total_price = cipher_suite.encrypt(str(value).encode()).decode()

    def __repr__(self):
        return f"<ProcessedOrder {self.id} - Status: {self.status}>"
