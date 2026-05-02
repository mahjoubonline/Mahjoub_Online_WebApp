# core/models/__init__.py
from core import db

# استيراد الموديل لضمان تسجيله في SQL Alchemy
from core.models.user import User

# بمجرد أن تجهز ملفات الموردين والطلبات، قم بإلغاء التعليق:
# from core.models.supplier import Supplier
# from core.models.order import Order

# تعريف الحزم المصدرة
__all__ = ['User']
