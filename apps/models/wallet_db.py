# coding: utf-8
# 📂 apps/models/wallet_db.py

# ... (الكود السابق لـ SupplierWallet يظل كما هو)

class WalletTransaction(db.Model):
    """سجل الحركات المالية (دفتر الأستاذ) لكل محفظة."""
    __tablename__ = 'wallet_transactions'
    
    __table_args__ = (
        db.Index('idx_trans_wallet', 'wallet_id'),
        db.Index('idx_trans_date', 'created_at'),
        db.Index('idx_trans_source', 'source_type'),
        db.Index('idx_trans_voucher', 'voucher_number'), # [التشقير] لضمان سرعة البحث عن السند
        {'extend_existing': True}
    )

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    # تفاصيل الحركة
    trans_type = db.Column(db.String(20), nullable=False) # 'credit', 'debit'
    source_type = db.Column(db.String(20), default='manual')
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(5), nullable=False)
    
    # تفاصيل السند الموحد
    description = db.Column(db.String(255))
    reference_number = db.Column(db.String(50)) # المرجع الأصلي (مثل رقم الطلب)
    voucher_number = db.Column(db.String(20), unique=True, nullable=True) # [رقم السند الموحد الجديد]
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    wallet = db.relationship('SupplierWallet', back_populates='transactions')

# --- محرك الترقيم التلقائي ---
from sqlalchemy import event, func

@event.listens_for(WalletTransaction, 'before_insert')
def set_voucher_number(mapper, connection, target):
    if not target.voucher_number:
        # 1. جلب أعلى رقم موجود حالياً
        last_trans = db.session.query(func.max(WalletTransaction.voucher_number)).scalar()
        
        if last_trans:
            # استخراج الرقم من التنسيق: MJ-2026-0012328 -> 12328
            try:
                last_num = int(last_trans.split('-')[-1])
            except:
                last_num = 12327 # احتياط
            new_num = last_num + 1
        else:
            # الرقم الابتدائي للمنصة
            new_num = 12328
            
        # 2. تركيب الرقم الجديد: MJ-2026-0012329
        target.voucher_number = f"MJ-2026-{new_num:07d}"
