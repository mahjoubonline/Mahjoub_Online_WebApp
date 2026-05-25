# coding: utf-8
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet
from apps.models.settlements_db import AdminSettlement

# ربط إضافي لضمان أن wallet.routes يرى الموديل باسم Wallet
Wallet = SupplierWallet
