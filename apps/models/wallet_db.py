# coding: utf-8
# 📂 apps/models/wallet_db.py - نظام المحافظ (مُشفر بالكامل بـ AES-256)

from apps.extensions import db
from apps.utils.security import AESCipher
from datetime import datetime

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, unique=True)
    supplier = db.relationship('Supplier', back_populates='wallet')
    
    # حقول مشفرة (تخزن كـ String في قاعدة البيانات)
    _balance_sar = db.Column(db.String(255), default=lambda: AESCipher.encrypt("0.0"))
    _balance_yer = db.Column(db.String(255), default=lambda: AESCipher.encrypt("0.0"))
    _balance_usd = db.Column(db.String(255), default=lambda: AESCipher.encrypt("0.0"))
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def balance_sar(self): 
        val = AESCipher.decrypt(self._balance_sar)
        return float(val) if val else 0.0
    
    @balance_sar.setter
    def balance_sar(self, value): 
        self._balance_sar = AESCipher.encrypt(str(value))

    @property
    def balance_yer(self): 
        val = AESCipher.decrypt(self._balance_yer)
        return float(val) if val else 0.0
    
    @balance_yer.setter
    def balance_yer(self, value): 
        self._balance_yer = AESCipher.encrypt(str(value))

    @property
    def balance_usd(self): 
        val = AESCipher.decrypt(self._balance_usd)
        return float(val) if val else 0.0
    
    @balance_usd.setter
    def balance_usd(self, value): 
        self._balance_usd = AESCipher.encrypt(str(value))

    transactions = db.relationship('WalletTransaction', back_populates='wallet', lazy='dynamic')

    def add_transaction(self, amount, currency, transaction_type, order_id=None, description=None):
        """
        إضافة حركة مالية وربطها بـ order_id القادم من قمرة لضمان التتبع المالي
        """
        transaction = WalletTransaction(
            wallet_id=self.id,
            amount=amount, 
            currency=currency.upper(),
            transaction_type=transaction_type,
            order_id=order_id, # ربط الحركة المالية بالطلب
            description=description
        )
        
        multiplier = 1 if transaction_type == 'credit' else -1
        
        # تحديث الأرصدة
        if currency.upper() == 'SAR': self.balance_sar += (amount * multiplier)
        elif currency.upper() == 'YER': self.balance_yer += (amount * multiplier)
        elif currency.upper() == 'USD': self.balance_usd += (amount * multiplier)
            
        db.session.add(transaction)
        db.session.commit()
        return transaction

class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    wallet = db.relationship('SupplierWallet', back_populates='transactions')
    
    # 🔗 الربط المالي: إضافة order_id لربط الحركة المالية بالطلب في قمرة
    order_id = db.Column(db.String(100), nullable=True)
    
    _amount = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='completed') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def amount(self): 
        val = AESCipher.decrypt(self._amount)
        return float(val) if val else 0.0
    
    @amount.setter
    def amount(self, value): 
        self._amount = AESCipher.encrypt(str(value))
