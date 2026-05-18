# coding: utf-8
# 🔑 مستند النموذج المالي والمحافظ الحوكمة الموحدة - منصة محجوب أونلاين 2026

from apps import db
from datetime import datetime
from sqlalchemy import event

class Wallet(db.Model):
    # التطابق التام والمقصود مع الجدول المعتمد في السيرفر لقطع دابر أي تعارض
    __tablename__ = 'supplier_wallets'
    
    # 1. المعرفات الأساسية والربط الجيني
    id = db.Column(db.Integer, primary_key=True)
    
    # ربط المحفظة بالمورد (العلاقة الصارمة: لكل مورد محفظة واحدة فقط)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), unique=True, nullable=False)
    
    # كود المحفظة المالي الموحد المشتق سيادياً (مثل: WEL-MAH9631)
    wallet_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # 2. خزائن الأرصدة المتعددة المتطابقة مع حقول الـ Database الفعلية
    yer_balance = db.Column('yer_total', db.Numeric(16, 2), nullable=False, default=0.00)
    yer_reserved = db.Column('yer_available', db.Numeric(16, 2), nullable=False, default=0.00) # تم استغلال الحقل المتاح للتوافق الهيكلي
    yer_withdrawn = db.Column('yer_withdrawn', db.Numeric(16, 2), nullable=False, default=0.00)
    yer_pending = db.Column('yer_pending', db.Numeric(16, 2), nullable=False, default=0.00)
    
    sar_balance = db.Column('sar_total', db.Numeric(16, 2), nullable=False, default=0.00)
    sar_reserved = db.Column('sar_available', db.Numeric(16, 2), nullable=False, default=0.00)
    sar_withdrawn = db.Column('sar_withdrawn', db.Numeric(16, 2), nullable=False, default=0.00)
    sar_pending = db.Column('sar_pending', db.Numeric(16, 2), nullable=False, default=0.00)
    
    usd_balance = db.Column('usd_total', db.Numeric(16, 2), nullable=False, default=0.00)
    usd_reserved = db.Column('usd_available', db.Numeric(16, 2), nullable=False, default=0.00)
    usd_withdrawn = db.Column('usd_withdrawn', db.Numeric(16, 2), nullable=False, default=0.00)
    usd_pending = db.Column('usd_pending', db.Numeric(16, 2), nullable=False, default=0.00)
    
    # 3. حقول تتبع التحديث والتوثيق الزمني
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 4. الربط الخلفي مع المورد لسهولة الاستدعاء المباشر في الـ API
    supplier = db.relationship('Supplier', backref=db.backref('wallet', uselist=False, cascade='all, delete-orphan'))

    @property
    def yer_available(self):
        return max(0.00, float(self.yer_balance - self.yer_pending))

    @property
    def sar_available(self):
        return max(0.00, float(self.sar_balance - self.sar_pending))

    @property
    def usd_available(self):
        return max(0.00, float(self.usd_balance - self.usd_pending))

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
            "yer_pending": float(self.yer_pending),
            
            "sar_total": float(self.sar_balance),
            "sar_available": self.sar_available,
            "sar_pending": float(self.sar_pending),
            
            "usd_total": float(self.usd_balance),
            "usd_available": self.usd_available,
            "usd_pending": float(self.usd_pending)
        }

# 🛡️ الحصانة الهيكلية
SupplierWallet = Wallet

# =========================================================================
# 📊 كلاس سجل الحركات المالية الموحد
# =========================================================================
class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions_log'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id', ondelete='CASCADE'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'deposit', 'withdrawal', 'hold', 'release'
    currency = db.Column(db.String(10), nullable=False)          # 'YER', 'SAR', 'USD'
    amount = db.Column(db.Numeric(16, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    wallet = db.relationship('Wallet', backref=db.backref('transactions', cascade='all, delete-orphan'))


# -------------------------------------------------------------------------
# 🛡️ مصيدة الحوكمة المحدثة والنهائية باستخدام الـ ORM Session Add
# -------------------------------------------------------------------------
from apps.models.supplier_db import Supplier

def auto_create_supplier_wallet(mapper, connection, target):
    """
    مراقب حوكمي صارم ينشئ محفظة مالية للمورد الجديد بالاعتماد الحصري على كائن الـ ORM.
    هذا الأسلوب يتكفل بمطابقة الأسماء البرمجية مع جداول السيرفر تلقائياً دون تضارب.
    """
    if target.sovereign_id and 'MAH963' in target.sovereign_id:
        serial_num = target.sovereign_id.split('MAH963')[-1]
    else:
        serial_num = str(target.id)
        
    generated_wallet_code = f"WEL-MAH963{serial_num}"

    # 🛡️ استخدام أسلوب الكائن النقي لإدراج المحفظة مباشرة بشكل متوافق برمجياً
    new_wallet = Wallet(
        supplier_id=target.id,
        wallet_code=generated_wallet_code,
        yer_balance=0.00,
        yer_reserved=0.00,
        yer_withdrawn=0.00,
        yer_pending=0.00,
        sar_balance=0.00,
        sar_reserved=0.00,
        sar_withdrawn=0.00,
        sar_pending=0.00,
        usd_balance=0.00,
        usd_reserved=0.00,
        usd_withdrawn=0.00,
        usd_pending=0.00
    )
    
    # ربط الكائن بالجلسة الحية الحالية لإدراجه متزامناً مع المورد
    db.session.add(new_wallet)

event.listen(Supplier, 'after_insert', auto_create_supplier_wallet)
