# 📂 apps/utils/sync_all.py
import logging
from apps.utils.orders_engine import get_pending_orders

logger = logging.getLogger(__name__)

def sync_orders_to_local_db():
    """
    مزامنة الطلبات محلياً مع حقن الموديلات داخلياً لمنع الـ Circular Import.
    """
    from apps.models.wallet_db import WalletTransaction
    from apps.extensions import db
    
    try:
        pending_orders = get_pending_orders()
        count = 0
        
        for order in pending_orders:
            existing = WalletTransaction.query.filter_by(order_id=str(order['id'])).first()
            if not existing:
                new_txn = WalletTransaction(
                    order_id=str(order['id']),
                    amount=float(order.get('totalPrice', 0)),
                    currency='SAR',
                    status='pending'
                )
                db.session.add(new_txn)
                count += 1
                
        db.session.commit()
        return count
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error syncing orders in sync_all: {str(e)}")
        return 0
