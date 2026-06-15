# 📂 apps/models/order_db.py
from apps.extensions import db
from datetime import datetime
# استيراد نموذج الموردين للتأكد من ربط العلاقات بشكل صحيح
from apps.models.supplier_db import Supplier 

class Order(db.Model):
    __tablename__ = 'orders'
    
    # المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    order_id_qumra = db.Column(db.String(100), unique=True, nullable=False) 
    
    # تفاصيل العميل والشحن
    customer_name = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50))
    shipping_address = db.Column(db.String(500))
    
    # البيانات المالية واللوجستية
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending') # حالة الشحن (pending, ready, delivered)
    payment_status = db.Column(db.String(50), default='unpaid') 
    payment_method = db.Column(db.String(100)) 
    source = db.Column(db.String(100)) # مصدر الطلب (متجر / صفحة هبوط)
    
    # الربط السيادي (المورد / المتجر)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # التوقيت
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقة (Relationship)
    # نستخدم اسم الكلاس 'Supplier' كسترينج لتجنب Circular Import إذا لزم الأمر
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.order_id_qumra}>'

    def to_dict(self):
        """مفيد لإرجاع بيانات الطلب في استجابات الـ JSON"""
        return {
            'id': self.id,
            'order_id_qumra': self.order_id_qumra,
            'customer_name': self.customer_name,
            'total': self.total,
            'status': self.status,
            'supplier_name': self.supplier.name if self.supplier else 'غير محدد',
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }
