# 1. جدول الموردين السيادي الموحد
class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # --- بيانات الهوية والدخول ---
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    activity_type = db.Column(db.String(100))
    
    # --- 🛡️ نظام الرقابة والاعتماد السيادي ---
    is_approved = db.Column(db.Boolean, default=False) 
    status = db.Column(db.String(20), default='pending') # pending, active, suspended
    
    # --- التفاصيل الجغرافية والاتصال ---
    trade_name = db.Column(db.String(200))
    full_name = db.Column(db.String(200))
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    # --- 💰 الترسانة المالية المتعددة (المحافظ السيادية) ---
    # تم استخدام Numeric لضمان أعلى دقة مالية في الحسابات
    wallet_balance = db.Column(db.Numeric(10, 2), default=0.00) # الرصيد الإجمالي التقديري
    wallet_usd = db.Column(db.Numeric(10, 2), default=0.00)     # محفظة الدولار
    wallet_sar = db.Column(db.Numeric(10, 2), default=0.00)     # محفظة الريال السعودي
    wallet_yer = db.Column(db.Numeric(10, 2), default=0.00)     # محفظة الريال اليمني
    
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    fin_type = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # --- 📦 علاقة الربط بالمخزون ---
    products = db.relationship('Product', backref='supplier_owner', lazy=True, cascade="all, delete-orphan")

    @property
    def sovereign_id(self):
        """توليد الرقم السيادي للمورد"""
        return f"MAH-9046{self.id}"

    @property
    def approval_label(self):
        return "معتمد ✅" if self.is_approved else "بانتظار المراجعة ⏳"
