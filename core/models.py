from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# تعريف كائن قاعدة البيانات
db = SQLAlchemy()

class User(db.Model):
    """جدول المستخدمين: يدعم المدير العام، المورد، والموظف"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False) # هنا نكتب الاسم بالعربي
    password = db.Column(db.String(255), nullable=False) # كلمة المرور مشفرة
    
    # الصلاحيات: 'admin' (أنت), 'supplier' (المورد), 'employee' (موظف المورد)
    role = db.Column(db.String(20), nullable=False, default='employee')
    
    # ربط المستخدم بمورد معين (إذا كان موظفاً أو صاحب شركة توريد)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)

class Supplier(db.Model):
    """جدول الموردين (شركاء النجاح)"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False) # اسم شركة المورد
    currency = db.Column(db.String(10), default='YER') # العملة: يمني، دولار، إلخ
    
    # المحفظة المالية (الرصيد المستحق للمورد)
    balance = db.Column(db.Float, default=0.0)
    
    # علاقة عكسية لجلب جميع موظفي هذا المورد
    staff = db.relationship('User', backref='employer', lazy=True)
    # علاقة لجلب جميع الطلبات المحولة لهذا المورد
    assigned_orders = db.relationship('Order', backref='assigned_supplier', lazy=True)

class Order(db.Model):
    """جدول الطلبات القادمة من قمرة (التعامل برقم الطلب فقط)"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False) # رقم الطلب من قمرة
    
    amount_sar = db.Column(db.Float, nullable=False) # المبلغ الأصلي بالريال السعودي
    amount_local = db.Column(db.Float) # المبلغ بعد تحويله لعملة المورد
    
    # ربط الطلب بالمورد الذي اخترته أنت (تحويل المسار)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # حالة الطلب: (قيد المراجعة، جاري التنفيذ، مكتمل)
    status = db.Column(db.String(30), default='قيد المراجعة')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemLog(db.Model):
    """جدول سجل العمليات (لسرية وتحركات النظام)"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255)) # وصف العملية (مثلاً: تحويل طلب رقم X للمورد Y)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
