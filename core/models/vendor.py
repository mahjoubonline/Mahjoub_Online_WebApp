# core/models/vendor.py
from core import db 
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'
    # هذا السطر ضروري جداً لتحديث الجداول الموجودة في Railway دون انهيار
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    # --- حقول الهوية السيادية (MAH-963) ---
    supplier_id = db.Column(db.String(50), unique=True) 
    trade_name = db.Column(db.String(150))
    owner_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    
    # المحفظة السيادية (W-MAH)
    e_wallet = db.Column(db.String(100), unique=True)
    
    # الأرصدة المالية السيادية (دعم العملات الثلاث)
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)
    
    # البيانات الجغرافية
    province = db.Column(db.String(100)) # المحافظة (عدن، الخوخة، إلخ)
    district = db.Column(db.String(100)) # المديرية
    activity_type = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقة العكسية مع المستخدم
    # ملاحظة: تم استخدام اسم 'User' كنص لتجنب الاستيراد الدائري
    user_rel = db.relationship('User', backref=db.backref('vendor_profile', uselist=False))

    def __repr__(self):
        return f'<Vendor {self.trade_name} - {self.supplier_id}>'

class WithdrawRequest(db.Model):
    __tablename__ = 'withdraw_requests'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10)) # YER, SAR, USD
    status = db.Column(db.String(20), default='pending') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
