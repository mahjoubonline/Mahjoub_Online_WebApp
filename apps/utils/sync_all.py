# 📂 apps/utils/sync_all.py
import logging
from apps.extensions import db
from apps.utils.orders_engine import get_pending_orders
# افترضنا وجود كلاس الطلبات في ملف الموديلات
from apps.models.wallet_db import WalletTransaction 

logger = logging.getLogger(__name__)

def sync_orders_to_local():
    """
    جلب الطلبات المعلقة من منصة قمرة وحفظها في قاعدة البيانات المحلية.
    """
    logger.info("Starting synchronization process...")
    
    try:
        # 1. جلب الطلبات من المحرك
        remote_orders = get_pending_orders()
        
        if not remote_orders:
            logger.info("No pending orders found to sync.")
            return {"status": "success", "count": 0}
            
        count = 0
        for order in remote_orders:
            # 2. التحقق مما إذا كان الطلب موجوداً مسبقاً (لتجنب التكرار)
            existing = WalletTransaction.query.filter_by(order_id=str(order['id'])).first()
            
            if not existing:
                # 3. إنشاء سجل جديد في قاعدة البيانات المحلية
                new_txn = WalletTransaction(
                    order_id=str(order['id']),
                    amount=str(order.get('totalPrice', 0)),
                    currency='SAR', # أو حسب عملة قمرة
                    transaction_type='pending',
                    description=f"Sync from Qumra: Order #{order['id']}",
                    status='pending'
                )
                db.session.add(new_txn)
                count += 1
        
        # 4. حفظ التغييرات
        db.session.commit()
        logger.info(f"Successfully synced {count} new orders.")
        return {"status": "success", "count": count}

    except Exception as e:
        db.session.rollback()
        logger.error(f"Critical error during sync: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # هذا الجزء يسمح لك بتشغيل المزامنة يدوياً من السيرفر
    sync_orders_to_local()
