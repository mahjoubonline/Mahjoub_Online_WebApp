from core import db

# استيراد الموديلات من الملفات الفرعية داخل المجلد
from .user import User
from .supplier import Supplier
from .product import Product

# جعل الموديلات متاحة للاستيراد المباشر
__all__ = ['User', 'Supplier', 'Product']
