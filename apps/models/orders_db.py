# coding: utf-8
# 📂 apps/models/orders_db.py

from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db
import os

# تهيئة مفتاح التشفير
cipher = Fernet(os.getenv('ENCRYPTION_KEY', Fernet.generate_key()))

class Order(db.Model):
    __tablename__ = 'orders'

    __table_args__ = (
        db.Index('idx_ord_supplier_id', 'supplier_id'),
        db.Index('idx_ord_ref', 'order_reference'),
        db.Index('idx_ord_status', 'status'),
        db.Index('idx_ord_created', 'created_at'),
        {'extend_existing': True}
    )

    # المعرفات
    id = db.Column(db.String(100), primary_key=True) # الـ API ID
    order_id_display = db.Column(db.String(50), nullable=True) # الرقم التسلسلي للعرض
    
    # الربط والبيانات المالية
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    order_reference = db.Column(db.String(100), unique=True, nullable=True) 
    
    # حقول المزامنة (بدون تشفير للبحث السريع)
    total_price = db.Column(db.Float, default=0.0)
    items_count = db.Column(db.Integer, default=0)
    
    # بيانات العميل (مشفرة)
    _customer_name = db.Column('customer_name', db.Text)
    _customer_phone = db.Column('customer_phone', db.Text)
    customer_address = db.Column(db.Text) 
    
    # حالة الطلب (نستخدم status كما هو في قاعدتك لتجنب الخطأ)
    status = db.Column(db.String(30), default='pending') 
    
    # التوثيق الزمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    supplier = db.relationship('Supplier', back_populates='orders')
    financials = db.relationship('OrderFinancial', back_populates='order', uselist=False, cascade="all, delete-orphan")

    # --- منطق التشفير ---
    @property
    def customer_name(self):
        try:
            return cipher.decrypt(self._customer_name.encode()).decode()
        except: return "غير معروف"

    @customer_name.setter
    def customer_name(self, value):
        self._customer_name = cipher.encrypt(value.encode()).decode()

    # (تم إضافة هذا ليتوافق مع routes.py دون الحاجة لتغيير قاعدة البيانات)
    @property
    def order_status(self):
        return self.status

    def __repr__(self):
        return f'<Order {self.id} | Status: {self.status}>'
