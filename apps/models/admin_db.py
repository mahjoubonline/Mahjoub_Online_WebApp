# coding: utf-8
# 📂 apps/models/admin_db.py - نظام الهوية المحصن

from apps.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), default='admin')
    is_active = db.Column(db.Boolean, default=True)
    
    failed_attempts = db.Column(db.Integer, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        try:
            self.password_hash = generate_password_hash(password)
        except Exception:
            self.password_hash = "INVALID_HASH"

    def check_password(self, password):
        """التحقق المحصن: يمنع الانهيار حتى لو فسدت البيانات"""
        try:
            if not self.password_hash or self.password_hash == "INVALID_HASH":
                return False
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            print(f"⚠️ خطأ في التحقق من كلمة المرور: {e}")
            return False

    def is_locked(self):
        try:
            if self.lock_until and datetime.utcnow() < self.lock_until:
                return True
        except:
            pass
        return False

    def increment_failed_attempts(self):
        """زيادة العداد بأمان"""
        try:
            self.failed_attempts = (self.failed_attempts or 0) + 1
            delay = (self.failed_attempts // 5) + 1 
            self.lock_until = datetime.utcnow() + timedelta(minutes=delay)
            # تم تحويل الحفظ إلى الـ Route لضمان التحكم في الـ session
        except Exception as e:
            print(f"⚠️ خطأ عند تسجيل فشل الدخول: {e}")

    def reset_failed_attempts(self):
        try:
            self.failed_attempts = 0
            self.lock_until = None
        except Exception as e:
            print(f"⚠️ خطأ عند إعادة ضبط العداد: {e}")

    def __repr__(self):
        return f'<AdminUser {self.username}>'
