# coding: utf-8
# 🔑 مستند النموذج المالي والمحافظ الحوكمية - منصة محجوب أونلاين 2026

from apps import db
from datetime import datetime
from sqlalchemy import event

class Wallet(db.Model):
    __tablename__ = 'wallets'
    
    # 1. المعرفات الأساسية والربط الجيني
    id = db.Column(db.Integer, primary_key=True)
    
    # ربط المحفظة بالمورد (العلاقة الصارمة: لكل مورد محفظة واحدة فقط)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), unique=True, nullable=False)
    
    # كود المحفظة المالي الموحد المشتق سيادياً (مثل: WEL-MAH9631)
    wallet_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # 2. خزائن الأرصدة المتعددة (Multi-Currency Vaults)
    yer_balance = db.Column(db.Numeric(16, 2), nullable=False, default=0.00)
    yer_reserved = db.Column(db.Numeric(16, 2), nullable=False, default=0.00)
    
    sar_balance = db.Column(db.Numeric(16, 2), nullable=False, default=0.00)
    sar_reserved = db.Column(db.Numeric(16, 2), nullable=False, default=0.00)
    
    usd_balance = db.Column(db.Numeric(16, 2), nullable=False, default=0.00)
    usd_reserved = db.Column(db.Numeric(16, 2), nullable=False, default=0.00)
    
    # 3. حقول تتبع التحديث والتوثيق الزمني
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 4. الربط الخلفي مع المورد لسهولة الاستدعاء المباشر في الـ API
    supplier = db.relationship('Supplier', backref=db.backref('wallet', uselist=False, cascade='all, delete-orphan'))

    @property
    def yer_available(self):
        return max(0.00, float(self.yer_balance - self.yer_reserved))

    @property
    def sar_available(self):
        return max(0.00, float(self.sar_balance - self.sar_reserved))

    @property
    def usd_available(self):
        return max(0.00, float(self.usd_balance - self.usd_reserved))

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "wallet_code": self.wallet_code,
            "trade_name": self.supplier.trade_name if self.supplier else "منشأة غير معرفة",
            "sovereign_id": self.supplier.sovereign_id if self.supplier else None,
            "rank_grade": self.supplier.rank_grade if self.supplier else "ريادي",
            "state_title": self.supplier.state_title if self.supplier else "تحت التدقيق",
            "shop_phone": self.supplier.shop_phone if self.supplier else None,
            
            "yer_total": float(self.yer_balance),
            "yer_available": self.yer_available,
            "yer_pending": float(self.yer_reserved),
            
            "sar_total": float(self.sar_balance),
            "sar_available": self.sar_available,
            "sar_pending": float(self.sar_reserved),
            
            "usd_total": float(self.usd_balance),
            "usd_available": self.usd_available,
            "usd_pending": float(self.usd_reserved)
        }


# =========================================================================
# 📊 [إصلاح العطل الحرج]: إضافة كلاس سجل الحركات المالية المطلوبة بالسيرفر
# =========================================================================
class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id', ondelete='CASCADE'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'deposit', 'withdrawal', 'hold', 'release'
    currency = db.Column(db.String(10), nullable=False)          # 'YER', 'SAR', 'USD'
    amount = db.Column(db.Numeric(16, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # ربط الحركة بالمحفظة الرئيسية
    wallet = db.relationship('Wallet', backref=db.backref('transactions', cascade='all, delete-orphan'))


# -------------------------------------------------------------------------
# 🛡️ مصيدة الحوكمة التلقائية (Event Listener): فتح المحفظة تلقائياً للمورد الجديد
# -------------------------------------------------------------------------
from apps.models.supplier_db import Supplier

def auto_create_supplier_wallet(mapper, connection, target):
    """
    مراقب حوكمي صارم يعمل فوراً أثناء عملية ولادة حساب المورد (after_insert).
    يستخرج الرقم التسلسلي الموحد لتركيب كود المحفظة وحقنها تلقائياً بالرصيد الصفري المستقر.
    """
    if target.sovereign_id and 'MAH963' in target.sovereign_id:
        serial_num = target.sovereign_id.split('MAH963')[-1]
    else:
        serial_num = str(target.id)
        
    generated_wallet_code = f"WEL-MAH963{serial_num}"

    wallet_table = Wallet.__table__
    connection.execute(
        wallet_table.insert().values(
            supplier_id=target.id,
            wallet_code=generated_wallet_code,
            yer_balance=0.00,
            yer_reserved=0.00,
            sar_balance=0.00,
            sar_reserved=0.00,
            usd_balance=0.00,
            usd_reserved=0.00,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    )

event.listen(Supplier, 'after_insert', auto_create_supplier_wallet)
