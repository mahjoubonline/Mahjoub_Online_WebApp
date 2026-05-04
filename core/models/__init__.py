# core/models/__init__.py

from core import db

# 1. استيراد نماذج الهوية
from core.models.user import User

# 2. استيراد نموذج الموردين (التعميد السيادي)
from .business import Supplier

# 3. محاولة استيراد النماذج الأخرى مع معالجة الأخطاء لضمان تشغيل التطبيق
try:
    from .vendor import Vendor
except ImportError:
    Vendor = None

try:
    from .product import Product
except ImportError:
    Product = None

# حل مشكلة Order التي تظهر في سجلات Railway (image_651b4a.png)
# سنقوم بتعريفه كـ None مؤقتاً إذا لم يكن موجوداً لمنع الانهيار
try:
    from .business import Order
except ImportError:
    try:
        from .vendor import Order
    except ImportError:
        Order = None

try:
    from .vendor import WithdrawRequest
except ImportError:
    WithdrawRequest = None

# 4. قائمة التصدير الشاملة
__all__ = [
    'db',
    'User',
    'Supplier',
    'Order',
    'Vendor',
    'Product',
    'WithdrawRequest'
]
