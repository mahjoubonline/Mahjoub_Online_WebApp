# coding: utf-8
# 📂 apps/models/admin_db.py - نموذج المدير (مُشفر تلقائياً)

from apps.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from apps.utils.security import AESCipher
from datetime import datetime

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='Admin') # Owner, Admin
    
    # حقل مشفر للهاتف
    _phone_number_enc = db.Column(db.String(255), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    failed_attempts = db.Column(db.Integer, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)

    # 🔑 التشفير التلقائي للهاتف
    @property
    def phone_number(self):
        if self._phone_number_enc:
            return AESCipher.decrypt(self._phone_number_enc)
        return None

    @phone_number.setter
    def phone_number(self, value):
        if value:
            self._phone_number_enc = AESCipher.encrypt(str(value))
        else:
            self._phone_number_enc = None

    # 🔒 إدارة كلمة المرور
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
