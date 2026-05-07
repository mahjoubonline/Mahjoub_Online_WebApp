import os
import sys
from datetime import datetime

# --- بروتوكول تثبيت المسارات (Railway Patch) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# استيراد db باستخدام مسارات مرنة لضمان الاستقرار على Railway
try:
    from core.extensions import db
except (ImportError, ModuleNotFoundError):
    try:
        from extensions import db
    except (ImportError, ModuleNotFoundError):
        from ..extensions import db

class Supplier(db.Model):
    """
    نموذج الموردين المعتمد لمنظومة محجوب أونلاين
    تم تعديله ليتوافق مع صرامة Postgres على Railway
    """
    __tablename__ = 'suppliers'
    
    # --- المعرفات الأساسية ---
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) 
    
    # --- البيانات الشخصية والتجارية ---
    owner_name = db.Column(db.String(150), nullable=True) # تم تعديله ليكون اختيارياً 
    trade_name = db.Column(db.String(150), nullable=True) # تم تعديله ليكون اختيارياً
    
    # الحل الجذري لمشكلة السجلات: جعل نوع النشاط يقبل القيم الفارغة
    activity_type = db.Column(db.String(100), nullable=True) 
    
    # --- الرتبة الإدارية والانتشار الجغرافي ---
    tier = db.Column(db.String(50), default='مبتدئ') 
    province = db.Column(db.String(100), nullable=True) 
    district = db.Column(db.String(100), nullable=True) 
    address_detail = db.Column(db.Text, nullable=True) 
    
    # --- بيانات التوثيق والاتصال ---
    id_type = db.Column(db.String(50), nullable=True) 
    id_card_number = db.Column(db.String(50), nullable=True) 
    phone = db.Column(db.String(20), nullable=True) 
    
    # --- الربط المالي ---
    e_wallet = db.Column(db.String(100), unique=True, nullable=True)
    bank_name = db.Column(db.String(100), nullable=True) 
    bank_acc = db.Column(db.String(100), nullable=True) 
    
    # --- حالة الحساب السحابي ---
    status = db.Column(db.String(20), default='active') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """تحويل سجل المورد إلى قاموس لتمكين محرك البحث من عرض النتائج"""
        return {
            "id": self.id,
            "trade_name": self.trade_name,
            "phone": self.phone,
            "province": self.province,
            "district": self.district,
            "activity_type": self.activity_type,
            "tier": self.tier,
            "status": self.status,
            "e_wallet": self.e_wallet
        }

    def __repr__(self):
        return f'<Supplier {self.trade_name if self.trade_name else self.username} - {self.tier}>'
