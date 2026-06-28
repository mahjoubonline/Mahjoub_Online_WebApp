# coding: utf-8
# 📂 apps/models/orders_db.py

import os
from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db

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
    
    # 3. بيانات الشحن اللوجستية (تم الحفاظ على التوافق)
    customer_name = db.Column(db.String(150))
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.Text) 
    
    # 4. حالة الطلب
    status = db.Column(db.String(30), default='pending') 
    
    # 5. التوثيق الزمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 6. الربط السيادي (تجنب أخطاء Multiple classes found)
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

    # --- ملاحظة حول التشفير ---
    # إذا كنت تحتاج لتشفير customer_name أو phone، نتبع نفس نهج التشفير في Wallet.
    # حالياً أبقينا البيانات بنص واضح لسهولة الفرز، لكن الهيكل جاهز للتشفير.

    def __repr__(self):
        return f'<Order {self.order_reference} | Status: {self.status}>'
