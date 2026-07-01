# 📂 apps/supplier_wallet/services.py (مُعدل)

from apps.models import SupplierWallet, WalletTransaction
from apps.extensions import db

class WalletService:
    @staticmethod
    def get_supplier_wallet(supplier_id):
        return SupplierWallet.query.filter_by(supplier_id=supplier_id).first()

    @staticmethod
    def process_transaction(supplier_id, amount, trans_type, currency, description, reference_number, source_type='manual_adjustment'):
        wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
        if not wallet:
            raise ValueError("المحفظة غير موجودة")

        # تسجيل القيد فقط، الـ event listener في wallet_db سيقوم بتحديث الرصيد تلقائياً
        transaction = WalletTransaction(
            wallet_id=wallet.id,
            trans_type=trans_type,
            source_type=source_type,
            amount=amount,
            currency=currency,
            description=description,
            reference_number=reference_number,
            owner_id=supplier_id # إضافة owner_id لضمان تكامل السجلات
        )
        
        db.session.add(transaction)
        db.session.commit() # هنا سيتم تفعيل event listener وتحديث الرصيد
        return transaction

    @staticmethod
    def sync_order_payment(supplier_id, order_id, amount, currency):
        return WalletService.process_transaction(
            supplier_id=supplier_id,
            amount=amount,
            trans_type='credit',
            currency=currency,
            description=f"تسوية مالية تلقائية للطلب رقم {order_id}",
            reference_number=f"QMR-{order_id}",
            source_type='system_sync'
        )
