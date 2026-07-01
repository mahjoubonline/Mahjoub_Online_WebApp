# coding: utf-8
# 📂 apps/orders/services.py

from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from sqlalchemy import func

class OrderService:
    @staticmethod
    def get_paginated_orders(page, per_page, search_query=None, status=None):
        """جلب الطلبات مع الربط والفلترة."""
        query = db.session.query(Order, OrderFinancial).outerjoin(OrderFinancial)
        
        if search_query:
            query = query.filter(
                Order.order_id_display.ilike(f'%{search_query}%') | 
                Order.customer_name.ilike(f'%{search_query}%')
            )
        
        if status:
            query = query.filter(Order.status == status)
            
        return query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_dashboard_stats():
        """حساب إحصائيات لوحة التحكم بدقة عالية."""
        return {
            'cancelled': Order.query.filter_by(status='cancelled').count(),
            'completed': Order.query.filter_by(status='completed').count(),
            'total_sales': db.session.query(func.sum(OrderFinancial.total_paid)).scalar() or 0
        }

    @staticmethod
    def get_order_details(order_id):
        """جلب تفاصيل طلب محدد مع بياناته المالية."""
        return db.session.query(Order, OrderFinancial)\
            .outerjoin(OrderFinancial, Order.id == OrderFinancial.order_id)\
            .filter(Order.id == order_id).first_or_404()
