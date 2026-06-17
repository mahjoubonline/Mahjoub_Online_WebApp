# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المتكامل مع منصة قمرة

import requests
import logging
from datetime import datetime
from apps.models.orders_db import ProcessedOrder, db

logger = logging.getLogger(__name__)

class SyncEngine:
    API_URL = "https://mahjoub.online/admin/graphql"
    API_TOKEN = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"

    @staticmethod
    def _get_headers():
        return {
            "Authorization": f"Bearer {SyncEngine.API_TOKEN}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def fetch_and_sync_order():
        """جلب ومزامنة الطلبات مع معالجة التواريخ والعدد"""
        query = """
        query {
            orders {
                id
                orderId
                customerName
                itemsCount
                total
                status
                createdAt
            }
        }
        """
        try:
            response = requests.post(SyncEngine.API_URL, json={'query': query}, headers=SyncEngine._get_headers())
            result = response.json()
            orders_data = result.get('data', {}).get('orders', [])
            
            logger.info(f"🔍 [SyncEngine] تم استلام {len(orders_data)} طلب من API.")

            for item in orders_data:
                order_id = str(item['orderId'])
                order = ProcessedOrder.query.get(order_id)
                
                if not order:
                    order = ProcessedOrder(id=order_id)
                
                # تحديث كافة الحقول
                order.customer_name = item.get('customerName')
                order.items_count = int(item.get('itemsCount', 0))
                order.total_price = float(item.get('total', 0))
                order.status = item.get('status')
                
                # تحويل التاريخ إذا لزم الأمر
                if item.get('createdAt'):
                    try:
                        order.created_at_api = datetime.fromisoformat(item['createdAt'].replace('Z', '+00:00'))
                    except:
                        pass
                
                db.session.add(order)
            
            db.session.commit()
            logger.info("✅ تم حفظ الطلبات في قاعدة البيانات بنجاح.")
            return True
        except Exception as e:
            logger.error(f"❌ [SyncEngine] خطأ: {e}")
            db.session.rollback()
            return False

    # ... (بقية دوال Mutation ثابتة كما هي)
