# coding: utf-8
# 📂 apps/models/__init__.py - التنسيق النهائي والمستقر للموديلات البرمجية (منصة Mahjoub Online)

from .admin_db import AdminUser
from .financial_db import ExchangeRate, FinancialLog
from .supplier_db import Supplier
from .vault_db import AdminVault, VaultTransaction
from .wallet_db import SupplierWallet, WalletTransaction
from .orders_db import ProcessedOrder, OrderItem  # 👈 تم إضافة OrderItem لضمان التثبيت الكامل ومنع الدوران
from .sync_log import SyncLog

__all__ = [
    'AdminUser',
    'ExchangeRate',
    'FinancialLog',
    'Supplier',
    'AdminVault',
    'VaultTransaction',
    'SupplierWallet',
    'WalletTransaction',
    'ProcessedOrder',
    'OrderItem',  # 👈 تصدير معتمد لطبقة التحكم والـ Migrations
    'SyncLog'
]
