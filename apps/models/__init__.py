# coding: utf-8
# 📂 apps/models/__init__.py - مجمع النماذج المحصنة

from .supplier_db import Supplier
from .wallet_db import SupplierWallet, WalletTransaction
from .statement_db import SupplierStatement
from .settlements_db import AdminSettlement
from .admin_db import AdminUser

# هذا الملف يجعل من السهل استيراد أي نموذج من أي مكان في التطبيق
# مثلاً يمكنك كتابة: from apps.models import Supplier
