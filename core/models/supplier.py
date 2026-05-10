# core/models/supplier.py
from datetime import datetime
from flask_login import UserMixin
from core.extensions import db

class Supplier(db.Model, UserMixin):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True) # MAH-{{ next_id }}
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # بيانات المالك والتوثيق (مطابقة للقالب)
    trade_name = db.Column(db.String(150), nullable=False)
    owner_name = db.Column(db.String(150), nullable=False)
    activity_type = db.Column(db.String(100))
    identity_type = db.Column(db.String(50))
    identity_image = db.Column(db.String(255)) # لتخزين مسار صورة الهوية
    
    # الاتصال والجغرافيا
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150)) # أضفناه بناءً على طلب القالب
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
    
    # الربط المالي (الخزينة الثلاثية)
    bank_name = db.Column(db.String(150))
    bank_acc = db.Column(db.String(100))
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Supplier {self.trade_name}>"
