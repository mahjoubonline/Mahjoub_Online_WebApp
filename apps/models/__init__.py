# coding: utf-8
# 📂 apps/models/__init__.py - مجمع النماذج المحدث

from .admin_db import AdminUser
from .supplier_db import Supplier
from .wallet_db import SupplierWallet, WalletTransaction
from .vault_db import AdminVault, VaultTransaction
from .financial_db import ExchangeRate, FinancialLog
# (تم حذف سطر استيراد bridge_db)

__all__ = [
    'AdminUser', 
    'Supplier', 
    'SupplierWallet', 
    'WalletTransaction', 
    'AdminVault', 
    'VaultTransaction',
    'ExchangeRate',
    'FinancialLog'
    # (تم حذف Product و ProductVariant من هنا)
]
