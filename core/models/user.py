from core import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    موديل المستخدمين - النواة السيادية للهوية الرقمية.
    يدعم تسجيل الدخول باسم المستخدم بالعربي وتعدد الأدوار.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # المعرف الأساسي للدخول (يدعم الأسماء المركبة)
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    # البريد الإلكتروني (اختياري لتجنب أخطاء قاعدة البيانات القديمة)
    email = db.Column(db.String(120), unique=True, nullable=True)
    
    # مفتاح التشفير (يجب أن يكون password_hash تماماً)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # الحوكمة: admin (علي محجوب)، supplier (الموردين)، user (العملاء)
    role = db.Column(db.String(20), nullable=False, default='supplier')
    
    # حالة الحساب السيادية
    is_active_account = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_admin(self):
        """تحقق سريع لصلاحيات الإدارة المركزية"""
        return self.role == 'admin'

    def set_password(self, password):
        """تشفير كلمة المرور قبل التخزين"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """المقارنة الأمنية عند محاولة الولوج"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} - Role: {self.role}>'
