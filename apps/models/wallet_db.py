# coding: utf-8
import os
from apps.extensions import db
from apps.utils.security import AESCipher

# تهيئة المشفر
cipher = AESCipher(os.getenv('ENCRYPTION_KEY', 'your-32-byte-key-here-must-be-secure'))

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.String(50), db.ForeignKey('suppliers.sovereign_id'), nullable=False, unique=True)
    wallet_code = db.Column(db.String(50), nullable=False, unique=True)
    
    # حقول مشفرة
    _yer_total = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    _sar_total = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    _usd_total = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    
    status = db.Column(db.String(20), default='نشطة', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

    transactions = db.relationship('WalletTransaction', backref='wallet', lazy=True, cascade="all, delete-orphan")

    # --- خصائص التشفير ---
    @property
    def yer_total(self): return float(cipher.decrypt(self._yer_total))
    @yer_total.setter
    def yer_total(self, val): self._yer_total = cipher.encrypt(str(val))

    @property
    def sar_total(self): return float(cipher.decrypt(self._sar_total))
    @sar_total.setter
    def sar_total(self, val): self._sar_total = cipher.encrypt(str(val))

    @property
    def usd_total(self): return float(cipher.decrypt(self._usd_total))
    @usd_total.setter
    def usd_total(self, val): self._usd_total = cipher.encrypt(str(val))

class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    tx_code = db.Column(db.String(60), unique=True, nullable=False)
    tx_type = db.Column(db.String(30), nullable=False) 
    currency = db.Column(db.String(10), nullable=False)
    
    # حقول مشفرة
    _amount = db.Column(db.String(255), nullable=False)
    _profit_margin = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    _notes = db.Column(db.Text, nullable=True)
    
    status = db.Column(db.String(20), default='ناجحة', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # --- خصائص التشفير للمعاملات ---
    @property
    def amount(self): return float(cipher.decrypt(self._amount))
    @amount.setter
    def amount(self, val): self._amount = cipher.encrypt(str(val))

    @property
    def profit_margin(self): return float(cipher.decrypt(self._profit_margin))
    @profit_margin.setter
    def profit_margin(self, val): self._profit_margin = cipher.encrypt(str(val))

    @property
    def notes(self): return cipher.decrypt(self._notes) if self._notes else ""
    @notes.setter
    def notes(self, val): self._notes = cipher.encrypt(str(val))
