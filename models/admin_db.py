from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# تعريف كائن قاعدة البيانات (المرجع الوحيد للمشروع بالكامل)
db = SQLAlchemy()

class AdminUser(db.Model):
    """
    جدول بيانات المسؤولين (الإدارة العليا) في منظومة محجوب أونلاين.
    يستخدم هذا الجدول لإدارة الدخول إلى لوحة التحكم السيادية.
    """
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) # اسم المستخدم (مثل ali_mahjoub)
    password_hash = db.Column(db.String(255), nullable=False)        # كلمة السر المشفرة لحماية السيادة
    full_name = db.Column(db.String(100))                           # الاسم الكامل (مثل علي محجوب)
    role = db.Column(db.String(20), default='founder')              # الدور القيادي (مؤسس النظام)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)    # توثيق زمني لآخر دخول

    def set_password(self, password):
        """تشفير كلمة السر لضمان أمن البيانات"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من مطابقة كلمة السر عند محاولة الولوج"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
