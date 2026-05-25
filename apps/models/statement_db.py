
# coding: utf-8
from datetime import datetime
from apps.extensions import db

class SupplierStatement(db.Model):
    """ جدول كشف الحساب التاريخي للمورد (أرشفة مالية) """
    __tablename__ = 'supplier_statements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    # تفاصيل الحركة
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String(255), nullable=False) # وصف العملية
    currency = db.Column(db.String(10), nullable=False) # YER, SAR, USD
    
    # القيم المالية (مدين / دائن)
    debit = db.Column(db.Numeric(15, 2), default=0.00)  # خصم
    credit = db.Column(db.Numeric(15, 2), default=0.00) # إضافة
    running_balance = db.Column(db.Numeric(15, 2), nullable=False) # الرصيد بعد العملية
    
    # ربط مرجعي (للوصول للعملية الأصلية في حال الرغبة في التفاصيل)
    reference_type = db.Column(db.String(50)) # 'TRANSACTION' أو 'SETTLEMENT'
    reference_id = db.Column(db.Integer)      # معرف السجل في الجدول الأصلي

    def __repr__(self):
        return f"<Statement {self.id} | Wallet {self.wallet_id} | Bal: {self.running_balance}>"
