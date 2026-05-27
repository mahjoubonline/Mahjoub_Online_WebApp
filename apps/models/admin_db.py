# coding: utf-8
# 🛡️ جدول إدارة النظام المشفر - منصة محجوب أونلاين 2026
import os
from apps.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from apps.utils.security import AESCipher

# تهيئة مشفر البيانات
cipher = AESCipher(os.getenv('ENCRYPTION_KEY', 'your-32-byte-key-here-must-be-secure'))

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    
    # حقول مشفرة (تخزين Ciphertext)
    _full_name = db.Column(db.String(255), nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    role = db.Column(db.String(50), default='admin')
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --- خصائص التشفير ---

    @property
    def full_name(self): return cipher.decrypt(self._full_name)
    @full_name.setter
    def full_name(self, value): self._full_name = cipher.encrypt(str(value))

    @property
    def email(self): return cipher.decrypt(self._email)
    @email.setter
    def email(self, value): self._email = cipher.encrypt(str(value))

    # --- طرق الأمان ---

    def set_password(self, password):
        """تشفير كلمة المرور (Hash) - تظل كما هي لأنها محمية بـ Werkzeug"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
