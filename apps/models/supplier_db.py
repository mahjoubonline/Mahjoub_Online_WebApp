# coding: utf-8
# 📂 apps/models/supplier_db.py

from apps.extensions import db
from cryptography.fernet import Fernet
import os
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event, update

class Supplier(db.Model, UserMixin):
    __tablename__ = 'suppliers'
    
    # 1. المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    supplier_code = db.Column(db.String(50), unique=True, nullable=True, index=True) 
    trade_name = db.Column(db.String(150), nullable=True, index=True)
    
    # 2. البيانات الحساسة (تشفير AES)
    _phone_enc = db.Column(db.String(255), nullable=False) 
    search_phone = db.Column(db.String(20), index=True) 
    
    # 3. بيانات المصادقة
    password_hash = db.Column(db.String(255), nullable=True)
    
    # 4. الحالات والرتب
    status = db.Column(db.String(20), default='active', index=True)
    rank = db.Column(db.String(20), default='bronze', index=True)
    
    # 5. التدقيق الزمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_login = db.Column(db.DateTime, nullable=True)

    # 6. العلاقات (تم إضافة staff_members لمنع الخطأ)
    supplier_profile = db.relationship('SupplierProfile', back_populates='supplier', uselist=False, cascade="all, delete-orphan")
    wallet = db.relationship('SupplierWallet', back_populates='supplier', uselist=False, cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='supplier', cascade="all, delete-orphan")
    financials = db.relationship('OrderFinancial', back_populates='supplier', cascade="all, delete-orphan")
    
    # العلاقة المفقودة التي كانت تسبب الخطأ
    staff_members = db.relationship('SupplierStaff', back_populates='supplier', cascade="all, delete-orphan")

    # --- نظام التشفير ---
    @staticmethod
    def _get_key():
        return os.environ.get('ENCRYPTION_KEY', 'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq=').encode()

    @property
    def phone(self):
        try:
            return Fernet(self._get_key()).decrypt(self._phone_enc.encode()).decode()
        except:
            return None

    @phone.setter
    def phone(self, value):
        self._phone_enc = Fernet(self._get_key()).encrypt(str(value).encode()).decode()
        self.search_phone = str(value)[:20]

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Supplier {self.username}>'

# --- نموذج الموظفين التابعين للمورد (لإكمال العلاقة) ---
class SupplierStaff(db.Model):
    __tablename__ = 'supplier_staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='staff')
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    
    supplier = db.relationship('Supplier', back_populates='staff_members')

# --- نظام إنشاء المحفظة وتحديث الكود تلقائياً ---
@event.listens_for(Supplier, 'after_insert')
def receive_after_insert(mapper, connection, target):
    from apps.models.wallet_db import SupplierWallet
    
    # 1. تحديث كود المورد
    new_supplier_code = f"MAH-SUP963{target.id}"
    connection.execute(
        update(Supplier).where(Supplier.id == target.id).values(supplier_code=new_supplier_code)
    )
    
    # 2. إنشاء محفظة للمورد
    new_wallet = SupplierWallet(
        wallet_code=f"MAH-WEL963{target.id}",
        supplier_id=target.id,
        balance_yer=0.00, balance_usd=0.00, balance_sar=0.00, balance_pending=0.00
    )
    
    session = db.session.object_session(target)
    if session:
        session.add(new_wallet)
