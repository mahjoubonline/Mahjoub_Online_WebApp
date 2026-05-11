# core/services/stats_service.py
from core.models.user import User
from core.models.supplier import Supplier
from core import db
from sqlalchemy import func
import logging

# إعداد السجلات لمراقبة أداء المحرك المالي
logger = logging.getLogger(__name__)

def get_admin_dashboard_stats():
    """
    محرك الإحصائيات السيادي:
    يقوم بحساب وتحليل البيانات المالية وأعداد المستخدمين والموردين 
    لتقديمها إلى غرفة القيادة (Dashboard).
    """
    try:
        # 1. حساب إجمالي الأرصدة في المحافظ السيادية للموردين (دعم العملات الثلاث)
        total_yer = db.session.query(func.sum(Supplier.balance_yer)).scalar() or 0.0
        total_sar = db.session.query(func.sum(Supplier.balance_sar)).scalar() or 0.0
        total_usd = db.session.query(func.sum(Supplier.balance_usd)).scalar() or 0.0

        # 2. إحصائيات التعداد العام
        users_count = User.query.count() or 0
        suppliers_count = Supplier.query.count() or 0

        # 3. إحصائيات الموردين حسب الحالة والرتبة
        active_suppliers = Supplier.query.filter_by(status='active').count()
        sovereign_suppliers = Supplier.query.filter_by(tier='سيادي').count()

        return {
            'users_count': users_count,
            'suppliers_count': suppliers_count,
            'active_suppliers': active_suppliers,
            'sovereign_suppliers': sovereign_suppliers,
            'total_yer': total_yer,
            'total_sar': total_sar,
            'total_usd': total_usd,
            'orders_count': 0  # يتم ربطها لاحقاً بمحرك الطلبات
        }

    except Exception as e:
        # بروتوكول الحماية: في حال فشل الاستعلام، يتم إرجاع قيم صفرية لضمان عدم انهيار اللوحة
        logger.error(f"⚠️ فشل في استخراج الإحصائيات المالية: {str(e)}")
        return {
            'users_count': 0,
            'suppliers_count': 0,
            'total_yer': 0.0,
            'total_sar': 0.0,
            'total_usd': 0.0,
            'error': str(e)
        }
