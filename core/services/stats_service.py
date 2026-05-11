# core/services/stats_service.py
from core.models.user import User
from core.models.supplier import Supplier
from core import db
from sqlalchemy import func

def get_admin_dashboard_stats():
    """
    محرك الإحصائيات: يقوم بحساب الأرقام والبيانات المالية الحية للوحة التحكم.
    """
    try:
        # حساب إجمالي أرصدة الموردين لكل عملة
        total_yer = db.session.query(func.sum(Supplier.balance_yer)).scalar() or 0.0
        total_sar = db.session.query(func.sum(Supplier.balance_sar)).scalar() or 0.0
        total_usd = db.session.query(func.sum(Supplier.balance_usd)).scalar() or 0.0

        return {
            'users_count': User.query.count() or 0,
            'suppliers_count': Supplier.query.count() or 0,
            'orders_count': 0,  # يمكن ربطها بموديل الطلبات لاحقاً
            'total_yer': total_yer,
            'total_sar': total_sar,
            'total_usd': total_usd
        }
    except Exception as e:
        # في حال حدوث خطأ، نعود بقيم صفرية لضمان عدم انهيار الواجهة
        print(f"⚠️ خطأ في محرك الإحصائيات: {e}")
        return {
            'users_count': 0,
            'suppliers_count': 0,
            'orders_count': 0,
            'total_yer': 0.0,
            'total_sar': 0.0,
            'total_usd': 0.0,
            'error': str(e)
        }
