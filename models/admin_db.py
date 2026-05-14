# coding: utf-8
# ملف: models/admin_db.py
# الغرض: تعريف هيكل بيانات المسؤولين في قاعدة البيانات

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# إنشاء كائن قاعدة البيانات ليتم استخدامه في كامل المشروع
db = SQLAlchemy()

# 🛡️ الجزء الأهم: تعريف كلاس AdminUser
# يجب أن يكون الاسم "AdminUser" تماماً كما هو مكتوب أدناه (حساس لحالة الأحرف)
class AdminUser(db.Model, UserMixin):
    """
    نموذج يمثل جدول المسؤولين في قاعدة البيانات.
    """
    __tablename__ = 'admin_users' # اسم الجدول في قاعدة البيانات

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
