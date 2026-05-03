# core/models/vendor.py

# السطر المفقود الذي تسبب في الخطأ (يجب استيراد db من قلب النظام)
from core import db 

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # حقول الهوية التجارية لـ "سوقك الذكي"
    trade_name = db.Column(db.String(150))
    owner_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    
    # الرقم السيادي للمحفظة
    e_wallet = db.Column(db.String(100), unique=True)
    
    # حقول الأرصدة المالية (YER, SAR, USD)
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)
    
    # البيانات الجغرافية والنشاط
    id_type = db.Column(db.String(50))
    id_card_number = db.Column(db.String(100))
    activity_type = db.Column(db.String(100))
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
    
    # البيانات البنكية
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    fin_type = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Vendor {self.trade_name}>'
