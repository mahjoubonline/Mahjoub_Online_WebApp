import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# --- بروتوكول تثبيت المسارات (Railway Patch) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core.extensions import db
except (ImportError, ModuleNotFoundError):
    from ..extensions import db

class Supplier(db.Model):
    """
    نموذج الموردين المطور - منظومة محجوب أونلاين v3.5
    نظام الحوكمة السيادي وإدارة الأرصدة المتعددة
    """
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # البيانات التعريفية
    owner_name = db.Column(db.String(150), nullable=True)
    trade_name = db.Column(db.String(150), nullable=True)
    activity_type = db.Column(db.String(100), nullable=True) 
    
    # الجغرافيا والتصنيف
    tier = db.Column(db.String(50), default='مبتدئ') # [مبتدئ، محترف، سيادي]
    province = db.Column(db.String(100), nullable=True) 
    district = db.Column(db.String(100), nullable=True) 
    address_detail = db.Column(db.Text, nullable=True) 
    
    # بيانات الاتصال والتوثيق
    id_type = db.Column(db.String(50), nullable=True) 
    id_card_number = db.Column(db.String(50), nullable=True) 
    phone = db.Column(db.String(20), nullable=True) 
    email = db.Column(db.String(120), nullable=True) # مضاف للاتصال الرسمي
    
    # --- النظام المالي الموحد (Multi-Currency Vault) ---
    e_wallet = db.Column(db.String(100), unique=True, nullable=True) # WAL_MAH_963...
    sovereign_id = db.Column(db.String(100), unique=True, nullable=True) # SUP_MAH_963...
    
    # الأرصدة السيادية
    balance_yer = db.Column(db.Numeric(20, 2), default=0.00) 
    balance_sar = db.Column(db.Numeric(20, 2), default=0.00) 
    balance_usd = db.Column(db.Numeric(20, 2), default=0.00) 
    
    # البيانات البنكية
    bank_name = db.Column(db.String(100), nullable=True) 
    bank_acc = db.Column(db.String(100), nullable=True) 
    
    # الحالة والتحكم
    status = db.Column(db.String(20), default='active') # [active, suspended, audit, banned]
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # --- العلاقات (Relationships) ---
    staff = db.relationship('SupplierStaff', backref='employer', lazy=True, cascade="all, delete-orphan")

    # --- بروتوكولات الحماية والتعميد ---

    def set_password(self, password):
        """تشفير كلمة المرور بنظام الترسانة الرقمية محجوب"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من مطابقة مفتاح الدخول"""
        return check_password_hash(self.password_hash, password)

    def mint_sovereign_id(self):
        """
        توليد المعرف السيادي الموحد بناءً على النمط التسلسلي الجديد 963
        مثال: المورد 1 يصبح 9631، المورد 2 يصبح 9632
        """
        if self.id:
            # التعديل المطلوب: دمج الـ 963 مع الـ ID مباشرة بدون أصفار حشو اختيارية ليكون (9631, 9632...)
            tag = f"963{self.id}" 
            self.e_wallet = f"WAL_MAH_{tag}"
            self.sovereign_id = f"SUP_MAH_{tag}"
            return self.sovereign_id
        return None

    def to_dict(self, include_staff=False):
        """تحويل الكيان إلى قاموس متوافق مع JSON للواجهات الذكية"""
        data = {
            "id": self.id,
            "sovereign_id": self.sovereign_id or f"SUP_{self.id}#",
            "username": self.username,
            "trade_name": self.trade_name or "غير مسمى",
            "owner_name": self.owner_name or "غير محدد",
            "phone": self.phone or "N/A",
            "province": self.province or "-",
            "district": self.district or "-",
            "tier": self.tier,
            "status": self.status,
            "balance_yer": float(self.balance_yer),
            "balance_sar": float(self.balance_sar),
            "balance_usd": float(self.balance_usd),
            "e_wallet": self.e_wallet,
            "created_at": self.created_at.strftime('%Y-%m-%d')
        }
        
        if include_staff:
            data['staff'] = [s.to_dict() for s in self.staff]
            
        return data

    def __repr__(self):
        return f'<Supplier {self.trade_name} | Sovereign_ID: {self.sovereign_id}>'

class SupplierStaff(db.Model):
    __tablename__ = 'supplier_staff'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50)) # محاسب، مندوب، مدير فرع
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "phone": self.phone,
            "is_active": self.is_active
        }
