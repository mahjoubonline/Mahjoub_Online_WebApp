# core/models/supplier.py
from datetime import datetime
from flask_login import UserMixin
from core import db

class Supplier(db.Model, UserMixin):
    """ 
    موديل المورد السيادي: المرجع الأساسي لهيكلة البيانات والولوج.
    يدعم الهوية الرقمية المستقلة والخزينة الثلاثية (YER, SAR, USD).
    """
    __tablename__ = 'suppliers'
    
    # --- المعرفات والهوية الرقمية ---
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True) # المعرف التلقائي مثل SUP_1#
    username = db.Column(db.String(100), unique=True, nullable=False) # اسم المستخدم للدخول
    password_hash = db.Column(db.String(255), nullable=False) # كلمة المرور المشفرة (5 أرقام)
    
    # --- البيانات الأساسية (واجهة التعميد الملكية) ---
    trade_name = db.Column(db.String(150), nullable=False) # الاسم التجاري للمحل/الشركة
    owner_name = db.Column(db.String(150)) # اسم المالك الرسمي
    activity_type = db.Column(db.String(100)) # نوع النشاط (إلكترونيات، ملابس، إلخ)
    identity_type = db.Column(db.String(50)) # نوع الهوية (شخصية، عائلية، جواز)
    
    # --- النطاق الجغرافي والاتصال ---
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    address_detail = db.Column(db.Text) # العنوان الدقيق
    phone = db.Column(db.String(20)) # رقم الهاتف للتواصل
    
    # --- الربط المالي (الخزينة السيادية الثلاثية) ---
    bank_name = db.Column(db.String(150)) # اسم البنك أو الكريمي
    bank_acc = db.Column(db.String(100)) # رقم الحساب البنكي
    balance_yer = db.Column(db.Float, default=0.0) # الرصيد بالريال اليمني
    balance_sar = db.Column(db.Float, default=0.0) # الرصيد بالريال السعودي
    balance_usd = db.Column(db.Float, default=0.0) # الرصيد بالدولار الأمريكي
    
    # --- الحالة والتوثيق الزمني ---
    status = db.Column(db.String(20), default='active') # نشط، موقف، محظور
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Supplier {self.trade_name} | {self.sovereign_id}>"

class SupplierStaff(db.Model):
    """ طاقم العمل التابع للمورد - لإدارة الموظفين والصلاحيات الفرعية """
    __tablename__ = 'supplier_staff'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100)) # مدير، مندوب، محاسب
    status = db.Column(db.String(20), default='active')
    
    # ربط العلاقة السيادية مع المورد الأساسي
    supplier = db.relationship('Supplier', backref=db.backref('staff_members', lazy=True))
