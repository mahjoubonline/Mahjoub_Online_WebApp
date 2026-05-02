from core import db
from datetime import datetime

class Supplier(db.Model):
    """
    موديل الموردين: يمثل شركاء الترسانة في مختلف المدن اليمنية
    """
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # اسم المورد أو الشركة
    city = db.Column(db.String(50), nullable=False)  # المدينة (عدن، الخوخة، إلخ)
    phone = db.Column(db.String(20), nullable=True)
    
    # ربط المورد بحساب القائد الذي يدير المنصة
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # علاقة لجلب كافة طلبات هذا المورد بسهولة
    orders = db.relationship('Order', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.name} - {self.city}>"

class Order(db.Model):
    """
    موديل الطلبات: لتتبع حركة السلع والسيولة المركزية
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)  # قيمة العملية
    status = db.Column(db.String(50), default='قيد التدقيق')   # حالة الطلب
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ربط الطلب بالمورد المسؤول عنه
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
