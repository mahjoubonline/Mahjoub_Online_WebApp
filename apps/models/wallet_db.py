# coding: utf-8
# 📂 apps/models/wallet_db.py

import os
from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db

class SupplierWallet(db.Model):
    """
    موديل محفظة الموردين: يحتوي على الأرصدة المالية والبيانات البنكية المشفرة.
    """
    __tablename__ = 'supplier_wallets'

    # [صمام الأمان]: فهرسة مسمّاة لضمان سرعة الاستعلامات ومنع تكرار التعريف
    __table_args__ = (
        db.Index('idx_wall_code', 'wallet_code'),
        db.Index('idx_wall_supplier_id', 'supplier_id'),
        db.Index('idx_wall_updated', 'updated_at'),
        {'extend_existing': True}
    )
    
    # الأعمدة الأساسية
    id = db.Column(db.Integer, primary_key=True)
    wallet_code = db.Column(db.String(50), unique=True, nullable=False)
    
    # العلاقة مع المورد: ربط فريد (كل مورد له محفظة واحدة فقط)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, unique=True)
    
    # [الدقة المالية]: استخدام Numeric لتجنب أخطاء التقريب في العملات
    balance_yer = db.Column(db.Numeric(18, 2), default=0.00) 
    balance_usd = db.Column(db.Numeric(18, 2), default=0.00) 
    balance_sar = db.Column(db.Numeric(18, 2), default=0.00) 
    balance_pending = db.Column(db.Numeric(18, 2), default=0.00)    
    total_withdrawn = db.Column(db.Numeric(18, 2), default=0.00)    
    
    # [تشفير AES]: تخزين البيانات البنكية الحساسة مشفرة
    _bank_details_enc = db.Column(db.String(500), nullable=True)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # [الربط السيادي]: منع تضارب الكلاسات
    supplier = db.relationship(
        'apps.models.supplier_db.Supplier', 
        back_populates='wallet'
    )

    # --- نظام التشفير (AES) ---
    @staticmethod
    def _get_key():
        """
        جلب مفتاح التشفير من متغيرات البيئة.
        يجب التأكد من ضبط ENCRYPTION_KEY في إعدادات Render.
        """
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # مفتاح افتراضي للتطوير فقط (يجب تغييره في الإنتاج)
            return b'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq='
        return key.encode()

    @property
    def bank_details(self):
        """فك تشفير بيانات البنك عند الاسترجاع من قاعدة البيانات"""
        if not self._bank_details_enc: 
            return None
        try:
            f = Fernet(self._get_key())
            return f.decrypt(self._bank_details_enc.encode()).decode()
        except Exception: 
            return None

    @bank_details.setter
    def bank_details(self, value):
        """تشفير بيانات البنك قبل الحفظ في قاعدة البيانات"""
        if value:
            f = Fernet(self._get_key())
            self._bank_details_enc = f.encrypt(str(value).encode()).decode()
        else:
            self._bank_details_enc = None

    def __repr__(self):
        return f'<SupplierWallet {self.wallet_code} | SAR: {self.balance_sar}>'
