# coding: utf-8
# 📂 apps/models/__init__.py - مجمع النماذج المحصنة (النسخة السيادية المكتملة)

from .admin_db import AdminUser
from .supplier_db import Supplier
from .wallet_db import SupplierWallet, WalletTransaction
from .vault_db import AdminVault, VaultTransaction
from .financial_db import ExchangeRate, FinancialLog

# هذا الملف يضمن استيراد النماذج ليتعرف عليها نظام المهاجرات (Flask-Migrate)
# ويجعل من السهل استيراد أي نموذج من أي مكان في التطبيق.
__all__ = [
    'AdminUser', 
    'Supplier', 
    'SupplierWallet', 
    'WalletTransaction', 
    'AdminVault', 
    'VaultTransaction',
    'ExchangeRate',
    'FinancialLog'
]
