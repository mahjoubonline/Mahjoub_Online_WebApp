# coding: utf-8
# 📂 apps/utils/report_generator.py
from sqlalchemy import func, cast, String
from apps.extensions import db
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import WalletTransaction
from apps.models.supplier_db import Supplier

class ReportGenerator:
    """
    محرك مركزي آمن ومطور لاستخراج التقارير المالية الشاملة - منصة محجوب أونلاين
    """

    @staticmethod
    def get_all_wallets_summary():
        """ 
        استخراج ملخص أرصدة كافة الحسابات (المتجر، المالك، كود المحفظة، الرصيد)
        تستخدم لعرض الكيان المالي الشامل للمنصة وتحديد من له ومن عليه
        """
        suppliers = Supplier.query.all()
        summary = []
        for s in suppliers:
            # افتراض أن الموديل يحتوي على حقل balance أو يتم حسابه
            # إذا كان الحقل في الموديل مختلفاً، تأكد من مطابقة الاسم
            summary.append({
                'trade_name': getattr(s, 'trade_name', '---'),
                'owner_name': getattr(s, 'owner_name', '---'),
                'wallet_code': getattr(s, 'sovereign_id', '---'), # نستخدم sovereign_id ككود للمحفظة
                'balance': float(getattr(s, 'balance', 0))
            })
        # ترتيب حسب الرصيد (من الأكثر رصيداً إلى الأقل)
        return sorted(summary, key=lambda x: x['balance'], reverse=True)

    @staticmethod
    def get_platform_financial_tree(currency='ALL', start_date=None, end_date=None):
        """ استخراج شجرة حسابات المنصة ومجاميع الحركات حسب العملة """
        query = db.session.query(
            SupplierStatement.currency, 
            func.sum(SupplierStatement.debit).label('total_debit'),
            func.sum(SupplierStatement.credit).label('total_credit')
        )

        if currency and currency != 'ALL':
            query = query.filter(SupplierStatement.currency == currency)
        if start_date:
            query = query.filter(SupplierStatement.created_at >= start_date)
        if end_date:
            query = query.filter(SupplierStatement.created_at <= end_date)
            
        results = query.group_by(SupplierStatement.currency).all()
        
        return [
            {
                'type': r.currency,
                'debit': float(r.total_debit or 0),
                'credit': float(r.total_credit or 0),
                'balance': float((r.total_credit or 0) - (r.total_debit or 0))
            } for r in results
        ]

    @staticmethod
    def get_detailed_transactions(supplier_id=None, currency='ALL', start_date=None, end_date=None):
        """ استخراج الحركات التفصيلية لمورد معين أو لجميع الحسابات """
        query = db.session.query(
            SupplierStatement.id,
            SupplierStatement.supplier_id,
            SupplierStatement.created_at,
            SupplierStatement.description,
            SupplierStatement.currency,
            SupplierStatement.debit,
            SupplierStatement.credit,
            SupplierStatement.running_balance,
            Supplier.trade_name.label('supplier_trade_name'),
            Supplier.owner_name.label('supplier_owner_name')
        ).join(
            Supplier, 
            cast(SupplierStatement.supplier_id, String) == cast(Supplier.id, String)
        )
        
        if supplier_id and str(supplier_id).strip() != '' and str(supplier_id) != 'ALL':
            query = query.filter(cast(SupplierStatement.supplier_id, String) == cast(supplier_id, String))
            
        if currency and currency != 'ALL':
            query = query.filter(SupplierStatement.currency == currency)
        if start_date:
            query = query.filter(SupplierStatement.created_at >= start_date)
        if end_date:
            query = query.filter(SupplierStatement.created_at <= end_date)
            
        results = query.order_by(SupplierStatement.created_at.desc()).all()

        statements = []
        for r in results:
            s = SupplierStatement()
            s.id = r.id
            s.supplier_id = r.supplier_id
            s.created_at = r.created_at
            s.description = r.description
            s.currency = r.currency
            s.debit = r.debit
            s.credit = r.credit
            s.running_balance = r.running_balance
            s.supplier_name = r.supplier_trade_name or r.supplier_owner_name or "مورد غير معروف"
            statements.append(s)

        return statements

    @staticmethod
    def calculate_net_profit(currency, start_date=None, end_date=None):
        """ حساب صافي أرباح المنصة من المحفظة المالية """
        query = WalletTransaction.query
        
        if currency and currency != 'ALL':
            query = query.filter(WalletTransaction.currency == currency)
        if start_date:
            query = query.filter(WalletTransaction.created_at >= start_date)
        if end_date:
            query = query.filter(WalletTransaction.created_at <= end_date)
            
        total_profit = query.with_entities(func.sum(WalletTransaction.profit_margin)).scalar()
        return float(total_profit or 0)
