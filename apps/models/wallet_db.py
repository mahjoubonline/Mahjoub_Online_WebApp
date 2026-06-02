# coding: utf-8
import os
from apps.extensions import db
from apps.utils.security import AESCipher

# تهيئة مشفر البيانات مع التحقق من وجود المفتاح السيادي لحماية العمليات المالية
encryption_key = os.getenv('ENCRYPTION_KEY')
if not encryption_key:
    print("⚠️ تحذير أمني جسيم: ENCRYPTION_KEY غير موجود! تم تفعيل المفتاح الاحتياطي للتطوير.")
    encryption_key = '00000000000000000000000000000000' # مفتاح افتراضي مؤقت للتطوير المحلي فقط

cipher = AESCipher(encryption_key)

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.String(50), db.ForeignKey('suppliers.sovereign_id'), nullable=False, unique=True)
    wallet_code = db.Column(db.String(50), nullable=False, unique=True)
    
    # حقول الأرصدة المشفرة للعملات الثلاث (YER, SAR, USD)
    _yer_total = db.Column(db.String(255), default=lambda: cipher.encrypt("0.00"))
    _sar_total = db.Column(db.String(255), default=lambda: cipher.encrypt("0.00"))
    _usd_total = db.Column(db.String(255), default=lambda: cipher.encrypt("0.00"))
    
    status = db.Column(db.String(20), default='نشطة', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

    # العلاقات البرمجية للحركات المالية
    transactions = db.relationship('WalletTransaction', backref='wallet', lazy=True, cascade="all, delete-orphan")

    # --- بوابات العملة الأولى: الريال اليمني (YER) ---
    @property
    def yer_total(self): 
        try: return float(cipher.decrypt(self._yer_total))
        except Exception: return 0.0
    @yer_total.setter
    def yer_total(self, val): self._yer_total = cipher.encrypt(str(val))

    # --- بوابات العملة الثانية: الريال السعودي (SAR) ---
    @property
    def sar_total(self): 
        try: return float(cipher.decrypt(self._sar_total))
        except Exception: return 0.0
    @sar_total.setter
    def sar_total(self, val): self._sar_total = cipher.encrypt(str(val))

    # --- بوابات العملة الثالثة المضافة: الدولار الأمريكي (USD) ---
    @property
    def usd_total(self): 
        try: return float(cipher.decrypt(self._usd_total))
        except Exception: return 0.0
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
    
    # 1. الأعمدة الجديدة المشفرة بالكامل
    _amount = db.Column(db.String(255), nullable=True)
    _profit_margin = db.Column(db.String(255), nullable=True)
    _notes = db.Column(db.String(500), nullable=True) # تم تعديل التشفير للنصوص الطويلة
    
    # 2. الأعمدة القديمة (تم حل مشكلة تداخل الأسماء بربط اسم العمود الفعلي باسم برمجي فريد)
    legacy_amount = db.Column('amount', db.String(255), nullable=True)
    legacy_profit_margin = db.Column('profit_margin', db.String(255), nullable=True)
    legacy_notes = db.Column('notes', db.Text, nullable=True)
    
    status = db.Column(db.String(20), default='ناجحة', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # --- الخصائص الذكية للهجرة السلسة وفك التشفير التلقائي ---
    
    @property
    def amount(self): 
        try:
            if self._amount: return float(cipher.decrypt(self._amount))
            if self.legacy_amount: return float(str(self.legacy_amount))
            return 0.0
        except Exception: return 0.0
    @amount.setter
    def amount(self, val): self._amount = cipher.encrypt(str(val))

    @property
    def profit_margin(self): 
        try: 
            if self._profit_margin: return float(cipher.decrypt(self._profit_margin))
            if self.legacy_profit_margin: return float(str(self.legacy_profit_margin))
            return 0.0
        except Exception: return 0.0
    @profit_margin.setter
    def profit_margin(self, val): self._profit_margin = cipher.encrypt(str(val))

    @property
    def notes(self): 
        try: 
            if self._notes: return cipher.decrypt(self._notes)
            if self.legacy_notes: return str(self.legacy_notes)
            return ""
        except Exception: return ""
    @notes.setter
    def notes(self, val): self._notes = cipher.encrypt(str(val))
