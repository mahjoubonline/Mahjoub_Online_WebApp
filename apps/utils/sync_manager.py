# 📂 apps/utils/sync_manager.py

from apps.orders.services import OrderService
from apps.supplier_wallet.services import WalletService

class SyncManager:
    @staticmethod
    def run_sync(api_key, supplier_id):
        """
        هذا هو "المصنع" أو المنسق الذي طلبت توضيحه.
        يأخذ البيانات من الطلبات (المستكشف) ويدفعها للمحفظة (الخزنة).
        """
        # 1. جلب البيانات الخام
        orders = OrderService.fetch_completed_orders(api_key)
        
        # 2. التنسيق والترحيل
        for order in orders:
            WalletService.sync_order_payment(
                supplier_id=supplier_id,
                order_id=order['id'],
                amount=order['netAmount'],
                currency=order['currency']
            )
        return True
