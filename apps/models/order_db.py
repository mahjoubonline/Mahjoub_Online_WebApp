# 📂 apps/models/order_db.py
from apps.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    # المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    order_id_qumra = db.Column(db.String(100), unique=True, nullable=False) # رقم الطلب من قمرة
    
    # بيانات العميل والطلب
    customer_name = db.Column(db.String(200))
    customer_phone = db.Column(db.String(50))
    shipping_address = db.Column(db.String(500))
    total = db.Column(db.Float)
    
    # الحالات
    status = db.Column(db.String(50), default='pending') # حالة الشحن
    payment_status = db.Column(db.String(50), default='unpaid') # حالة الدفع
    payment_method = db.Column(db.String(100)) # وسيلة الدفع
    source = db.Column(db.String(100)) # المصدر (من المتجر / صفحة الهبوط)
    
    # الربط مع المورد (العلاقة المطلوبة)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # التوقيت
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.order_id_qumra}>'

# ملاحظة: تأكد من وجود الموديل الخاص بالموردين (Supplier) 
# في ملف apps/models/supplier_db.py لتعمل علاقة ForeignKey بشكل صحيح.
