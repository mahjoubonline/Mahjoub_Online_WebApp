# coding: utf-8
# 📂 apps/models/orders_db.py

from datetime import datetime
from apps.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    # [صمام الأمان]: فهرسة مسمّاة ومنع تكرار التعريف لضمان الاستقرار
    __table_args__ = (
        db.Index('idx_ord_supplier_id', 'supplier_id'),
        db.Index('idx_ord_ref', 'order_reference'),
        db.Index('idx_ord_cust_name', 'customer_name'),
        db.Index('idx_ord_cust_phone', 'customer_phone'),
        db.Index('idx_ord_status', 'status'),
        db.Index('idx_ord_created', 'created_at'),
        db.Index('idx_ord_updated', 'updated_at'),
        {'extend_existing': True}
    )

    # 1. المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # 2. روابط السيادة
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    order_reference = db.Column(db.String(100), unique=True, nullable=False)
    
    # 3. بيانات الشحن اللوجستية
    customer_name = db.Column(db.String(150))
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.Text) 
    
    # 4. حالة الطلب
    status = db.Column(db.String(30), default='pending') 
    
    # 5. التوثيق الزمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 6. [المسار الكامل]: الربط السيادي لمنع خطأ Multiple classes found
    supplier = db.relationship(
        'apps.models.supplier_db.Supplier', 
        back_populates='orders'
    )
    
    # الربط مع المالية (One-to-One)
    financials = db.relationship(
        'apps.models.financials_db.OrderFinancial', 
        back_populates='order', 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Order {self.order_reference} | Status: {self.status}>'
