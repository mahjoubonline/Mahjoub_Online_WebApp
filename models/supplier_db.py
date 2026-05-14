from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# إنشاء كائن الـ db محلياً هنا لمنع خطأ ModuleNotFoundError نهائياً
db = SQLAlchemy()

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    # 1. الحقول الأساسية للمورد ومعرفات النظام
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sovereign_id = db.Column(db.String(50), unique=True, nullable=False) # المعرف الموحد المتوافق مع الكود الشغال
    username = db.Column(db.String(50), unique=True, nullable=False)   # اسم مستخدم النظام
    password = db.Column(db.String(255), nullable=False)                # حقل كلمة المرور المباشر المستقر
    category = db.Column(db.String(100), nullable=False)               # فئة المورد (مورد جملة / تجزئة)
    
    # 2. بيانات المالك والمنشأة
    owner_name = db.Column(db.String(150), nullable=False)             # اسم المالك الكامل
    trade_name = db.Column(db.String(150), unique=True, nullable=False) # الاسم التجاري للمنشأة
    shop_phone = db.Column(db.String(20), unique=True, nullable=False)  # رقم هاتف المنشأة
    
    # 3. البيانات الجغرافية
    province = db.Column(db.String(100), nullable=False)               # المحافظة
    district = db.Column(db.String(100), nullable=False)               # المديرية
    address_detail = db.Column(db.Text, nullable=False)                # العنوان بالتفصيل
    
    # 4. الربط المالي السيادي
    finance_type = db.Column(db.String(50), nullable=False)            # نوع الربط (بنوك / صرافة)
    bank_name = db.Column(db.String(150), nullable=False)              # اسم البنك أو شركة الصرافة
    bank_account = db.Column(db.String(100), nullable=False)           # رقم الحساب / المحفظة المالية
    
    # 5. التوقيت والحالة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)       # تاريخ ووقت التعميد في النظام
    is_active = db.Column(db.Boolean, default=True)                    # حالة المورد (نشط / موقف)

    def __repr__(self):
        return f"<Supplier {self.trade_name} - {self.sovereign_id}>"
