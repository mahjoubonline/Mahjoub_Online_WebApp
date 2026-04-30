from core import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    # ربط المورد بحسابه في جدول المستخدمين (علاقة رأس برأس)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # بيانات المتجر التجارية
    store_name = db.Column(db.String(150), nullable=False)
    contact_phone = db.Column(db.String(20))
    location = db.Column(db.String(200)) # مثل: عدن، الخوخة، المخا
    
    # حالة الاعتماد من قبل الإدارة
    is_verified = db.Column(db.Boolean, default=False)
    
    # الربط مع المنتجات (كل مورد يمكنه امتلاك عدة منتجات)
    products = db.relationship('Product', backref='owner_supplier', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Supplier {self.store_name}>'
