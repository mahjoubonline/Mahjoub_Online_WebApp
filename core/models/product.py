from core import db
from datetime import datetime

class Product(db.Model):
    """
    موديل المنتج - نظام محجوب أونلاين
    يربط بين سعر التكلفة للمورد وسعر البيع في قمرة مع تتبع الرقم التسلسلي.
    """
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    # --- بيانات المنتج الأساسية ---
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    
    # --- الربط السيادي مع قمرة ---
    qumra_id = db.Column(db.String(100), unique=True) # المعرف الفريد في منصة قمرة
    sku = db.Column(db.String(100), unique=True)      # وحدة حفظ المخزون
    
    # --- الحوكمة المالية ---
    cost_price = db.Column(db.Float, nullable=False)  # سعر التكلفة (حق المورد)
    sale_price = db.Column(db.Float)                 # سعر البيع النهائي للزبون
    commission = db.Column(db.Float, default=0.0)    # صافي ربح المنصة من هذا المنتج
    
    # --- حالة المخزون ---
    stock_quantity = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_profit(self):
        """حساب الربح الصافي للمنصة من هذا المنتج"""
        if self.sale_price and self.cost_price:
            return self.sale_price - self.cost_price
        return 0.0

    def __repr__(self):
        return f'<Product: {self.name} | Supplier ID: {self.supplier_id}>'
