# core/models/user.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core.extensions import db 

class User(db.Model, UserMixin):
    """ 
    موديل الهوية السيادية: يمثل المستخدمين (المدراء، الموظفين) 
    وهو الركيزة الأساسية لنظام الحماية في محجوب أونلاين.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # تصنيف الرتبة (admin, staff, supplier_admin, employee)
    # ملاحظة: تم توسيع الرتب لتشمل إدارة الموردين
    role = db.Column(db.String(50), default='admin') 
    
    # الربط مع المورد (يكون NULL إذا كان المستخدم أدمن للنظام العام)
    # هذا الحقل هو "جسر العبور" لنظام الموظفين الجديد
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # الحقول الإضافية للهوية
    full_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    
    # الحالة الزمنية والأمنية
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """تشفير كلمة المرور وتأمينها في الخزينة الرقمية"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من الهوية الرقمية عند تسجيل الدخول"""
        return check_password_hash(self.password_hash, password)

    @property
    def is_supplier_staff(self):
        """دالة ذكية للتحقق ما إذا كان المستخدم يتبع مورد معين"""
        return self.supplier_id is not None

    def to_dict(self):
        """تحويل بيانات المستخدم لقاموس لسهولة استخدامها في الواجهات"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "supplier_id": self.supplier_id,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<User {self.username} | Role: {self.role} | Supplier: {self.supplier_id}>"
