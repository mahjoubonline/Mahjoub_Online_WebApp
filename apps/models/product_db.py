# coding: utf-8
# 📂 apps/models/product_db.py - (جسر المنتجات بين واجهة قمرة وسيرفر محجوب الخلفي)

from apps.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 🎯 وسم المورد المخفي (موجود فقط في سيرفرك ولا يظهر في قمرة أبداً لضمان السرية)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)
    
    # 🔗 معرف المنتج في منصة قمرة (لربط الـ Webhook القادم بالمنتج الصحيح في سيرفرك)
    qamrah_product_id = db.Column(db.String(100), unique=True, index=True, nullable=True)
    
    product_name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)            # رمز التخزين الفريد للمطابقة
    
    # --- تفكيك الهيكل المالي الحاص بالتكلفة والسوق ---
    cost_price = db.Column(db.Numeric(16, 2), nullable=False)              # سعر التكلفة النقي (الذي يتدفق لمحفظة المورد)
    market_sale_price = db.Column(db.Numeric(16, 2), nullable=False)       # سعر البيع النهائي للزبون المعروض في قمرة
    
    currency = db.Column(db.String(10), default='YER', nullable=False)     # 'YER', 'SAR', 'USD'
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # روابط العلاقات
    supplier = db.relationship('Supplier', backref='products')
