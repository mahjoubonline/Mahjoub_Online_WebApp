from core import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import InternalError, ProgrammingError

class User(db.Model, UserMixin):
    # تحديد اسم الجدول ليتطابق مع النظام السيادي لـ "محجوب أونلاين"
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    # الحقل المعتمد للتشفير
    password_hash = db.Column(db.String(256), nullable=False)
    
    # الأعمدة الهيكلية لضمان صلاحيات الإدارة والموردين
    role = db.Column(db.String(50), default='admin') 
    is_active_account = db.Column(db.Boolean, default=True)

    # --- الربط السيادي مع نموذج المورد (Supplier) ---
    # تم ضبط uselist=False لأن كل مستخدم مورد يمتلك بروفايل مورد واحد فقط
    # العلاقة 'Supplier' تضمن تكامل البيانات عند الإضافة أو الحذف
    supplier = db.relationship('Supplier', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        """تشفير كلمة المرور السيادية قبل الحفظ في الترسانة"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من صحة كلمة المرور عبر الهاش المشفر"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        """صمام أمان: التحقق من نشاط الحساب مع حماية الجلسة من الانهيار"""
        try:
            return self.is_active_account
        except (InternalError, ProgrammingError, Exception):
            # تطهير الجلسة فوراً في حال وجود خطأ في الهيكل
            db.session.rollback()
            return True 

    def __repr__(self):
        """التمثيل النصي للمستخدم داخل سجلات المراقبة"""
        try:
            return f"<User {self.username} - Role: {self.role}>"
        except:
            db.session.rollback()
            return f"<User {self.username}>"

    def get_id(self):
        """معرف Flask-Login الأساسي لاستمرارية الجلسة"""
        return str(self.id)
