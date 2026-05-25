# coding: utf-8
# 📊 نموذج كشوفات الحسابات الموحد - نظام محجوب أونلاين 2026
# تم تحسين النموذج لضمان الاستقرار المالي والربط المرجعي

from datetime import datetime
from apps.extensions import db

class SupplierStatement(db.Model):
    """ 
    جدول كشف الحساب التاريخي للمورد (Ledger) 
    يقوم بأرشفة العمليات المالية لضمان الشفافية والمراجعة
    """
    __tablename__ = 'supplier_statements'
    
    # ⚠️ هام جداً: إضافة هذا السطر يمنع خطأ "Table already defined" عند تحديث التطبيق
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 🔗 الربط المباشر بالمورد
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, index=True)
    
    # 💳 الربط بالمحفظة (nullable=True يسمح بمرونة في الحركات العامة)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=True, index=True)
    
    # 🕒 تفاصيل التوقيت والوصف
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False) 
    currency = db.Column(db.String(10), nullable=False, index=True)    
    
    # 🧮 القيم المالية (استخدام Numeric لضمان دقة العمليات الحسابية)
    debit = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)  
    credit = db.Column(db.Numeric(15, 2), default=0.00, nullable=False) 
    
    # الرصيد التراكمي
    running_balance = db.Column(db.Numeric(15, 2), nullable=False, default=0.00) 
    
    # 🛡️ حقل إضافي لأرباح الإدارة
    admin_fee = db.Column(db.Numeric(15, 2), default=0.00) 
    
    # 🔗 الربط المرجعي (استخدام index لتسريع الاستعلامات)
    reference_type = db.Column(db.String(50), nullable=True, index=True) 
    reference_id = db.Column(db.Integer, nullable=True)      

    def __init__(self, **kwargs):
        super(SupplierStatement, self).__init__(**kwargs)
        # التأكد من قيم افتراضية آمنة
        self.debit = self.debit or 0.00
        self.credit = self.credit or 0.00
        self.running_balance = self.running_balance or 0.00

    def __repr__(self):
        return f"<SupplierStatement {self.id} | Supplier: {self.supplier_id} | Balance: {self.running_balance} {self.currency}>"
