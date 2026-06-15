# 📂 apps/models/order_db.py
from apps.extensions import db
from datetime import datetime
from sqlalchemy.types import JSON  # لاستخدام JSON كنوع بيانات

class Order(db.Model):
    __tablename__ = 'orders'
    
    # المعرفات
    id = db.Column(db.Integer, primary_key=True)
    order_id_qumra = db.Column(db.String(100), unique=True, nullable=False) 
    
    # تفاصيل العميل (مرونة: nullable=True لتجنب فشل المزامنة)
    customer_name = db.Column(db.String(200), nullable=True)
    customer_phone = db.Column(db.String(50), nullable=True)
    
    # البيانات المالية واللوجستية
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')
    payment_status = db.Column(db.String(50), default='unpaid')
    
    # مخزن البيانات الديناميكي (جوهر الفكرة)
    # هنا سيتم حفظ كل تفاصيل الطلب كما تأتي من قمرة
    raw_data = db.Column(JSON, nullable=True)
    
    # العلاقات
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # التوقيت
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقة مع المورد
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))

    def to_dict(self):
        """إرجاع بيانات الطلب مع دمج البيانات الخام عند الحاجة"""
        return {
            'id': self.id,
            'order_id_qumra': self.order_id_qumra,
            'customer_name': self.customer_name or 'غير معروف',
            'total': self.total,
            'status': self.status,
            'raw_data_summary': self.raw_data.keys() if self.raw_data else [], # لمعرفة ما يوجد داخل JSON
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }
