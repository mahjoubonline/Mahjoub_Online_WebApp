# coding: utf-8
from apps import db
from cryptography.fernet import Fernet
import os

class SupplierProfile(db.Model):
    __tablename__ = 'supplier_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, unique=True, index=True)
    
    # معلومات النشاط
    trade_name = db.Column(db.String(150), index=True) # الاسم التجاري
    email = db.Column(db.String(150), index=True)
    
    # بيانات حساسة (مشفرة بـ AES)
    _bank_account_enc = db.Column(db.String(255), nullable=True) # رقم الحساب البنكي
    _id_number_enc = db.Column(db.String(255), nullable=True)    # رقم الهوية
    
    # العنوان التفصيلي (لأغراض لوجستية)
    governorate = db.Column(db.String(100), index=True) # المحافظة
    city = db.Column(db.String(100), index=True)        # المديرية/المدينة
    
    # الربط
    user = db.relationship('Supplier', back_populates='supplier_profile')

    # --- نظام التشفير ---
    @staticmethod
    def _get_key():
        return os.environ.get('ENCRYPTION_KEY', 'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq=').encode()

    @property
    def bank_account(self):
        try:
            return Fernet(self._get_key()).decrypt(self._bank_account_enc.encode()).decode()
        except: return None

    @bank_account.setter
    def bank_account(self, value):
        self._bank_account_enc = Fernet(self._get_key()).encrypt(str(value).encode()).decode()

    def __repr__(self):
        return f'<Profile {self.trade_name}>'
