# core/models/user.py
from core import db # تم تعديل الاستيراد ليتوافق مع هيكل مشروعك
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    نواة الهوية الرقمية - v4.1 (تم الإصلاح لضمان الاستقرار)
    تتحكم في صلاحيات الوصول لمركز قيادة محجوب أونلاين.
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True) 
    password_hash = db.Column(db.String(256), nullable=False)
    
    # الأدوار السيادية: [admin, staff, supplier, customer]
    role = db.Column(db.String(50), default='customer') 
    is_active_account = db.Column(db.Boolean, default=True)

    # --- الإصلاح الجوهري (الجسر بين المستخدم والمورد) ---
    
    # 1. إضافة المفتاح الأجنبي لربط المستخدم بملف المورد إذا كان دوره 'supplier'
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)

    # 2. العلاقة العكسية للوصول لبيانات المورد من كائن المستخدم
    # uselist=False تعني أن كل مستخدم له ملف مورد واحد فقط
    supplier_profile = db.relationship('Supplier', backref='user_account', uselist=False)

    def set_password(self, password):
        """تشفير سيادي عالي الطاقة ببروتوكول PBKDF2"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من مطابقة البصمة الرقمية لكلمة المرور"""
        if not self.password_hash: return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        """تفعيل الحصانة البرمجية لـ Flask-Login"""
        return self.is_active_account

    def to_dict(self):
        """تجهيز البيانات لعمليات الـ API والجافا سكريبت"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "is_active": self.is_active_account,
            "supplier_id": self.supplier_id
        }

    def __repr__(self):
        return f"<User {self.username} | Role: {self.role}>"
