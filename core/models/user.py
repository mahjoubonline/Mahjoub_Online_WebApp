# core/models/user.py
from datetime import datetime
import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core.extensions import db 

class User(db.Model, UserMixin):
    """ 
    موديل الهوية السيادية: يمثل المستخدمين (المدراء، الموردين، والموظفين).
    هو الركيزة الأساسية لنظام الحماية والحوكمة في محجوب أونلاين.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # تصنيف الرتب (super_admin, admin_staff, supplier_owner, supplier_staff)
    role = db.Column(db.String(50), default='admin') 
    
    # نظام الأذونات المرن: يخزن كـ JSON (مثل: {"edit_products": true, "view_reports": false})
    permissions = db.Column(db.Text, default='{}')
    
    # الربط مع الكيان (يكون NULL لموظفي الإدارة العليا)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # حقول الهوية الشخصية
    full_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    
    # الرقابة الزمنية والأمنية
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    last_ip = db.Column(db.String(45)) # لتتبع موقع الدخول تقنياً
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """تشفير كلمة المرور وتأمينها في الخزينة الرقمية"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من الهوية الرقمية عند تسجيل الدخول"""
        return check_password_hash(self.password_hash, password)

    # --- منطق الحوكمة الذكي (Smart Governance Logic) ---

    def has_permission(self, perm_name):
        """الرادار السيادي: يتحقق هل يملك المستخدم إذن معين؟"""
        if self.role == 'super_admin': 
            return True # المؤسس يملك صلاحيات مطلقة دائماً
        try:
            perms = json.loads(self.permissions) if self.permissions else {}
            return perms.get(perm_name, False)
        except:
            return False

    @property
    def is_admin_team(self):
        """يتحقق إذا كان المستخدم يتبع مركز قيادة الإدارة العليا"""
        return self.role in ['super_admin', 'admin_staff']

    @property
    def is_supplier_team(self):
        """يتحقق إذا كان المستخدم يتبع كيان مورد (صاحب عمل أو موظف)"""
        return self.role in ['supplier_owner', 'supplier_staff']

    def update_session(self, ip_address):
        """تحديث بيانات الجلسة اللحظية عند كل دخول ناجح"""
        self.last_login = datetime.utcnow()
        self.last_ip = ip_address
        db.session.commit()

    def to_dict(self):
        """تحويل البيانات لقاموس جاهز للاستخدام في واجهات الصلاحيات"""
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role,
            "permissions": json.loads(self.permissions) if self.permissions else {},
            "supplier_id": self.supplier_id,
            "is_active": self.is_active,
            "last_login": self.last_login.strftime('%Y-%m-%d %H:%M') if self.last_login else "لم يسجل دخول"
        }

    def __repr__(self):
        return f"<User {self.username} | Role: {self.role} | Supplier: {self.supplier_id}>"
