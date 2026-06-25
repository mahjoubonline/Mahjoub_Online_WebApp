# coding: utf-8
# 📂 apps/models/wallet_db.py

from apps.extensions import db
from cryptography.fernet import Fernet
import os
from datetime import datetime

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'

    # 1. المعرفات والفهرسة
    id = db.Column(db.Integer, primary_key=True)
    wallet_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, unique=True, index=True)
    
    # 2. الأرصدة (الأعمدة الجديدة للعملات الثلاث)
    balance_yer = db.Column(db.Numeric(15, 2), default=0.00) # ريال يمني
    balance_usd = db.Column(db.Numeric(15, 2), default=0.00) # دولار
    balance_sar = db.Column(db.Numeric(15, 2), default=0.00) # ريال سعودي
    
    # رصيد معلق عام
    balance_pending = db.Column(db.Numeric(15, 2), default=0.00)    
    total_withdrawn = db.Column(db.Numeric(15, 2), default=0.00)    
    
    # 3. حقل اختياري مشفر للبيانات البنكية
    _bank_details_enc = db.Column(db.String(500), nullable=True)
    
    # 4. التحديث التلقائي
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # 5. الربط
    supplier = db.relationship('Supplier', back_populates='wallet')

    # --- خصائص إضافية للوحة التحكم ---
    @property
    def total_balance_yer(self):
        """حساب إجمالي الأرصدة كقيمة مكافئة باليمني (اختياري)"""
        return float(self.balance_yer) + (float(self.balance_usd) * 2000) # مثال تقريبي

    # --- نظام التشفير ---
    @staticmethod
    def _get_key():
        return os.environ.get('ENCRYPTION_KEY', 'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq=').encode()

    @property
    def bank_details(self):
        if not self._bank_details_enc: return None
        try:
            return Fernet(self._get_key()).decrypt(self._bank_details_enc.encode()).decode()
        except:
            return None

    @bank_details.setter
    def bank_details(self, value):
        if value:
            self._bank_details_enc = Fernet(self._get_key()).encrypt(str(value).encode()).decode()

    def __repr__(self):
        return f'<SupplierWallet {self.wallet_code} | YER: {self.balance_yer}>'
