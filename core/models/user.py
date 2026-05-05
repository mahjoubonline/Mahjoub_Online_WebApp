from core import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import InternalError, ProgrammingError

# --- كلاس المستخدم (نواة الهوية والرقابة الإدارية) ---
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # الأدوار: admin (أنت)، staff (فريقك)، vendor (الموردين لاحقاً)
    role = db.Column(db.String(50), default='admin') 
    is_active_account = db.Column(db.Boolean, default=True)

    # ملاحظة سيادية: تم فصل علاقة Vendor و WithdrawRequest مؤقتاً 
    # لكي تعمل لوحة الإدارة دون البحث عن ملفات محذوفة.
    # سيتم ربطها برمجياً عند تفعيل لوحة المورد.

    def set_password(self, password):
        """تشفير كلمة المرور لتعزيز الأمن الرقمي لـ محجوب أونلاين"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق السيادي من الهوية عند دخول الترسانة الإدارية"""
        if not self.password_hash: return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        """ضمان استمرارية الوصول حتى عند حدوث تذبذب في القاعدة"""
        try:
            return self.is_active_account
        except (InternalError, ProgrammingError, Exception):
            db.session.rollback()
            return True 

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username} - Role: {self.role}>"
