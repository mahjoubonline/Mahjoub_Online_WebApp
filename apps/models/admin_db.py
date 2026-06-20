# coding: utf-8
# 📂 apps/models/admin_db.py - نظام الهوية الموحد للمنصة (إدارة وموردين)

import os
from apps.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from flask import current_app
from datetime import datetime

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # --- حقول الهوية والمطابقة لجميع الحسابات ---
    username = db.Column(db.String(100), unique=True, nullable=False)        # اسم المستخدم المعتمد
    admin_email = db.Column(db.String(150), unique=True, nullable=False)     # البريد الإلكتروني المدخل بالخطوة الأولى
    password_hash = db.Column(db.String(255), nullable=False)
    _phone_number_enc = db.Column(db.String(255), nullable=True)              # الهاتف الإداري المشفر بـ Fernet
    
    # --- فرز رتب السيادة والحوكمة ---
    role = db.Column(db.String(50), default='supplier') # (super_admin, admin, supplier, marketer)
    
    # --- فهارس البحث السريع وعابر الأنظمة ---
    admin_code = db.Column(db.String(100), unique=True, nullable=True)       # الكود السيادي المتولد آلياً
    search_name = db.Column(db.String(150), index=True, nullable=True)
    search_phone = db.Column(db.String(20), index=True, nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 الربط الموحد: التوجيه الصحيح إلى الكلاس الفعلي المسؤول عن البيانات التجارية 'SupplierProfile'
    # استخدام back_populates يضمن التزامن الكامل والتوافق المطلق مع جدول التوصيف المتقدم لحساب المورد
    supplier_profile = db.relationship('SupplierProfile', back_populates='user', uselist=False, lazy='joined')

    # --- نظام توليد الأكواد الآلي الموحد ---
    def generate_sovereign_code(self):
        """توليد الأكواد بناءً على الرتبة المحددة للحساب"""
        if self.id and not self.admin_code:
            if self.
