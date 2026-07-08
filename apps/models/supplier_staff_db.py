# coding: utf-8
import os
from datetime import datetime
from cryptography.fernet import Fernet
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from apps.extensions import db

class SupplierStaff(db.Model, UserMixin):
    __tablename__ = 'supplier_staff'
    
    # 1. الأعمدة
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    
    # التشفير السيادي للهاتف
    _phone_enc = db.Column(db.String(255), nullable=False) 
    phone = db.Column(db.String(20), nullable=False) # للبحث السريع
    
    email = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='worker')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 2. الفهارس للسرعة العالية
    __table_args__ = (
        db.Index('idx_staff_supplier_id', 'supplier_id'),
        db.Index('idx_staff_username', 'username'),
        db.Index('idx_staff_phone', 'phone'),
        db.Index('idx_staff_role', 'role'),
        db.Index('idx_staff_active', 'is_active'),
        {'extend_existing': True}
    )

    # 3. العلاقات
    supplier = db.relationship('Supplier', back_populates='staff_members')

    # 4. التشفير (Fernet للهاتف + PBKDF2 لكلمة المرور)
    @staticmethod
    def _get_key():
        key = os.environ.get('ENCRYPTION_KEY', 'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq=')
        return key.encode()

    @property
    def phone_number(self):
        try:
            return Fernet(self._get_key()).decrypt(self._phone_enc.encode()).decode()
        except: return None

    @phone_number.setter
    def phone_number(self, value):
        if value:
            self._phone_enc = Fernet(self._get_key()).encrypt(str(value).encode()).decode()
            self.phone = str(value)[-9:] # لتسهيل البحث

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<SupplierStaff {self.username} | Role: {self.role}>'
