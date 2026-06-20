# coding: utf-8
# 📂 apps/models/wallet_db.py - نظام المحافظ والحركات السيادي (مُشفر بالكامل بـ AES-256)

from apps.extensions import db
from apps.utils.security import AESCipher
from datetime import datetime

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    # 🔗 الربط المتبادل مع جدول الموردين (Supplier)
    supplier = db.relationship('Supplier', back_populates='wallet')
    
    # --- الأرصدة المتاحة المشفّرة (Available Balance) ---
    _balance_sar = db.Column(db.String(255), default=AESCipher.encrypt("0.0"))
    _balance_yer = db.Column(db.String(255), default=AESCipher.encrypt("0.0"))
    _balance_usd = db.Column(db.String(255), default=AESCipher.encrypt("0.0"))
    
    # --- الأرصدة المجمدة المشفّرة لحين التوصيل (Frozen Balance) ---
    _frozen_sar = db.Column(db.String(255), default=AESCipher.encrypt("0.0"))
    _frozen_yer = db.Column(db.String(255), default=AESCipher.encrypt("0.0"))
    _frozen_usd = db.Column(db.String(255), default=AESCipher.encrypt("0.0"))
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    transactions = db.relationship('WalletTransaction', back_populates='wallet', lazy='dynamic', cascade="all, delete-orphan")

    # ==========================================
    # 💎 بوابات التحكم بالأرصدة المتاحة (Properties)
    # ==========================================
    @property
    def balance_sar(self): 
        val = AESCipher.decrypt(self._balance_sar)
        return float(val) if val else 0.0
    @balance_sar.setter
    def balance_sar(self, value): self._balance_sar = AESCipher.encrypt(str(value))

    @property
    def balance_yer(self): 
        val = AESCipher.decrypt(self._balance_yer)
        return float(val) if val else 0.0
    @balance_yer.setter
    def balance_yer(self, value): self._balance_yer = AESCipher.encrypt(str(value))

    @property
    def balance_usd(self): 
        val = AESCipher.decrypt(self._balance_usd)
        return float(val) if val else 0.0
    @balance_usd.setter
    def balance_usd(self, value): self._balance_usd = AESCipher.encrypt(str(value))

    # ==========================================
    # ❄️ بوابات التحكم بالأرصدة المجمدة (Properties)
    # ==========================================
    @property
    def frozen_sar(self): 
        val = AESCipher.decrypt(self._frozen_sar)
        return float(val) if val else 0.0
    @frozen_sar.setter
    def frozen_sar(self, value): self._frozen_sar = AESCipher.encrypt(str(value))

    @property
    def frozen_yer(self): 
        val = AESCipher.decrypt(self._frozen_yer)
        return float(val) if val else 0.0
    @frozen_yer.setter
    def frozen_yer(self, value): self._frozen_yer = AESCipher.encrypt(str(value))

    @property
    def frozen_usd(self): 
        val = AESCipher.decrypt(self._frozen_usd)
        return float(val) if val else 0.0
    @frozen_usd.setter
    def frozen_usd(self, value): self._frozen_usd = AESCipher.encrypt(str(value))

    # ==========================================
    # ⚙️ المحرك المالي لإدارة وتوزيع الطاقة النقدية
    # ==========================================
    def add_transaction(self, amount, currency, transaction_type, order_id=None, description=None):
        """
        إضافة حركة مالية مشفرة وتوجيه الحسابات بناءً على دورة حياة الطلب:
        - 'credit_frozen': حجز رصيد المورد معلقاً بمجرد وصول الطلب من قمرة.
        - 'release_to_available': فك التجميد ونقل المال للمتاح عند نجاح التوصيل.
        - 'debit_withdrawal': خصم المال من الرصيد المتاح عند إتمام التسوية كاش.
        """
        curr = currency.upper()
        
        # 1. إنشاء سجل الحركة وحفر المبلغ مشفراً عبر الـ setter
        transaction = WalletTransaction(
            wallet_id=self.id,
            currency=curr,
            transaction_type=transaction_type,
            order_id=order_id,
            description=description
        )
        transaction.amount = amount  # التشفير التلقائي
        
        # 2. حوكمة وتوجيه الأرصدة بناءً على نوع الحركة والعملة
        if transaction_type == 'credit_frozen':
            if curr == 'SAR': self.frozen_sar += amount
            elif curr == 'YER': self.frozen_yer += amount
            elif curr == 'USD': self.frozen_usd += amount
            
        elif transaction_type == 'release_to_available':
            if curr == 'SAR':
                self.frozen_sar -= amount
                self.balance_sar += amount
            elif curr == 'YER':
                self.frozen_yer -= amount
                self.balance_yer += amount
            elif curr == 'USD':
                self.frozen_usd -= amount
                self.balance_usd += amount
                
        elif transaction_type == 'debit_withdrawal':
            if curr == 'SAR': self.balance_sar -= amount
            elif curr == 'YER': self.balance_yer -= amount
            elif curr == 'USD': self.balance_usd -= amount
            
        db.session.add(transaction)
        # تم إزالة db.session.commit() لتترك حرة تحت سياق الـ controller لضمان تكامل العمليات (Atomicity)
        return transaction


class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id', ondelete='CASCADE'), nullable=False)
    wallet = db.relationship('SupplierWallet', back_populates='transactions')
    
    # 🔗 الربط المالي الفريد مع قمرة أو سوق محجوب
    order_id = db.Column(db.String(100), nullable=True)
    
    # الحقل المالي المحمي بجدار التشفير
    _amount = db.Column(db.String(255), nullable=False)
    
    currency = db.Column(db.String(3), nullable=False)
    transaction_type = db.Column(db.String(30), nullable=False) # credit_frozen, release_to_available, debit_withdrawal
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='completed') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def amount(self): 
        val = AESCipher.decrypt(self._amount)
        return float(val) if val else 0.0
    
    @amount.setter
    def amount(self, value): 
        self._amount = AESCipher.encrypt(str(value))
