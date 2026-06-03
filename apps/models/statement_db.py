# coding: utf-8
# 📂 apps/models/statement_db.py - نموذج القيود المحاسبية (مُحصن)

from apps.extensions import db
from apps.utils.security import AESCipher 

class SupplierStatement(db.Model):
    """
    نموذج القيود والعمليات المحاسبية للموردين - محصن ومشفر
    """
    __tablename__ = 'supplier_statements'
    
    id = db.Column(db.Integer, primary_key=True)
    # ربط القيد بالمورد لضمان سلامة البيانات
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    
    # علاقة الربط لضمان سهولة الوصول للبيانات في الداشبورد
    supplier = db.relationship('Supplier', backref=db.backref('statements', lazy='dynamic'))
    
    # حقول التخزين المشفر للقيم الحساسة
    _description = db.Column(db.String(500), nullable=True) 
    _debit = db.Column(db.String(255), nullable=False)
    _credit = db.Column(db.String(255), nullable=False)
    _running_balance = db.Column(db.String(255), nullable=False)
    
    currency = db.Column(db.String(10), default='USD', nullable=False)

    # --- بوابات التشفير وفك التشفير ---

    @property
    def description(self): 
        return AESCipher.decrypt(self._description) if self._description else ""
    @description.setter
    def description(self, value): 
        self._description = AESCipher.encrypt(str(value)) if value else None

    @property
    def debit(self): 
        try:
            return float(AESCipher.decrypt(self._debit))
        except (ValueError, TypeError, Exception):
            return 0.0
    @debit.setter
    def debit(self, value): 
        self._debit = AESCipher.encrypt(str(float(value or 0.0)))

    @property
    def credit(self): 
        try:
            return float(AESCipher.decrypt(self._credit))
        except (ValueError, TypeError, Exception):
            return 0.0
    @credit.setter
    def credit(self, value): 
        self._credit = AESCipher.encrypt(str(float(value or 0.0)))

    @property
    def running_balance(self): 
        try:
            return float(AESCipher.decrypt(self._running_balance))
        except (ValueError, TypeError, Exception):
            return 0.0
    @running_balance.setter
    def running_balance(self, value): 
        self._running_balance = AESCipher.encrypt(str(float(value or 0.0)))

    def __repr__(self):
        return f'<SupplierStatement {self.id} - Supplier ID: {self.supplier_id}>'
