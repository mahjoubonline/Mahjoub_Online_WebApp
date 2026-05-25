# coding: utf-8
# 📊 نموذج كشوفات الحسابات الموحد - نظام محجوب أونلاين 2026
# تم إضافة الربط المباشر بـ Supplier لتمكين البحث السريع

from datetime import datetime
from apps.extensions import db

class SupplierStatement(db.Model):
    """ 
    جدول كشف الحساب التاريخي للمورد (Ledger) 
    يقوم بأرشفة العمليات المالية لضمان الشفافية والمراجعة
    """
    __tablename__ = 'supplier_statements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 🔗 الربط المباشر بالمورد
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    
    # 💳 الربط بالمحفظة (اختياري، يمكن استخدامه إذا لزم الأمر)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=True)
    
    # 🕒 تفاصيل التوقيت والوصف
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String(255), nullable=False) 
    currency = db.Column(db.String(10), nullable=False)    
    
    # 🧮 القيم المالية
    debit = db.Column(db.Numeric(15, 2), default=0.00)  
    credit = db.Column(db.Numeric(15, 2), default=0.00) 
    
    # الرصيد التراكمي
    running_balance = db.Column(db.Numeric(15, 2), nullable=False) 
    
    # 🛡️ حقل إضافي لأرباح الإدارة (مهم لبطاقات الأداء)
    admin_fee = db.Column(db.Numeric(15, 2), default=0.00) 
    
    # 🔗 الربط المرجعي
    reference_type = db.Column(db.String(50)) 
    reference_id = db.Column(db.Integer)      

    def __repr__(self):
        return f"<SupplierStatement {self.id} | Balance: {self.running_balance} {self.currency}>"
