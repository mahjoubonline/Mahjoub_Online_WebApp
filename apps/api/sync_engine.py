# 📂 apps/api/sync_engine.py - محرك المزامنة (النسخة المكتملة)

import logging
import requests
from config import Config
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder

logger = logging.getLogger(__name__)

class SyncEngine:
    
    @staticmethod
    def fetch_and_sync_order(order_id):
        """جلب تفاصيل الطلب من المتجر مباشرة عبر API ثم مزامنته"""
        try:
            # 1. الاتصال بمتجر محجوب
            url = f"{Config.STORE_BASE_URL}/admin/graphql" # أو الرابط الصحيح للـ API
            headers = {"Authorization": f"Bearer {Config.QUMRA_API_KEY}"}
            
            # استعلام GraphQL (مثال)
            query = {"query": "{ order(id: " + order_id + ") { status total { amount } } }"}
            
            response = requests.post(url, json=query, headers=headers)
            if response.status_code == 200:
                order_data = response.json().get('data', {}).get('order', {})
                return SyncEngine.sync_order_data(order_data)
            
            return False
        except Exception as e:
            logger.error(f"❌ [SyncEngine] خطأ أثناء الاتصال بالمتجر: {e}")
            return False

    @staticmethod
    def sync_order_data(order_data):
        """يقوم بمعالجة بيانات الطلب وحفظها في قاعدة البيانات"""
        try:
            order_id = str(order_data.get('id', ''))
            if not order_id: return False

            order = ProcessedOrder.query.get(order_id) or ProcessedOrder(id=order_id)

            order.status = order_data.get('status', 'pending')
            total_amount = order_data.get('total', {}).get('amount', 0.0)
            order.total_price = float(total_amount)

            db.session.add(order)
            db.session.commit()
            logger.info(f"🔄 [SyncEngine] تمت مزامنة الطلب {order_id} بنجاح.")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ [SyncEngine] خطأ أثناء المزامنة: {e}")
            return False
