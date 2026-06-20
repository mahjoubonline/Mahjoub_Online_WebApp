# coding: utf-8
# 📂 apps/models/supplier_db.py - الكيان السيادي لبيانات الموردين وحوكمة الصلاحيات

from apps.extensions import db
from flask_login import UserMixin
from datetime import datetime
from apps.utils.security import AESCipher # استيراد أداة التشفير

class Supplier(db.Model, UserMixin):
    """
    الجدول الأساسي والمحكم لإدارة كيانات الموردين وصلاحياتهم الرقمية.
    تم إضافة حقل country_code لضمان دقة الاتصال الدولي والتحقق عبر الواتساب.
    """
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    
    # 🔗 الجسر السيادي
    admin_user_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), unique=True, nullable=True)

    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    trade_name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)
    
    # حقول مشفرة بـ AES-256
    _owner_phone = db.Column('owner_phone', db.String(255), nullable=True)
    _country_code = db.Column('country_code', db.String(10), nullable=True) # حقل منفصل لرمز الدولة
    _owner_email = db.Column('owner_email', db.String(255), nullable=True)
    
    # الأكواد السيادية
    supplier_code = db.Column(db.String(50), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 العلاقات البرمجية
    wallet = db.relationship('SupplierWallet', back_populates='supplier', uselist=False, lazy=True, cascade="all, delete-orphan")

    # --- Property للتحكم في الهاتف ورمز الدولة ---
    @property
    def full_phone(self):
        """إرجاع الرقم الكامل المدمج (رمز الدولة + الرقم)"""
        phone = self.owner_phone # استدعاء الـ property الخاص بفك التشفير
        return f"{self._country_code}{phone}" if self._country_code and phone else None

    @property
    def owner_phone(self):
        """فك تشفير الرقم الأساسي"""
        try:
            return AESCipher.decrypt(self._owner_phone) if self._owner_phone else None
        except Exception:
            return None

    @owner_phone.setter
    def owner_phone(self, value):
        """تشفير الهاتف قبل التخزين وتنظيفه من المسافات"""
        if value:
            clean_phone = "".join(value.split())
            self._owner_phone = AESCipher.encrypt(clean_phone)
        else:
            self._owner_phone = None

    # --- Property للتحكم في البريد الإلكتروني ---
    @property
    def owner_email(self):
        try:
            return AESCipher.decrypt(self._owner_email) if self._owner_email else None
        except Exception:
            return None

    @owner_email.setter
    def owner_email(self, value):
        if value:
            self._owner_email = AESCipher.encrypt(value)
        else:
            self._owner_email = None

    def generate_codes(self):
        if not self.supplier_code and self.id:
            self.supplier_code = f"SUP-MAH{self.id}x{datetime.utcnow().strftime('%y%m')}"
            
    def __repr__(self):
        return f"<Supplier [{self.supplier_code}] -> {self.trade_name}>"
