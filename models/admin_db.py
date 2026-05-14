# coding: utf-8
# ملف: models/admin_db.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# تهيئة كائن قاعدة البيانات
db = SQLAlchemy()

# 🛡️ الكلاس الذي يبحث عنه نظام التشغيل (تأكد من كتابته بهذا الشكل)
class AdminUser(db.Model, UserMixin):
    """
    نموذج مستخدم المسؤول لمنصة محجوب أونلاين.
    """
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<AdminUser {self.username}>'
