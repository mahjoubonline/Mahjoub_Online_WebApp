# 📂 apps/models/__init__.py
# الفهرس الموحد لجميع موديلات قاعدة البيانات

# 1. الموديلات الأساسية (التي لا تعتمد على غيرها)
from .supplier_db import Supplier
from .admin_db import AdminUser
from .admin_staff_db import AdminStaff
from .marketers_db import Marketer
from .otp_db import OTPVerification
from .supplier_profile_db import SupplierProfile
from .supplier_staff_db import SupplierStaff
from .sync_log import SyncLog
from .wallet_db import VendorWallet 

# 2. الموديلات المعتمدة (التي تعتمد على الموديلات أعلاه)
from .orders_db import Order
from .financials_db import OrderFinancial 

# القائمة الموحدة للتصدير
__all__ = [
    'Supplier',
    'AdminUser', 
    'AdminStaff', 
    'Marketer', 
    'OTPVerification', 
    'SupplierProfile', 
    'SupplierStaff', 
    'SyncLog', 
    'VendorWallet',
    'Order',
    'OrderFinancial'
]
