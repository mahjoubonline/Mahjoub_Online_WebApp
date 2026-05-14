from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# استيراد كائن الـ db من ملف الـ models الرئيسي لمشروعك لضمان عدم فصل السيرفر
from apps.models import db  

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    # 1. الحقول الأساسية للمورد ومعرفات النظام
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unified_id = db.Column(db.String(50), unique=True, nullable=False) # المعرف الموحد SUP-WEL-MAH...
    username = db.Column(db.String(50), unique=True, nullable=False)   # اسم مستخدم النظام
    password_hash = db.Column(db.String(255), nullable=False)          # كلمة المرور المشفرة (الهاش)
    
    # 2. بيانات الوصول والتوثيق (الهوية والمستندات)
    identity_type = db.Column(db.String(100), nullable=False)          # نوع الهوية (بطاقة، سجل تجاري...)
    identity_number = db.Column(db.String(100), nullable=False)        # رقم الوثيقة / الهوية
    identity_image = db.Column(db.String(255), nullable=True)          # اسم ملف الصورة المرفوعة في السيرفر
    
    # 3. بيانات المالك والمنشأة
    owner_name = db.Column(db.String(150), nullable=False)             # اسم المالك الكامل
    trade_name = db.Column(db.String(150), unique=True, nullable=False) # الاسم التجاري للمنشأة (فريد)
    shop_phone = db.Column(db.String(20), unique=True, nullable=False)  # رقم هاتف المنشأة (فريد)
    
    # 4. البيانات الجغرافية
    province = db.Column(db.String(100), nullable=False)               # المحافظة
    district = db.Column(db.String(100), nullable=False)               # المديرية
    address = db.Column(db.Text, nullable=False)                       # العنوان بالتفصيل (الحي، الشارع...)
    
    # 5. الربط المالي السيادي والعمليات المالية
    fin_type = db.Column(db.String(50), nullable=False)                # نوع الربط (بنوك / صرافة)
    bank_name = db.Column(db.String(150), nullable=False)              # اسم البنك أو شركة الصرافة
    bank_acc = db.Column(db.String(100), nullable=False)               # رقم الحساب / المحفظة المالية
    
    # 6. تصنيف فئة المورد ونظام المتابعة
    category = db.Column(db.String(100), nullable=False)               # فئة المورد (مورد جملة / تجزئة)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)       # تاريخ ووقت التعميد في النظام
    is_active = db.Column(db.Boolean, default=True)                    # حالة المورد (نشط / موقف)

    # --- ميكانيكيات حماية وتشفير كلمة المرور المؤقتة ---
    def set_password(self, password):
        """توليد هاش وتشفير كلمة المرور بشكل آمن وقوي جداً لمنع الاختراق"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور المدخلة ومقارنتها بالهاش المشفر أثناء تسجيل دخول المورد"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Supplier {self.trade_name} - {self.unified_id}>"
