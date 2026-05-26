# 📂 apps/utils/report_generator.py

from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from sqlalchemy import func

class ReportGenerator:
    # ... الدوال السابقة (get_detailed_transactions, etc) ...

    @staticmethod
    def get_all_wallets_summary(currency):
        # جلب جميع الموردين
        suppliers = Supplier.query.all()
        results = []
        
        for s in suppliers:
            # حساب الرصيد الحالي للمورد (آخر رصيد تراكمي)
            last_statement = SupplierStatement.query.filter_by(supplier_id=s.id)\
                .order_by(SupplierStatement.created_at.desc()).first()
            
            balance = last_statement.running_balance if last_statement else 0.0
            
            results.append({
                'trade_name': getattr(s, 'trade_name', '---'),
                'owner_name': getattr(s, 'owner_name', '---'),
                'wallet_code': getattr(s, 'sovereign_id', '---'),
                'balance': float(balance)
            })
        return results
