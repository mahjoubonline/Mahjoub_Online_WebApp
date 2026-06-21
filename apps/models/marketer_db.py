# 📂 apps/models/marketer_db.py
# coding: utf-8

from apps import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Marketer(db.Model, UserMixin):
    __tablename__ = 'marketers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # معلومات إضافية للمسوق
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """تشفير كلمة المرور قبل حفظها"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور عند تسجيل الدخول"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Marketer {self.username}>'
