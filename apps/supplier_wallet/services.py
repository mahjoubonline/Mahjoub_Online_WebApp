# coding: utf-8
# 📂 apps/supplier_wallet/services.py

from apps.models import SupplierWallet, WalletTransaction
from apps.extensions import db

class WalletService:
    @staticmethod
    def get_supplier_wallet(supplier_id):
        """جلب محفظة المورد بناءً على معرف المورد"""
        return SupplierWallet.query.filter_by(supplier_id=supplier_id).first()

    @staticmethod
    def process_transaction(supplier_id, amount, trans_type, currency, description, reference_number, source_type='manual_adjustment'):
        """
        خدمة معالجة الحركة المالية للمورد
        """
        wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
        if not wallet:
            raise ValueError("المحفظة غير موجودة")

        # تحديث الأرصدة
        if currency == 'SAR':
            wallet.balance_sar += amount if trans_type == 'credit' else -amount
        elif currency == 'YER':
            wallet.balance_yer += amount if trans_type == 'credit' else -amount
        elif currency == 'USD':
            wallet.balance_usd += amount if trans_type == 'credit' else -amount
        else:
            raise ValueError(f"العملة {currency} غير مدعومة")

        # تسجيل القيد
        transaction = WalletTransaction(
            wallet_id=wallet.id,
            trans_type=trans_type,
            source_type=source_type, # تم تعديلها لتسمح بـ 'system_sync' لاحقاً
            amount=amount,
            currency=currency,
            description=description,
            reference_number=reference_number
        )
        
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def sync_order_payment(supplier_id, order_id, amount, currency):
        """
        دالة مخصصة للمزامنة التلقائية مع متجر قمرة
        تستدعي process_transaction مع تحديد نوع المصدر كـ 'system_sync'
        """
        return WalletService.process_transaction(
            supplier_id=supplier_id,
            amount=amount,
            trans_type='credit',
            currency=currency,
            description=f"تسوية مالية تلقائية للطلب رقم {order_id}",
            reference_number=f"QMR-{order_id}",
            source_type='system_sync'
        )

    @staticmethod
    def get_balance_summary(wallet):
        """تجهيز ملخص الأرصدة لعرضه في لوحة الموردين"""
        return {
            'SAR': wallet.balance_sar,
            'YER': wallet.balance_yer,
            'USD': wallet.balance_usd
        }
