# 📂 apps/utils/report_generator.py
from apps.models.statement_db import SupplierStatement
from sqlalchemy import and_

class ReportGenerator:
    
    @staticmethod
    def get_detailed_transactions(supplier_id, currency, start_date, end_date):
        # بناء الفلاتر ديناميكياً
        filters = []
        if supplier_id != 'ALL':
            filters.append(SupplierStatement.supplier_id == supplier_id)
        if currency != 'ALL':
            filters.append(SupplierStatement.currency == currency)
        if start_date:
            filters.append(SupplierStatement.created_at >= start_date)
        if end_date:
            filters.append(SupplierStatement.created_at <= end_date)
            
        return SupplierStatement.query.filter(and_(*filters)).order_by(SupplierStatement.created_at.asc()).all()

    @staticmethod
    def calculate_net_profit(currency, start_date, end_date):
        # منطق حساب الأرباح (يمكنك تخصيصه لاحقاً)
        return 0.0
