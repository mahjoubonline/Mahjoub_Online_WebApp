# coding: utf-8
# 📂 apps/models/order_db.py - نظام الطلبات السيادي (مؤمن ومفهرس للتحمل المليوني)

from apps.extensions import db
from apps.utils.security import AESCipher
from datetime import datetime

class ProcessedOrder(db.Model):
    __tablename__ = 'processed_orders'

    # ID كمعرف أساسي
    id = db.Column(db.String(100), primary_key=True)  # QID
    
    # ⚡ فهارس للبحث السريع في الطلبات
    order_id = db.Column(db.String(50), index=True)
    order_status = db.Column(db.String(50), index=True)
    financial_status = db.Column(db.String(50), index=True)
    fulfillment_status = db.Column(db.String(50), index=True)
    shipping_city = db.Column(db.String(100), index=True)
    shipping_street = db.Column(db.String(200))
    
    # ⚡ مفتاح ربط مفهرس (ضروري جداً لجلب طلبات مورد معين)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # --- الحقول المشفرة ---
    _total_price = db.Column('total_price', db.String(255))
    _customer_name = db.Column('customer_name', db.String(255))
    _customer_phone = db.Column('customer_phone', db.String(255))
    _customer_email = db.Column('customer_email', db.String(255))

    # --- Properties (تشفير وفك تشفير) ---
    @property
    def total_price(self):
        val = AESCipher.decrypt(self._total_price)
        return float(val) if val else 0.0

    @total_price.setter
    def total_price(self, value):
        self._total_price = AESCipher.encrypt(str(value))

    # (إضافة الـ Properties لبقية الحقول بنفس الطريقة...)

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    # ⚡ فهرسة order_id لجلب منتجات الطلب الواحد فوراً
    order_id = db.Column(db.String(100), db.ForeignKey('processed_orders.id'), index=True)
    product_title = db.Column(db.String(200), index=True)
    quantity = db.Column(db.Integer)
    _price = db.Column('price', db.String(255))

    @property
    def price(self):
        val = AESCipher.decrypt(self._price)
        return float(val) if val else 0.0

    @price.setter
    def price(self, value):
        self._price = AESCipher.encrypt(str(value))
