# coding: utf-8
# 📂 apps/models/orders_db.py

from apps.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    
    # 1. روابط السيادة والتبعية
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, index=True)
    order_reference = db.Column(db.String(100), unique=True, nullable=False, index=True) # رقم الطلب الفريد
    
    # 2. بيانات الشحن اللوجستية (للزبون)
    customer_name = db.Column(db.String(150), index=True)
    customer_phone = db.Column(db.String(20), index=True)
    customer_address = db.Column(db.Text) 
    
    # 3. حالة الطلب (مفهرسة لتتبع التقدم)
    status = db.Column(db.String(30), default='pending', index=True) 
    
    # 4. التوثيق الزمني الدقيق
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # 5. الربط مع المورد
    supplier = db.relationship('Supplier', back_populates='orders')
    
    # 6. الربط مع المالية (هذا هو السطر الذي كان مفقوداً وتسبب في الخطأ)
    financials = db.relationship('OrderFinancial', back_populates='order', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.order_reference} | Status: {self.status}>'
