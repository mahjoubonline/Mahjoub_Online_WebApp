# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المحدث

import os
import requests
import logging
from apps.extensions import db
from apps.models.sync_log import SyncLog
from apps.models.wallet_db import WalletTransaction, SupplierWallet
from apps.models.orders_db import Order

logger = logging.getLogger(__name__)

class SyncEngine:
    API_URL = "https://mahjoub.online/admin/graphql"  

    @staticmethod
    def _get_headers():
        api_key = os.environ.get("QUMRA_API_KEY", "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def process_financials(order_id, supplier_id, total_price, marketer_id=None):
        """توزيع مالي ذكي للحصص: المورد، المنصة، المسوق"""
        try:
            # 1. جلب المحفظة
            wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
            if not wallet: return False

            # 2. منطق الحسابات (هنا يمكنك تعديل النسب لاحقاً)
            supplier_cost = total_price * 0.8  # مثال: 80% للمورد
            platform_profit = total_price * 0.2 # مثال: 20% للمنصة
            
            # إذا وجد مسوق، نخصم حصته من ربح المنصة
            if marketer_id:
                marketer_share = platform_profit * 0.5 # 50% من ربح المنصة للمسوق
                platform_profit -= marketer_share
                db.session.add(WalletTransaction(wallet_id=wallet.id, owner_id=marketer_id, trans_type='marketer_commission', amount=marketer_share, currency='SAR', order_id=order_id))

            # تسجيل حركات المحفظة
            db.session.add(WalletTransaction(wallet_id=wallet.id, owner_id=supplier_id, trans_type='supplier_cost', amount=supplier_cost, currency='SAR', order_id=order_id))
            db.session.add(WalletTransaction(wallet_id=wallet.id, owner_id=1, trans_type='platform_commission', amount=platform_profit, currency='SAR', order_id=order_id))
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ خطأ في التوزيع المالي: {e}")
            return False

    @staticmethod
    def fetch_and_sync_order():
        query = """
        query {
            findAllOrders {
                id
                totalPrice
                status
                supplierId
                trackingTag
            }
        }
        """
        # ... (بقية كود الاتصال بـ API) ...
        # عند المعالجة:
        # if not exists:
        #    if SyncEngine.process_financials(order['id'], order['supplierId'], order['totalPrice'], order.get('trackingTag')):
        #        logger.info(f"✅ تمت التسوية الذكية للطلب {order['id']}")
