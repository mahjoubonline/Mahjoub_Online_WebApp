from core import db
from datetime import datetime
from flask_login import UserMixin

# 1. جدول الإدارة العليا (القائد علي ومساعدوه)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 2. جدول شركاء النجاح (الموردين) - نظام التعميد السيادي
class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    
    # بيانات الحساب والنشاط (من واجهة التعميد)
    name = db.Column(db.String(100), unique=True, nullable=False) # اسم المستخدم للدخول
    password = db.Column(db.String(200), nullable=True) 
    activity_type = db.Column(db.String(100)) # نوع النشاط التجاري
    
    # بيانات المنشأة والموقع
    trade_name = db.Column(db.String(200)) # الاسم التجاري
    full_name = db.Column(db.String(200))  # اسم المالك الكامل
    id_type = db.Column(db.String(50))     # نوع الهوية
    province = db.Column(db.String(100))   # المحافظة
    district = db.Column(db.String(100))   # المديرية
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    # الربط المالي (بنوك / صرافة)
    fin_type = db.Column(db.String(50))    # بنوك أو صرافة
    bank_name = db.Column(db.String(100))  # اسم الجهة المالية
    bank_acc = db.Column(db.String(100))   # رقم الحساب / الآيبان
    
    # محفظة المورد (الرصيد المالي)
    wallet_balance = db.Column(db.Float, default=0.0) 
    
    # الأرشفة والتوثيق
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='supplier_owner', lazy=True)

    @property
    def sovereign_id(self):
        """
        توليد الرقم السيادي للمحفظة
        يبدأ من الأساس الثابت MAH-9046 ويزيد رقمياً مع كل مورد جديد
        """
        base_sovereign = 9046
        # إذا كان المعرف 1 يصبح الرقم 90461، وإذا كان 2 يصبح 90462 وهكذا
        return f"MAH-{base_sovereign}{self.id}"

# 3. جدول ترسانة المنتجات - مركز التحكم في البيانات
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    
    # السياسة المالية
    original_price = db.Column(db.Float, nullable=False, default=0.0) # سعر التكلفة من المورد
    sale_price = db.Column(db.Float, nullable=False, default=0.0)     # سعر البيع (تحدده الإدارة)
    
    # التحكم في الحالة والمزامنة
    status = db.Column(db.String(50), default='pending') 
    is_synced = db.Column(db.Boolean, default=False) 
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # يظهر المنتج في السجلات مرتبطاً بالرقم السيادي للمورد
        base_sovereign = 9046
        return f'<Product {self.name} | Wallet: MAH-{base_sovereign}{self.supplier_id}>'
