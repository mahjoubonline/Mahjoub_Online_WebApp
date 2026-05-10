# core/models/__init__.py

# 1. استيراد قاعدة البيانات لضمان وحدة الاتصال
from core.extensions import db 

# 2. استيراد الكيانات الأساسية (النواة الرقمية)
from .user import User
from .supplier import Supplier, SupplierStaff
from .product import Product
from .business import Order, OrderItem

# 3. بروتوكول التصدير الموحد (__all__)
# هذا يسمح لك باستدعاء أي موديل في أي مكان عبر: from core.models import Supplier
__all__ = [
    'db', 
    'User', 
    'Supplier', 
    'SupplierStaff',
    'Product', 
    'Order',
    'OrderItem'
]

# رسالة تأكيد صامتة تظهر عند تهيئة الموديلات (للمطور فقط)
# print("✅ Tarsana Models: Registry Initialized Successfully.")
