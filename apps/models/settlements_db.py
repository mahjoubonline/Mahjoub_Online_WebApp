# coding: utf-8
# 📊 نموذج كشوفات الحسابات الموحد (Ledger) - منصة محجوب أونلاين 2026
# هذا النموذج هو "سجل العمليات" الذي تبحث فيه لحظياً لاستخراج شجرة الحسابات والتقارير

from datetime import datetime
from apps.extensions import db

class SupplierStatement(db.Model):
    __tablename__ = 'supplier_statements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 🔗 الربط: nullable=True يسمح بتسجيل حركات "المنصة" العامة بدون مورد محدد
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True, index=True)
    
    # 🕒 التوقيت (فهرس لتسريع البحث اللحظي بين الفترات)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # 📝 البيانات المالية
    description = db.Column(db.String(255), nullable=False) 
    currency = db.Column(db.String(10), nullable=False, index=True) # YER, SAR, USD
    
    debit = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)  # مدين
    credit = db.Column(db.Numeric(15, 2), default=0.00, nullable=False) # دائن
    running_balance = db.Column(db.Numeric(15, 2), nullable=False, default=0.00) 
    
    # 🛡️ نوع الحركة (محوري لشجرة الحسابات)
    # أمثلة: (SALE, PURCHASE, SETTLEMENT, PROFIT_TRANS, SYSTEM_FEE)
    reference_type = db.Column(db.String(50), nullable=False, index=True) 
    reference_id = db.Column(db.Integer, nullable=True)     

    def __repr__(self):
        return f"<Statement {self.id} | {self.reference_type} | {self.currency}>"

    # --- دوال المساعدة للتقارير (تستخدم في الـ Route) ---
    
    @classmethod
    def get_platform_tree(cls, currency='ALL', start_date=None, end_date=None):
        """تجميع الحركات حسب نوعها لشجرة حسابات المنصة"""
        query = db.session.query(
            cls.reference_type,
            db.func.sum(cls.debit).label('total_debit'),
            db.func.sum(cls.credit).label('total_credit')
        )
        
        if currency != 'ALL':
            query = query.filter_by(currency=currency)
        if start_date:
            query = query.filter(cls.created_at >= start_date)
        if end_date:
            query = query.filter(cls.created_at <= end_date)
            
        return query.group_by(cls.reference_type).all()
