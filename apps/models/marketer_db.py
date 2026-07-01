# coding: utf-8
# 📂 apps/models/marketer_db.py

import os
from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash

class Marketer(db.Model, UserMixin):
    __tablename__ = 'marketers'

    __table_args__ = (
        db.Index('idx_mkt_name', 'full_name'),
        db.Index('idx_mkt_code', 'marketing_code'),
        db.Index('idx_mkt_active', 'is_active'),
        db.Index('idx_mkt_refs', 'total_referrals'),
        db.Index('idx_mkt_created', 'created_at'),
        {'extend_existing': True}
    )

    # المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    marketing_code = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    _phone_enc = db.Column(db.String(255), nullable=True) 
    
    # حالات التشغيل والتحصيلات
    is_active = db.Column(db.Boolean, default=True)
    total_referrals = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات (لربط المسوق بطلباته مباشرة)
    orders = db.relationship('Order', back_populates='marketer', lazy='dynamic')

    # --- نظام التشفير (AES) للرقم ---
    @staticmethod
    def _get_key():
        key = os.environ.get('ENCRYPTION_KEY')
        return key.encode() if key else b'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq='

    @property
    def phone(self):
        if not self._phone_enc: return None
        try:
            return Fernet(self._get_key()).decrypt(self._phone_enc.encode()).decode()
        except: return None

    @phone.setter
    def phone(self, value):
        if value:
            self._phone_enc = Fernet(self._get_key()).encrypt(str(value).encode()).decode()

    # --- طرق تسجيل الدخول وتأمين كلمة المرور ---
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- دالة مساعدة لحساب إجمالي العمولات لاحقاً ---
    def get_total_commissions(self):
        # يمكن توسيع هذه الدالة لاحقاً لربطها بجدول الحركات المالية
        return 0.0

    def __repr__(self):
        return f'<Marketer {self.full_name} | Code: {self.marketing_code}>'
