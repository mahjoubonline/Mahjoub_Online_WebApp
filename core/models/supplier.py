from core import db
from datetime import datetime

class Supplier(db.Model):
    # تحديد اسم الجدول ليتطابق مع قاعدة بيانات "محجوب أونلاين"
    __tablename__ = 'suppliers'
    
    # المعرف التسلسلي الداخلي لقاعدة البيانات
    id = db.Column(db.Integer, primary_key=True)
    
    # الربط مع حساب المستخدم الأساسي
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # --- الهوية السيادية (MAH-XXXX) ---
    # هذا الحقل هو الذي حل مشكلة الخطأ "vendor_uid"
    vendor_uid = db.Column(db.String(100), unique=True, nullable=True)
    
    # --- البيانات التجارية ---
    owner_name = db.Column(db.String(150)) # اسم المالك
    trade_name = db.Column(db.String(150), nullable=False) # الاسم التجاري (بديل لـ store_name)
    phone = db.Column(db.String(20))
    activity_type = db.Column(db.String(100)) # نوع النشاط
    
    # --- المحفظة المالية الموحدة (W-MAH-XXXX) ---
    e_wallet = db.Column(db.String(100), unique=True)
    
    # --- الأرصدة السيادية الثلاثة ---
    balance_yer = db.Column(db.Float, default=0.0) # ريال يمني
    balance_sar = db.Column(db.Float, default=0.0) # ريال سعودي
    balance_usd = db.Column(db.Float, default=0.0) # دولار أمريكي
    
    # --- الموقع الجغرافي (نطاق العمل: عدن، الخوخة، المخا، حيس) ---
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    location = db.Column(db.String(200)) # العنوان التفصيلي
    
    # --- بيانات التحقق والتوثيق ---
    id_type = db.Column(db.String(50)) # نوع الهوية
    id_card_number = db.Column(db.String(100)) # رقم الهوية
    is_verified = db.Column(db.Boolean, default=False)
    
    # --- البيانات البنكية ---
    bank_name = db.Column(db.String(150))
    bank_acc = db.Column(db.String(100))
    fin_type = db.Column(db.String(50)) # فئة التاجر المالية
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --- العلاقات اللوجستية ---
    # الربط مع جدول المنتجات (Product)
    products = db.relationship('Product', backref='owner_supplier', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Supplier {self.trade_name} - UID: {self.vendor_uid}>"
