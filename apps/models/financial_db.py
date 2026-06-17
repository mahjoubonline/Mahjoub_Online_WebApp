# coding: utf-8
# 📂 apps/models/financial_db.py - مرجع الأسعار والرقابة المالية (المحدث)

from apps.extensions import db
from datetime import datetime

class ExchangeRate(db.Model):
    __tablename__ = 'exchange_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(3), unique=True, nullable=False)
    rate_to_sar = db.Column(db.Numeric(18, 6), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_rate(cls, currency_code):
        currency_code = currency_code.upper()
        if currency_code == 'SAR':
            return 1.0
        # إضافة تحكم في الخطأ لضمان استمرارية النظام
        record = cls.query.filter_by(currency_code=currency_code).first()
        if not record:
            # افتراضياً، نعتبر العملة 1:1 إذا لم تُعرف لضمان عدم توقف العمليات
            return 1.0
        return float(record.rate_to_sar)

class FinancialLog(db.Model):
    __tablename__ = 'financial_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(50), nullable=False)
    sar_value = db.Column(db.Numeric(18, 2), nullable=False)
    # إضافة ربط اختياري مع الطلبات لسهولة التدقيق (Audit)
    order_id = db.Column(db.String(100), nullable=True) 
    details = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
