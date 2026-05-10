# core/models/__init__.py

# 1. استيراد قاعدة البيانات (التوحيد السيادي)
from core import db 

# 2. استيراد الكيانات الأساسية (النواة الرقمية)
from .user import User
from .supplier import Supplier, SupplierStaff
# تأكد من وجود هذه الملفات أو قم بتعطيلها مؤقتاً إذا لم تكن جاهزة
# from .product import Product
# from .business import Order, OrderItem

# 3. بروتوكول التصدير الموحد (__all__)
__all__ = [
    'db', 
    'User', 
    'Supplier', 
    'SupplierStaff'
    # 'Product', 
    # 'Order',
    # 'OrderItem'
]
