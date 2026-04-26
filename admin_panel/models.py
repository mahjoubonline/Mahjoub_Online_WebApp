from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# تعريف قاعدة البيانات
db = SQLAlchemy()

# 1. جدول الموردين (السلطة الموردة)
class Supplier(db.Model):
    __tablename__ = 'supplier' # تم تغيير الاسم ليتوافق مع ForeignKey في core
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='active')
    wallet_balance = db.Column(db.Numeric(10, 2), default=0.00) # استخدام Numeric للدقة المالية
    
    # علاقة لجلب منتجات المورد
    products = db.relationship('Product', backref='supplier_owner', lazy=True)

# 2. نموذج المنتج السيادي الموحد
class Product(db.Model):
    __tablename__ = 'product' # توحيد اسم الجدول مع core
    id = db.Column(db.Integer, primary_key=True)
    
    # --- 🔗 جسر الربط مع "قمرة" ---
    qumra_id = db.Column(db.String(100), unique=True, nullable=True) # للمزامنة اليدوية
    q_product_id = db.Column(db.String(100), unique=True, nullable=True) # المعرف الرسمي في قمرة
    q_collection_id = db.Column(db.String(100), nullable=True) # القسم
    handle = db.Column(db.String(200)) # الرابط اللطيف
    
    # --- 📝 البيانات الوصفية ---
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True) 
    image_url = db.Column(db.String(500), nullable=True)
    
    # --- 💰 الترسانة المالية (دقة متناهية) ---
    cost_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00) 
    sale_price = db.Column(db.Numeric(10, 2), nullable=True) 
    currency = db.Column(db.String(10), default='SAR') 
    
    # --- 📊 مصفوفة الحالة والحوكمة ---
    status = db.Column(db.String(50), default='pending') 
    is_synced = db.Column(db.Boolean, default=False) 
    stock = db.Column(db.Integer, default=0)
    
    # --- 🤝 الارتباط السيادي ---
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def status_label(self):
        status_map = {
            'pending': '⏳ بانتظار التعميد',
            'approved': '✅ معتمد جاهز للنشر',
            'published': '🚀 منشور على المتجر'
        }
        return status_map.get(self.status, '❓ غير معروف')
