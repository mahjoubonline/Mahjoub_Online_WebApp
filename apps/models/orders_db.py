# coding: utf-8
import os
from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db

# تهيئة مفتاح التشفير (يجب أن يكون ENCRYPTION_KEY موجوداً في متغيرات البيئة على Render)
def get_cipher():
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        # تحذير: في الإنتاج يجب دائماً توفير مفتاح ثابت
        return Fernet(Fernet.generate_key())
    return Fernet(key.encode())

cipher = get_cipher()

class Order(db.Model):
    __tablename__ = 'orders'

    # تحسين الأداء عبر الفهارس (Indexes)
    __table_args__ = (
        db.Index('idx_ord_supplier_id', 'supplier_id'),
        db.Index('idx_ord_ref', 'order_reference'),
        db.Index('idx_ord_status', 'status'),
        db.Index('idx_ord_created', 'created_at'),
        {'extend_existing': True}
    )

    # المعرفات الأساسية
    id = db.Column(db.String(100), primary_key=True) 
    order_id_display = db.Column(db.String(50), nullable=True)
    
    # الربط والبيانات المالية
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    order_reference = db.Column(db.String(100), unique=True, nullable=True) 
    
    # بيانات بدون تشفير (للبحث والفلترة السريعة)
    total_price = db.Column(db.Numeric(18, 2), default=0.00)
    items_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default='pending') 
    
    # بيانات مشفرة (تخزين مخفي)
    _customer_name = db.Column('customer_name', db.Text)
    _customer_phone = db.Column('customer_phone', db.Text)
    _customer_address = db.Column('customer_address', db.Text)
    
    # التوثيق الزمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    supplier = db.relationship('Supplier', back_populates='orders')
    financials = db.relationship('OrderFinancial', back_populates='order', uselist=False, cascade="all, delete-orphan")

    # --- منطق التشفير (Customer Name) ---
    @property
    def customer_name(self):
        if not self._customer_name: return "غير معروف"
        try:
            return cipher.decrypt(self._customer_name.encode()).decode()
        except: return "خطأ في فك التشفير"

    @customer_name.setter
    def customer_name(self, value):
        self._customer_name = cipher.encrypt(str(value).encode()).decode()

    # --- منطق التشفير (Customer Phone) ---
    @property
    def customer_phone(self):
        try:
            return cipher.decrypt(self._customer_phone.encode()).decode() if self._customer_phone else None
        except: return None

    @customer_phone.setter
    def customer_phone(self, value):
        if value:
            self._customer_phone = cipher.encrypt(str(value).encode()).decode()

    # --- منطق التشفير (Customer Address) ---
    @property
    def customer_address(self):
        try:
            return cipher.decrypt(self._customer_address.encode()).decode() if self._customer_address else None
        except: return None

    @customer_address.setter
    def customer_address(self, value):
        if value:
            self._customer_address = cipher.encrypt(str(value).encode()).decode()

    @property
    def order_status(self):
        return self.status

    def __repr__(self):
        return f'<Order {self.id} | Status: {self.status}>'
