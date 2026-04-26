from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

# 1. تعريف الكائن أولاً (هذا هو المحرك الذي كان مفقوداً)
db = SQLAlchemy()

# 2. الآن يمكنك تعريف الجداول التي تستخدم db
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # المحافظ السيادية
    wallet_balance = db.Column(db.Numeric(10, 2), default=0.00)
    wallet_usd = db.Column(db.Numeric(10, 2), default=0.00)
    wallet_sar = db.Column(db.Numeric(10, 2), default=0.00)
    wallet_yer = db.Column(db.Numeric(10, 2), default=0.00)
    
    is_approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')
    
    products = db.relationship('Product', backref='supplier_owner', lazy=True, cascade="all, delete-orphan")

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    q_product_id = db.Column(db.String(100), unique=True, nullable=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    sale_price = db.Column(db.Numeric(10, 2), nullable=True)
    currency = db.Column(db.String(10), default='SAR')
    status = db.Column(db.String(50), default='pending')
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
