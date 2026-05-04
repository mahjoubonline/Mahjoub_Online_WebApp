# core/models/__init__.py

from core import db

# 1. استيراد النماذج الأساسية (الهوية والسيادة)
from .user import User
from .vendor import Vendor, WithdrawRequest

# 2. استيراد النماذج المرتبطة بالأعمال والمنتجات
try:
    from .product import Product
except ImportError:
    Product = None

# 3. معالجة نموذج الطلبات (Order)
# تم نقل الاعتماد هنا إلى vendor أو business حسب هيكلية ملفاتك
try:
    from .business import Order
except ImportError:
    try:
        from .vendor import Order
    except ImportError:
        Order = None

# 4. قائمة التصدير الشاملة (تنظيف من أي مسمى Supplier قديم)
__all__ = [
    'db',
    'User',
    'Vendor',
    'Order',
    'Product',
    'WithdrawRequest'
]
