# coding: utf-8
# 📂 apps/models/wallet_db.py

import os
from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db
from sqlalchemy import event, func

class SupplierWallet(db.Model):
    """محفظة الموردين: الأرصدة والبيانات المشفرة."""
    __tablename__ = 'supplier_wallets'

    __table_args__ = (
        db.Index('idx_wall_code', 'wallet_code'),
        db.Index('idx_wall_supplier_id', 'supplier_id'),
        db.Index('idx_wall_updated', 'updated_at'),
        {'extend_existing': True}
    )
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_code = db.Column(db.String(50), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, unique=True)
    
    balance_yer = db.Column(db.Numeric(18, 2), default=0.00) 
    balance_usd = db.Column(db.Numeric(18, 2), default=0.00) 
    balance_sar = db.Column(db.Numeric(18, 2), default=0.00) 
    balance_pending = db.Column(db.Numeric(18, 2), default=0.00)    
    total_withdrawn = db.Column(db.Numeric(18, 2), default=0.00)    
    
    _bank_details_enc = db.Column(db.String(500), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    supplier = db.relationship('apps.models.supplier_db.Supplier', back_populates='wallet')
    transactions = db.relationship('WalletTransaction', back_populates='wallet', cascade="all, delete-orphan")

    @staticmethod
    def _get_key():
        key = os.environ.get('ENCRYPTION_KEY')
        return key.encode() if key else b'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq='

    @property
    def bank_details(self):
        if not self._bank_details_enc: return None
        try:
            f = Fernet(self._get_key())
            return f.decrypt(self._bank_details_enc.encode()).decode()
        except: return None

    @bank_details.setter
    def bank_details(self, value):
        if value:
            f = Fernet(self._get_key())
            self._bank_details_enc = f.encrypt(str(value).encode()).decode()
        else: self._bank_details_enc = None

class WalletTransaction(db.Model):
    """سجل الحركات المالية الموحد (دفتر الأستاذ) لكل المنصة."""
    __tablename__ = 'wallet_transactions'
    
    __table_args__ = (
        db.Index('idx_trans_wallet', 'wallet_id'),
        db.Index('idx_trans_date', 'created_at'),
        db.Index('idx_trans_type', 'trans_type'),
        db.Index('idx_trans_owner', 'owner_type', 'owner_id'),
        db.Index('idx_trans_voucher', 'voucher_number'),
        {'extend_existing': True}
    )

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    owner_type = db.Column(db.String(20), default='supplier') 
    owner_id = db.Column(db.Integer, nullable=False)
    
    trans_type = db.Column(db.String(20), nullable=False) 
    source_type = db.Column(db.String(20), default='manual')
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(5), nullable=False)
    
    balance_before = db.Column(db.Numeric(18, 2), nullable=False)
    balance_after = db.Column(db.Numeric(18, 2), nullable=False)
    
    description = db.Column(db.String(255))
    reference_number = db.Column(db.String(50)) 
    related_order_id = db.Column(db.String(50), nullable=True)
    voucher_number = db.Column(db.String(20), unique=True, nullable=True) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=True)

    wallet = db.relationship('SupplierWallet', back_populates='transactions')

    @classmethod
    def execute_transfer(cls, wallet_id, amount, trans_type, currency='SAR', owner_type='supplier', owner_id=0, description=''):
        """المحرك المالي الرشيق: سطر كود واحد لتنفيذ أي عملية مالية."""
        new_trans = cls(
            wallet_id=wallet_id,
            amount=amount,
            trans_type=trans_type,
            currency=currency,
            owner_type=owner_type,
            owner_id=owner_id,
            description=description
        )
        db.session.add(new_trans)
        db.session.commit()
        return new_trans

@event.listens_for(WalletTransaction, 'before_insert')
def set_voucher_number(mapper, connection, target):
    # توليد رقم القسيمة
    if not target.voucher_number:
        last_trans = db.session.query(func.max(WalletTransaction.voucher_number)).scalar()
        if last_trans and '-' in last_trans:
            try: last_num = int(last_trans.split('-')[-1])
            except: last_num = 12327
        else: last_num = 12327
        target.voucher_number = f"MJ-2026-{last_num + 1:07d}"

    # تحديث الأرصدة بناءً على العملة
    if target.balance_before is None or target.balance_after is None:
        wallet = SupplierWallet.query.get(target.wallet_id)
        if wallet:
            # تحديد الرصيد الحالي بناءً على العملة
            if target.currency == 'YER':
                current = wallet.balance_yer or 0.00
            elif target.currency == 'USD':
                current = wallet.balance_usd or 0.00
            else: # SAR افتراضياً
                current = wallet.balance_sar or 0.00
            
            target.balance_before = current
            
            # حساب الحركة (إيداع أو سحب)
            if target.trans_type in ['credit', 'adjustment_credit', 'sale_revenue']:
                target.balance_after = current + target.amount
            else:
                target.balance_after = current - target.amount
            
            # حفظ الرصيد الجديد في العمود الصحيح
            if target.currency == 'YER':
                wallet.balance_yer = target.balance_after
            elif target.currency == 'USD':
                wallet.balance_usd = target.balance_after
            else:
                wallet.balance_sar = target.balance_after
