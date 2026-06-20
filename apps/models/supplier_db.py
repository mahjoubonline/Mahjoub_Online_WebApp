# coding: utf-8
# 📂 apps/models/supplier_user_db.py - نظام حوكمة المستخدمين والصلاحيات لـ MAHJOUB ONLINE

from apps.extensions import db
from datetime import datetime

class SupplierUser(db.Model):
    __tablename__ = 'supplier_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 🔗 ربط الموظف أو المالك بالمورد الرئيسي في قاعدة البيانات
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)
    
    # --- بيانات الاعتماد اليومية للموظفين ---
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # --- معلومات الهوية ---
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    
    # 🛡️ نظام الحوكمة وجدار فصل الصلاحيات الصارم
    # الصلاحيات المتاحة: 
    # - 'admin': المالك (له السيادة المطلقة ورؤية الأرصدة المشفرة والتسويات).
    # - 'stock_manager': مأمور المخازن (تعديل الكميات والمخزون فقط).
    # - 'accountant': المحاسب (متابعة حركات التكلفة دون القدرة على سحب كاش).
    role = db.Column(db.String(30), default='admin', nullable=False)
    
    # حالة الحساب (يمكن للمالك تجميد حساب أي موظف فوراً)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # تاريخ انتهاء العقد (التوقيف التلقائي للموظفين المؤقتين عبر السيرفر)
    contract_end_date = db.Column(db.Date, nullable=True)
    
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 الربط العكسي لسهولة الاستدعاء
    supplier = db.relationship('Supplier', backref=db.backref('users', cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<SupplierUser(username='{self.username}', role='{self.role}', active={self.is_active})>"
