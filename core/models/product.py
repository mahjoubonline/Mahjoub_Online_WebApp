from core import db
from datetime import datetime

class Product(db.Model):
    """
    نموذج المنتج السيادي: يعمل كجسر ربط بين نظام محجوب أونلاين ومنصة قمرة.
    يتم تخزين البيانات المالية والروابط التقنية فقط، بينما تبقى الأصول في السحابة.
    """
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # --- 🔗 جسر الربط التقني مع "قمرة" ---
    q_product_id = db.Column(db.String(100), unique=True, nullable=True) 
    
    # 🚨 تعديل هام: معرف القسم في قمرة (ضروري لعملية النشر آلياً)
    q_collection_id = db.Column(db.String(100), nullable=True) 

    name = db.Column(db.String(200), nullable=False)
    
    # --- 💰 الترسانة المالية (نظام حماية العملات) ---
    # استخدام Numeric بدلاً من Float لضمان دقة الحسابات المالية
    cost_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00) 
    currency = db.Column(db.String(10), default='SAR') 
    sale_price = db.Column(db.Numeric(10, 2), nullable=True) 
    
    # --- 📊 مصفوفة الحالة والحوكمة ---
    status = db.Column(db.String(50), default='pending') 
    is_synced = db.Column(db.Boolean, default=False) 
    
    # --- 🤝 الارتباط السيادي (هوية المورد) ---
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product: {self.name} | QID: {self.q_product_id} | Collection: {self.q_collection_id}>'
