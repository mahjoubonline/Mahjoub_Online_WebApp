# coding: utf-8
from apps import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class SupplierStaff(db.Model):
    __tablename__ = 'supplier_staff'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, index=True)
    
    # بيانات الموظف
    username = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # الصلاحيات (Roles) للتحكم في ما يمكن للموظف رؤيته أو فعله
    role = db.Column(db.String(50), default='worker', index=True) # owner, processor, accountant
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # التوثيق
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # دوال الأمان
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Staff {self.username} | Role: {self.role}>'
