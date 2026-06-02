# coding: utf-8
# 📂 apps/models/__init__.py
# هذا الملف مسؤول عن تصدير جميع جداول قاعدة البيانات (Models) 
# ليتسنى لـ SQLAlchemy و Flask-Migrate التعرف عليها.

from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import Wallet, WalletTransaction
from apps.models.settlements_db import AdminSettlement
from apps.models.statement_db import SupplierStatement

# قائمة التصدير الرسمية لتنظيم الوصول للنماذج
__all__ = [
    'AdminUser',
    'Supplier',
    'Wallet',
    'WalletTransaction',
    'AdminSettlement',
    'SupplierStatement'
]
