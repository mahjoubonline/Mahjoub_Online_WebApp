# core/models/supplier.py

# استخدام الاستيراد النسبي للخروج من مجلد models والوصول لـ extensions
from ..extensions import db 
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    # المعرفات
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    # بيانات النشاط
    owner_name = db.Column(db.String(150), nullable=False)
    trade_name = db.Column(db.String(150), nullable=False)
    activity_type = db.Column(db.String(100))
    
    # بيانات التوثيق
    id_type = db.Column(db.String(50))
    id_card_number = db.Column(db.String(50))
    
    # الاتصال والجغرافيا (تركيزنا على الخوخة، حيس، عدن)
    phone = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
    
    # الربط المالي (المحفظة السيادية)
    e_wallet = db.Column(db.String(100), unique=True)
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    
    # الحالة والتوقيت
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Supplier {self.trade_name}>'
