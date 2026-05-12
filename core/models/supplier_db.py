from core.extensions import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(100), unique=True, nullable=False)
    trade_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    tier = db.Column(db.String(50), default='مبتدئ')
    status = db.Column(db.String(50), default='نشط')
    balance_yer = db.Column(db.Numeric(20, 2), default=0.0)
    balance_sar = db.Column(db.Numeric(20, 2), default=0.0)
    balance_usd = db.Column(db.Numeric(20, 2), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
