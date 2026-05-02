from core import db

# 1. استيراد النماذج من ملفاتها الفرعية
from core.models.user import User
from .vendor import Vendor

# ملاحظة هامة: إذا كان كلاس WithdrawRequest موجوداً داخل ملف vendor.py، 
# يجب استيراده هنا أيضاً ليصبح مرئياً للنظام بالكامل.
try:
    from .vendor import WithdrawRequest
except ImportError:
    # في حال لم يتم تعريفه بعد في ملف vendor
    WithdrawRequest = None

# 2. تعريف الحزم المصدرة (قائمة واحدة شاملة)
# وضع كافة النماذج في قائمة __all__ واحدة يضمن أن النظام يراها جميعاً
__all__ = [
    'User', 
    'Vendor', 
    'WithdrawRequest'
]

# 3. قسم التوسعات المستقبلية (إلغاء التعليق عند الجاهزية)
# from .supplier import Supplier
# from .order import Order
# from .product import Product
