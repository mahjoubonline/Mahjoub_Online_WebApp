# coding: utf-8
# 📂 apps/models/__init__.py
# تجميع وإشهار النماذج لسهولة الاستيراد من خارج حزمة models

from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet as Wallet, WalletTransaction
from apps.models.settlements_db import AdminSettlement

# نستخدم الاستيراد المؤجل (Lazy Import) داخل ملفات الـ routes إذا لزم الأمر، 
# لكن سنبقي الإشهار هنا بشرط أن لا يستورد statement_db أي موديل من هذا الملف.
from apps.models.statement_db import SupplierStatement

__all__ = [
    'AdminUser',
    'Supplier',
    'Wallet',
    'WalletTransaction',
    'AdminSettlement',
    'SupplierStatement'
]
