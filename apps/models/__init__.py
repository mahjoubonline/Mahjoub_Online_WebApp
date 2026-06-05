# coding: utf-8
# 📂 apps/models/__init__.py - مجمع النماذج المحصنة (النسخة المستقرة)

from .admin_db import AdminUser
from .supplier_db import Supplier
from .wallet_db import SupplierWallet, WalletTransaction

# هذا الملف يضمن استيراد النماذج ليتعرف عليها نظام المهاجرات (Flask-Migrate)
# ويجعل من السهل استيراد أي نموذج من أي مكان في التطبيق.
