# core/models/__init__.py

# 1. استيراد قاعدة البيانات (التوحيد السيادي لضمان الاتصال)
from core import db 

# 2. استيراد الكيانات الأساسية (النواة الرقمية للترسانة)
# تم التأكد من تضمين كلاس User و Supplier لإنهاء أخطاء الـ Import
from .user import User
from .supplier import Supplier, SupplierStaff

# ملاحظة: الملفات أدناه تم تعطيلها مؤقتاً لضمان إقلاع السيرفر
# بمجرد إنشاء ملفات الـ Product والـ Business، قم بإزالة علامة (#)
# from .product import Product
# from .business import Order, OrderItem

# 3. بروتوكول التصدير الموحد (__all__)
# هذا القسم يخبر Flask و SQLAlchemy بالكيانات الجاهزة للتعميد في قاعدة البيانات
__all__ = [
    'db', 
    'User', 
    'Supplier', 
    'SupplierStaff'
    # 'Product', 
    # 'Order',
    # 'OrderItem'
]

# رسالة للمطور تظهر في سجلات Railway عند نجاح التهيئة
# print("🛡️ [CORE MODELS] All sovereign entities registered successfully.")
