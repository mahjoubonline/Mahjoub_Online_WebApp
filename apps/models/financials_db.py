# coding: utf-8
# 📂 apps/models/financials_db.py

import os
from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db

class OrderFinancial(db.Model):
    __tablename__ = 'order_financials'

    # [صمام الأمان]: فهرسة مسمّاة لضمان سرعة الاستعلامات والربط
    __table_args__ = (
        db.Index('idx_fin_order_id', 'order_id'),
        db.Index('idx_fin_supplier_id', 'supplier_id'),
        db.Index('idx_fin_settlement', 'settlement_status'),
        db.Index('idx_fin_created', 'created_at'),
        {'extend_existing': True}
    )

    # 1. المعرفات والربط
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    
    # 2. المبالغ المالية (مشفرة لضمان الخصوصية المالية)
    _supplier_cost_enc = db.Column(db.String(255), nullable=False)
    _mahjoub_commission_enc = db.Column(db.String(255), nullable=False)
    _total_paid_enc = db.Column(db.String(255), nullable=False)
    shipping_fees = db.Column(db.Numeric(18, 2), default=0.00)
    
    # 3. حالة التسوية
    settlement_status = db.Column(db.String(20), default='pending')
    
    # 4. توثيق زمني
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    settled_at = db.Column(db.DateTime, nullable=True)

    # [المسار الكامل]: الربط السيادي لمنع خطأ Multiple classes found
    order = db.relationship('apps.models.orders_db.Order', back_populates='financials')
    supplier = db.relationship('apps.models.supplier_db.Supplier', back_populates='financials')

    # --- نظام التشفير (AES) ---
    @staticmethod
    def _get_key():
        key = os.environ.get('ENCRYPTION_KEY')
        return key.encode() if key else b'w1Kk9P7zY5mZg4tE8Lp2nJvR6cXsA9qB0xU3jH5oI8Vq='

    def _encrypt(self, value):
        f = Fernet(self._get_key())
        return f.encrypt(str(value).encode()).decode()

    def _decrypt(self, value):
        f = Fernet(self._get_key())
        return float(f.decrypt(value.encode()).decode())

    # --- Properties للمبالغ المشفرة ---
    @property
    def supplier_cost(self): return self._decrypt(self._supplier_cost_enc)
    @supplier_cost.setter
    def supplier_cost(self, value): self._supplier_cost_enc = self._encrypt(value)

    @property
    def mahjoub_commission(self): return self._decrypt(self._mahjoub_commission_enc)
    @mahjoub_commission.setter
    def mahjoub_commission(self, value): self._mahjoub_commission_enc = self._encrypt(value)

    @property
    def total_paid(self): return self._decrypt(self._total_paid_enc)
    @total_paid.setter
    def total_paid(self, value): self._total_paid_enc = self._encrypt(value)

    def calculate_net_profit(self):
        return self.mahjoub_commission

    def __repr__(self):
        return f'<OrderFinancial OrderID: {self.order_id} | Status: {self.settlement_status}>'
