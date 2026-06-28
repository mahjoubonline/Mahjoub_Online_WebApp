# coding: utf-8
# 📂 apps/models/orders_db.py

from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db
import os

# تهيئة مفتاح التشفير (يجب أن يكون مخزناً في متغيرات البيئة)
# تأكد من وجود مفتاح تشفير صالح في CONFIG
cipher = Fernet(os.getenv('ENCRYPTION_KEY', Fernet.generate_key()))

class Order(db.Model):
    __tablename__ = 'orders'

    # [صمام الأمان]: فهرسة مسمّاة لضمان سرعة الاستعلامات والربط
    __table_args__ = (
        db.Index('idx_ord_supplier_id', 'supplier_id'),
        db.Index('idx_ord_ref', 'order_reference'),
        db.Index('idx_ord_status', 'status'),
        db.Index('idx_ord_created', 'created_at'),
        {'extend_existing': True}
    )

    # 1. المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # 2. روابط السيادة
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    order_reference = db.Column(db.String(100), unique=True, nullable=False)
    
    # 3. بيانات الشحن (تم تفعيل التشفير للأعمدة الحساسة)
    _customer_name = db.Column('customer_name', db.Text)
    _customer_phone = db.Column('customer_phone', db.Text)
    customer_address = db.Column(db.Text) 
    
    # 4. حالة الطلب
    status = db.Column(db.String(30), default='pending') 
    
    # 5. التوثيق الزمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 6. الربط السيادي (استخدام اسم الكلاس لكسر حلقة الـ Import)
    supplier = db.relationship('Supplier', back_populates='orders')
    
    # الربط مع المالية
    financials = db.relationship('OrderFinancial', back_populates='order', uselist=False, cascade="all, delete-orphan")

    # --- منطق التشفير ---
    @property
    def customer_name(self):
        return cipher.decrypt(self._customer_name.encode()).decode()

    @customer_name.setter
    def customer_name(self, value):
        self._customer_name = cipher.encrypt(value.encode()).decode()

    @property
    def customer_phone(self):
        return cipher.decrypt(self._customer_phone.encode()).decode()

    @customer_phone.setter
    def customer_phone(self, value):
        self._customer_phone = cipher.encrypt(value.encode()).decode()

    def __repr__(self):
        return f'<Order {self.order_reference} | Status: {self.status}>'
