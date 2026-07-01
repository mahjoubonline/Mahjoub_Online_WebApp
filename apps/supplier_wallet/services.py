# 📂 apps/supplier_wallet/services.py (مُعدل ومجهز)

from decimal import Decimal, InvalidOperation
from apps.models.wallet_db import SupplierWallet, WalletTransaction
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

        # معالجة الرقم لضمان كونه Decimal (حل جذري لمشكلة الـ Data Seed)
        try:
            decimal_amount = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            decimal_amount = Decimal('0.00')

        # تسجيل القيد
        transaction = WalletTransaction(
            wallet_id=wallet.id,
            trans_type=trans_type,
            source_type=source_type,
            amount=decimal_amount, # استخدام القيمة المحولة
            currency=currency,
            description=description,
            reference_number=reference_number,
            owner_id=supplier_id 
        )
        
        db.session.add(transaction)
        db.session.commit() # تفعيل event listener لتحديث الرصيد
        return transaction

    @staticmethod
    def sync_order_payment(supplier_id, order_id, amount, currency):
        # التحويل هنا يضمن أن القيمة المرسلة من الـ API (غالباً float) تصبح Decimal فوراً
        return WalletService.process_transaction(
            supplier_id=supplier_id,
            amount=amount, 
            trans_type='credit',
            currency=currency,
            description=f"تسوية مالية تلقائية للطلب رقم {order_id}",
            reference_number=f"QMR-{order_id}",
            source_type='system_sync'
        )
