from core import db  # استيراد كائن قاعدة البيانات من تطبيق الفلاسك الخاص بك
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    # المعرفات والربط الأساسي
    id = db.Column(db.Integer, primary_key=True)
    # ملاحظة: إذا كنت تربط المورد بمستخدم، تأكد من وجود جدول User في core/models/user.py
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=True) 
    
    # المعرفات السيادية (نظام الترسانة)
    sovereign_id = db.Column(db.String(20), unique=True, nullable=False)
    e_wallet = db.Column(db.String(50), unique=True, nullable=False)
    
    # بيانات النشاط والتوثيق
    trade_name = db.Column(db.String(255), nullable=False)
    owner_name = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    
    # بيانات الهوية
    id_type = db.Column(db.String(50), nullable=False)
    id_card_number = db.Column(db.String(100), nullable=False)
    id_image = db.Column(db.String(255), nullable=True) # مسار الصورة في السيرفر
    phone = db.Column(db.String(20), nullable=False)
    
    # النطاق الجغرافي (Aden, Al-Khokha, Mocha, Hays)
    province = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    address_detail = db.Column(db.Text, nullable=False)
    
    # الربط المالي السيادي
    fin_type = db.Column(db.String(20), default='banks') # 'banks' أو 'exchange'
    bank_name = db.Column(db.String(150), nullable=False)
    bank_acc = db.Column(db.String(100), nullable=False)
    
    # بيانات النظام
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Supplier {self.trade_name} ({self.sovereign_id})>"
