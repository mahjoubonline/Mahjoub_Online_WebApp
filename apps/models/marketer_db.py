# 📂 apps/models/marketer_db.py (مع التشفير الثنائي للهاتف)
from apps import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from apps.utils.security import AESCipher # استيراد مشفر AES

class Marketer(db.Model, UserMixin):
    __tablename__ = 'marketers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # الهاتف مشفر هنا
    _phone = db.Column('phone', db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    # --- Property لتشفير الهاتف ---
    @property
    def phone(self):
        return AESCipher.decrypt(self._phone) if self._phone else ""

    @phone.setter
    def phone(self, value):
        self._phone = AESCipher.encrypt(str(value))

    # --- تشفير كلمة المرور (Hashing) ---
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
