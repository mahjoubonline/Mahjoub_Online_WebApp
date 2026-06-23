# coding: utf-8
# 📂 apps/models/__init__.py
# الفهرس الموحد لجميع موديلات قاعدة البيانات (مرتب بدقة لمنع فشل الـ Mapper)

# 1. الموديلات المستقلة تماماً (المكونات الأساسية)
from .admin_db import AdminUser
from .admin_staff import AdminStaff
from .marketer import Marketer
from .otp_db import OTPVerification
from .sync_log_db import SyncLog

# 2. الموديلات التي تعتمد على الموديلات الأساسية
from .supplier_profile_db import SupplierProfile 
from .supplier_staff import SupplierStaff
from .vendor_wallet import VendorWallet 

# 3. الموديلات الرئيسية (التي تحتوي على الـ relationships)
from .supplier_db import Supplier
from .order import Order
from .order_financials import OrderFinancial 

# القائمة الموحدة للتصدير
__all__ = [
    'Supplier', 'AdminUser', 'AdminStaff', 'Marketer', 
    'OTPVerification', 'SupplierProfile', 'SupplierStaff', 
    'SyncLog', 'VendorWallet', 'Order', 'OrderFinancial'
]
