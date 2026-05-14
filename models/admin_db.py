# coding: utf-8
# - استيراد المكتبات المطلوبة للنموذج
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# تهيئة كائن قاعدة البيانات
db = SQLAlchemy()

# 🛡️ تعريف كلاس المسؤول - تأكد من تطابق الاسم تماماً
class AdminUser(db.Model, UserMixin):
    """
    نموذج مستخدم المسؤول (AdminUser):
    يتم استيراده بواسطة run.py لتأمين لوحة التحكم.
    """
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<AdminUser {self.username}>'
