# coding: utf-8
# 🔑 مستند النموذج الحوكمي المشفر للموردين - منصة محجوب أونلاين 2026

import os
from apps.extensions import db
from datetime import datetime
from apps.utils.security import AESCipher

# تهيئة مشفر البيانات
cipher = AESCipher(os.getenv('ENCRYPTION_KEY', 'your-32-byte-key-here-must-be-secure'))

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True, nullable=False, index=True) 
    wallet_code = db.Column(db.String(50), unique=True, nullable=False)
    
    # حقول مشفرة (ربط الاسم البرمجي بالاسم الحقيقي في القاعدة بدون شرطة سفلية)
    owner_name_enc = db.Column('owner_name', db.String(255), nullable=False)
    owner_phone_enc = db.Column('owner_phone', db.String(255), nullable=False)
    trade_name_enc = db.Column('trade_name', db.String(255), nullable=False)
    shop_phone_enc = db.Column('shop_phone', db.String(255), nullable=False)
    bank_acc_enc = db.Column('bank_acc', db.String(255), nullable=False)
    
    # حقول التصنيف والتعلم الذكي
    category = db.Column(db.String(50), default='عام') 
    behavior_score = db.Column(db.Float, default=100.0)
    total_transactions = db.Column(db.Integer, default=0)
    
    # حقول إدارية
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    identity_type = db.Column(db.String(50), nullable=False)   
    identity_number = db.Column(db.String(50), unique=True, nullable=False)  
    identity_image = db.Column(db.String(255))   
    activity_type = db.Column(db.String(50))     
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    address_detail = db.Column(db.Text) 
    fin_type = db.Column(db.String(20))         
    bank_name = db.Column(db.String(100))        
    status = db.Column(db.String(20), nullable=False, default='pending') 
    rank_grade = db.Column(db.String(20), nullable=False, default='ريادي') 
    registration_source = db.Column(db.String(30), nullable=False, default='الموقع الخارجي') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- خصائص التشفير الذكي (Properties) ---

    @property
    def owner_name(self): return cipher.decrypt(self.owner_name_enc)
    @owner_name.setter
    def owner_name(self, value): self.owner_name_enc = cipher.encrypt(value)

    @property
    def owner_phone(self): return cipher.decrypt(self.owner_phone_enc)
    @owner_phone.setter
    def owner_phone(self, value): self.owner_phone_enc = cipher.encrypt(value)

    @property
    def trade_name(self): return cipher.decrypt(self.trade_name_enc)
    @trade_name.setter
    def trade_name(self, value): self.trade_name_enc = cipher.encrypt(value)

    @property
    def shop_phone(self): return cipher.decrypt(self.shop_phone_enc)
    @shop_phone.setter
    def shop_phone(self, value): self.shop_phone_enc = cipher.encrypt(value)

    @property
    def bank_acc(self): return cipher.decrypt(self.bank_acc_enc)
    @bank_acc.setter
    def bank_acc(self, value): self.bank_acc_enc = cipher.encrypt(value)

    # --- باقي الدوال ---
    
    def learn_from_interaction(self, is_positive):
        self.behavior_score += (0.5 if is_positive else -2.0)
        self.total_transactions += 1
        if self.behavior_score > 150: self.category = 'مورد استراتيجي'
        elif self.behavior_score < 50: self.category = 'مورد تحت المراقبة'
        db.session.commit()

    @property
    def balance(self):
        from apps.models.statement_db import SupplierStatement
        last = SupplierStatement.query.filter_by(supplier_id=self.id).order_by(SupplierStatement.created_at.desc()).first()
        return last.running_balance if last else 0.0

    @staticmethod
    def generate_next_sovereign_id():
        last = Supplier.query.order_by(Supplier.id.desc()).first()
        num = int(last.sovereign_id.split('MAH963')[-1]) + 1 if last else 1
        return f"SUP-MAH963{num}"
