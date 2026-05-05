from core import db
from datetime import datetime

# --- كلاس الطلبات (حوكمة العمليات التجارية) ---
class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    
    # ربط الطلب بالمستخدم (العميل الذي قام بالشراء)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # تفاصيل العملة والمبالغ (التوافق مع الأرصدة الثلاثة)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='YER') # YER, SAR, USD
    
    # حالة الطلب السيادية
    status = db.Column(db.String(50), default='pending') # pending, processing, shipped, delivered, cancelled
    
    # بيانات الشحن المباشرة
    shipping_address = db.Column(db.Text, nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    
    # التوقيت الرقمي
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # علاقة للوصول لبيانات صاحب الطلب
    customer = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"<Order ID: {self.id} - Status: {self.status}>"

# --- يمكنك إضافة كلاسات أخرى هنا مستقبلاً مثل Transaction أو Payment ---
