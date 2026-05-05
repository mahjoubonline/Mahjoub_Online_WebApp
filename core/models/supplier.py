# core/models/supplier.py

# جرب هذا المسار إذا كانت extensions داخل مجلد core
from core.extensions import db 

# أو جرب هذا المسار إذا كانت extensions في المجلد الرئيسي مباشرة
# from extensions import db 

from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    owner_name = db.Column(db.String(150), nullable=False)
    trade_name = db.Column(db.String(150), nullable=False)
    activity_type = db.Column(db.String(100))
    id_type = db.Column(db.String(50))
    id_card_number = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
    e_wallet = db.Column(db.String(100), unique=True)
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Supplier {self.trade_name}>'
