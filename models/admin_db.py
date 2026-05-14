# coding: utf-8
# 🌟 استيراد المكتبات الأساسية لإدارة قاعدة البيانات وجلسات المستخدمين
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 🗄️ تهيئة كائن قاعدة البيانات المركزي
db = SQLAlchemy()

class AdminUser(db.Model, UserMixin):
    """
    موديل المسؤولين (AdminUser):
    تم تغيير الاسم إلى AdminUser لحل مشكلة ImportError الظاهرة في image_783ed5.png.
    هذا الكلاس يمثل جدول المسؤولين في لوحة تحكم محجوب أونلاين.
    """
    __tablename__ = 'admin_users'

    # 🔑 الهوية الرقمية (Primary Key)
    id = db.Column(db.Integer, primary_key=True)
    
    # 👤 بيانات الدخول والتعريف
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # لتخزين كلمة المرور مشفرة
    
    # 📜 بيانات إضافية للمسؤول
    full_name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default='super_admin') 
    
    # 🕒 سجلات النشاط (التوقيت العالمي ليتناسب مع خوادم Railway)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """
        دالة التشفير: تحويل كلمة المرور الصريحة إلى هاش (Hash) غير قابل للقراءة.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        دالة التحقق: مقارنة كلمة المرور المدخلة بالتشفير المخزن.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
