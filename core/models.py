from core import db
from datetime import datetime
from flask_login import UserMixin # ضروري لإدارة جلسات الدخول

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # ستكون مشفرة
    role = db.Column(db.String(20), default='admin') # لتحديد الصلاحيات (قائد، مراقب، الخ)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True) # لتمكين المورد من الدخول بلوحته
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # علاقة الربط مع المنتجات
    products = db.relationship('Product', backref='owner', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
