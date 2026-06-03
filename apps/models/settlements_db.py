# coding: utf-8
# 📂 apps/models/settlements_db.py - سجل التسويات المالية للموردين (مُحصن)

import hashlib
from apps.extensions import db
from apps.utils.security import AESCipher 

class AdminSettlement(db.Model):
    """ نموذج تسجيل عمليات التسوية المالية للموردين """
    __tablename__ = 'admin_settlements'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, index=True)
    
    # علاقة الربط لضمان سهولة الاستعلام عن تسويات المورد
    supplier = db.relationship('Supplier', backref=db.backref('settlements', lazy='dynamic'))
    
    # حقول التخزين المشفرة
    _amount = db.Column('amount_enc', db.String(255), nullable=False)
    _reference_number = db.Column('reference_number_enc', db.String(255), nullable=True)
    _notes = db.Column('notes_enc', db.Text, nullable=True)
    
    # الفهرس الأعمى للبحث (Blind Index)
    reference_hash = db.Column('reference_hash', db.String(64), unique=True, nullable=True, index=True)
    
    currency = db.Column(db.String(10), default='USD', nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='مكتملة', nullable=False, index=True)
    settlement_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, index=True)

    # --- بوابات التشفير (تستخدم AESCipher مباشرة) ---

    @property
    def amount(self):
        try:
            return float(AESCipher.decrypt(self._amount)) if self._amount else 0.0
        except Exception:
            return 0.0

    @amount.setter
    def amount(self, value):
        self._amount = AESCipher.encrypt(str(float(value or 0.0)))

    @property
    def reference_number(self):
        try:
            return AESCipher.decrypt(self._reference_number) if self._reference_number else ""
        except Exception:
            return ""

    @reference_number.setter
    def reference_number(self, value):
        if value:
            clean_ref = str(value).strip()
            self._reference_number = AESCipher.encrypt(clean_ref)
            self.reference_hash = hashlib.sha256(clean_ref.encode('utf-8')).hexdigest()
        else:
            self._reference_number = None
            self.reference_hash = None

    @property
    def notes(self):
        try:
            return AESCipher.decrypt(self._notes) if self._notes else ""
        except Exception:
            return ""

    @notes.setter
    def notes(self, value):
        self._notes = AESCipher.encrypt(str(value)) if value else None

    def __repr__(self):
        return f"<AdminSettlement {self.id} | Supplier: {self.supplier_id} | Status: {self.status}>"
