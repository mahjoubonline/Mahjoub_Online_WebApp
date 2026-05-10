from core.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import InternalError, ProgrammingError

class User(db.Model, UserMixin):
    """
    نواة الهوية الرقمية - v4.0
    تتحكم في صلاحيات الوصول لمركز قيادة محجوب أونلاين
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True) # مضاف للتواصل الرسمي
    password_hash = db.Column(db.String(256), nullable=False)
    
    # الأدوار السيادية: [admin, staff, supplier, customer]
    role = db.Column(db.String(50), default='customer') 
    is_active_account = db.Column(db.Boolean, default=True)

    # --- الربط البرمجي (علاقات الترسانة) ---
    # ربط المستخدم ببروفايل المورد (في حال كان حسابه مورد)
    # ملاحظة: تم استخدام backref هادئ لتجنب التعارض
    supplier_profile = db.relationship('Supplier', backref='account', uselist=False, lazy=True)

    def set_password(self, password):
        """تشفير سيادي عالي الطاقة"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من الهوية قبل فتح بوابات النظام"""
        if not self.password_hash: return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        """ضمان الحصانة البرمجية عند استعلام الحالة"""
        try:
            return self.is_active_account
        except Exception:
            db.session.rollback()
            return True 

    def to_dict(self):
        """تحويل البيانات لـ JSON لمحرك الجافا سكريبت"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "is_active": self.is_active_account
        }

    def __repr__(self):
        return f"<User {self.username} | Role: {self.role}>"
