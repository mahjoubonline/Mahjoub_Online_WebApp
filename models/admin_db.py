from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# تعريف كائن قاعدة البيانات المركزي
db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    """
    موديل المسؤولين (Admins): يمثل الأشخاص الذين لديهم صلاحية 
    الدخول إلى لوحة تحكم محجوب أونلاين.
    """
    __tablename__ = 'admins'

    # الحقول الأساسية للهوية
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # بيانات التعريف الشخصية
    full_name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default='super_admin')  # تحديد الصلاحيات
    
    # بيانات النشاط والزمن
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """
        تشفير كلمة المرور قبل حفظها في قاعدة البيانات لضمان الأمان السيادي.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        التحقق من مطابقة كلمة المرور المدخلة مع التشفير المخزن.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'
