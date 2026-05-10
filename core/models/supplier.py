# core/models/supplier.py
from datetime import datetime
from flask_login import UserMixin
# نستخدم الاستيراد المباشر من extensions لضمان عدم حدوث تضارب (Circular Import)
from core.extensions import db

class Supplier(db.Model, UserMixin):
    """ 
    موديل المورد السيادي: المرجع الأساسي لهيكلة البيانات والولوج.
    يدعم الهوية الرقمية (Username/Password) والمحفظة الثلاثية السيادية.
    """
    __tablename__ = 'suppliers'
    
    # --- المعرفات والهوية السيادية ---
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True) # المعرف التلقائي مثل SUP_1#
    username = db.Column(db.String(100), unique=True, nullable=False) # اسم المستخدم للدخول
    password_hash = db.Column(db.String(255), nullable=False) # كلمة المرور المشفرة
    
    # --- البيانات الأساسية والتوثيق الملكي ---
    trade_name = db.Column(db.String(150), nullable=False) # الاسم التجاري للمنشأة
    owner_name = db.Column(db.String(150)) # اسم المالك الرسمي
    activity_type = db.Column(db.String(100)) # نوع النشاط (إلكترونيات، مواد غذائية، إلخ)
    identity_type = db.Column(db.String(50)) # نوع الهوية المرفقة
    
    # --- النطاق الجغرافي والاتصال ---
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    address_detail = db.Column(db.Text) # العنوان الدقيق والمعالم
    phone = db.Column(db.String(20)) # رقم الهاتف (الواتساب)
    
    # --- الربط المالي (الخزينة السيادية الثلاثية) ---
    bank_name = db.Column(db.String(150)) # اسم البنك أو شركة الصرافة
    bank_acc = db.Column(db.String(100)) # رقم الحساب المعتمد
    balance_yer = db.Column(db.Float, default=0.0) # الرصيد بالريال اليمني
    balance_sar = db.Column(db.Float, default=0.0) # الرصيد بالريال السعودي
    balance_usd = db.Column(db.Float, default=0.0) # الرصيد بالدولار الأمريكي
    
    # --- الحالة والتوثيق الزمني ---
    status = db.Column(db.String(20), default='active') # نشط / موقف / محظور
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Supplier {self.trade_name} | {self.sovereign_id}>"

class SupplierStaff(db.Model):
    """ طاقم العمل التابع للمورد - لإدارة الصلاحيات الفرعية والموظفين """
    __tablename__ = 'supplier_staff'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100)) # مدير، مندوب، محاسب
    status = db.Column(db.String(20), default='active')
    
    # ربط العلاقة السيادية مع المورد الأساسي (Back-reference)
    supplier = db.relationship('Supplier', backref=db.backref('staff_members', lazy=True))
