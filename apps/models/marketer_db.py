# coding: utf-8
# 📂 apps/models/marketer_db.py - نظام المسوقين السيادي (مؤمن ومفهرس)

from apps.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from apps.utils.security import AESCipher

class Marketer(db.Model, UserMixin):
    __tablename__ = 'marketers'

    id = db.Column(db.Integer, primary_key=True)
    
    # الفهارس لسرعة الوصول (index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # الهاتف المشفر
    _phone = db.Column('phone', db.String(255), nullable=True)
    
    # ⚡ حقل البحث السريع (الفهرس) للتحمل العالي
    phone_index = db.Column(db.String(50), index=True, nullable=True)
    
    is_active = db.Column(db.Boolean, default=True, index=True)

    # --- Property لتشفير وفك تشفير الهاتف ---
    @property
    def phone(self):
        return AESCipher.decrypt(self._phone) if self._phone else ""

    @phone.setter
    def phone(self, value):
        if value:
            clean_phone = "".join(str(value).split())
            self._phone = AESCipher.encrypt(clean_phone)
            # تحديث حقل الفهرسة للبحث السريع
            self.phone_index = clean_phone
        else:
            self._phone = None
            self.phone_index = None

    # --- تشفير كلمة المرور (Hashing) ---
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
