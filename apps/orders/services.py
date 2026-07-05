from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.extensions import db
from decimal import Decimal

class OrderService:
    @staticmethod
    def get_order_details(order_id):
        # جلب الطلب مع بياناته المالية
        result = db.session.query(Order, OrderFinancial)\
            .outerjoin(OrderFinancial, Order.id == OrderFinancial.order_id)\
            .filter(Order.id == str(order_id)).first()
        return result if result else (None, None)

    @staticmethod
    def complete_order_and_settle(order_id):
        """
        محرك التسوية: يحول الطلب لمكتمل ويوزع الأرباح للمورد في محفظته
        """
        order = Order.query.get(str(order_id))
        financial = OrderFinancial.query.filter_by(order_id=str(order_id)).first()
        
        if order and financial and order.status != 'completed':
            # 1. تحديث حالة الطلب والمالية
            order.status = 'completed'
            financial.settlement_status = 'settled'
            
            # 2. إيداع المبلغ في محفظة المورد
            wallet = SupplierWallet.query.filter_by(supplier_id=financial.supplier_id).first()
            if wallet:
                # إنشاء سجل حركة مالية
                transaction = WalletTransaction(
                    wallet_id=wallet.id,
                    owner_type='supplier',
                    owner_id=financial.supplier_id,
                    trans_type='sale_revenue',
                    amount=Decimal(str(financial.total_paid_raw)),
                    currency=financial.currency,
                    description=f"تسوية الطلب رقم {order.order_id_display}",
                    related_order_id=str(order.id)
                )
                db.session.add(transaction)
            
            db.session.commit()
            return True
        return False
