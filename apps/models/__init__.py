# coding: utf-8
# 📂 apps/models/__init__.py

"""
مركز التحكم في الموديلات (Model Registry)
تم تنظيم الاستيراد لضمان تحميل الموديلات بشكل متسلسل ومنع حدوث الاعتمادات الدائرية.
"""

from apps.extensions import db

# 1. الموديلات الأساسية (التي تمثل الجداول المستقلة ولا تعتمد على غيرها)
from .supplier_db import Supplier
from .admin_db import AdminUser
from .marketer_db import Marketer
from .exchange_db import ExchangeRate

# 2. الموديلات التابعة (التي تعتمد على الـ Foreign Keys للموديلات الأساسية)
from .admin_staff_db import AdminStaff
from .supplier_profile_db import SupplierProfile
from .supplier_staff_db import SupplierStaff
from .wallet_db import SupplierWallet, WalletTransaction
from .financials_db import OrderFinancial
from .orders_db import Order
from .order_items_db import OrderItem
from .sync_log import SyncLog

# 3. القائمة المصدرة (Export Registry)
# جميع الكلاسات المسجلة هنا ستكون متاحة عند استدعاء `from apps.models import ...`
__all__ = [
    'db',
    'AdminStaff',
    'AdminUser',
    'ExchangeRate',
    'Marketer',
    'Order',
    'OrderItem',
    'OrderFinancial',
    'Supplier',
    'SupplierProfile',
    'SupplierStaff',
    'SupplierWallet',
    'SyncLog',
    'WalletTransaction'
]
