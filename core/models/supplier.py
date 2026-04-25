from core import db
from datetime import datetime
from flask_login import UserMixin

class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    
    # بيانات الدخول والتعميد
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    activity_type = db.Column(db.String(100))
    
    # تفاصيل المنشأة والموقع التيهامي
    trade_name = db.Column(db.String(200))
    full_name = db.Column(db.String(200))
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    # النظام المالي والمحفظة
    fin_type = db.Column(db.String(50))
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    wallet_balance = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # علاقة الربط بالمنتجات
    products = db.relationship('Product', backref='supplier_owner', lazy=True, cascade="all, delete-orphan")

    @property
    def sovereign_id(self):
        """توليد الرقم السيادي للمحفظة MAH-9046"""
        return f"MAH-9046{self.id}"

    def __repr__(self):
        return f'<Supplier: {self.name} | Wallet: {self.sovereign_id}>'
