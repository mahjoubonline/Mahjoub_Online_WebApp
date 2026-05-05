# core/models/__init__.py
from core import db 

# 1. استيراد الهوية الأساسية (نواة النظام)
from .user import User

# 2. استيراد الموردين (الموديل الجديد والسيادي لـ محجوب أونلاين)
# هذا الاستيراد ضروري لضمان ظهور جدول الموردين في Railway
try:
    from .supplier import Supplier
except ImportError:
    Supplier = None

# 3. استيراد المكونات الإضافية (المنتجات والعمليات التجارية)
try:
    from .product import Product
except ImportError:
    Product = None

try:
    # قراءة Order من ملف business.py
    from .business import Order
except ImportError:
    Order = None

# 4. تعريف المكونات المتاحة للنظام (الشرعية الرقمية الموحدة)
# أضفنا Supplier هنا لضمان استدعائه عند كتابة: from core.models import *
__all__ = ['db', 'User', 'Supplier', 'Product', 'Order']
