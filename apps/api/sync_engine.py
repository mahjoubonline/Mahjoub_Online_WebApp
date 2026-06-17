# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المحدث (التوافق مع Schema)

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
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apollo-require-preflight": "true"
        }

    @staticmethod
    def fetch_and_sync_order():
        """جلب ومزامنة الطلبات بناءً على الـ Schema الجديدة"""
        query = """
        query {
            findAllOrders {
                data {
                    _id
                    status
                    totalPrice
                    createdAt
                    isPaid
                }
            }
        }
        """
        try:
            response = requests.post(
                SyncEngine.API_URL, 
                json={'query': query}, 
                headers=SyncEngine._get_headers(),
                timeout=15
            )
            
            if response.status_code != 200:
                logger.error(f"❌ [SyncEngine] فشل الاتصال. حالة الـ HTTP: {response.status_code}")
                return False

            result = response.json()
            
            if 'errors' in result:
                logger.error(f"❌ [SyncEngine] خطأ من API قمرة: {result['errors']}")
                return False
            
            # تصحيح مسار الوصول للبيانات حسب الـ Schema
            # findAllOrders -> data -> [list of orders]
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            if not orders_data:
                logger.warning("⚠️ [SyncEngine] لم يتم العثور على طلبات في استجابة الـ API.")
                return False

            logger.info(f"🔍 [SyncEngine] تم استلام {len(orders_data)} طلب.")

            for item in orders_data:
                # المعرف هو _id وليس orderId
                order_id = str(item.get('_id'))
                if not order_id: continue
                
                order = ProcessedOrder.query.get(order_id)
                if not order:
                    order = ProcessedOrder(id=order_id)
                
                # تحديث البيانات المتاحة
                order.status = item.get('status')
                order.total_price = float(item.get('totalPrice', 0))
                
                # معالجة التاريخ
                created_at = item.get('createdAt')
                if created_at:
                    try:
                        # حذف حرف Z إذا وجد وتنسيق التاريخ
                        date_str = created_at.replace('Z', '+00:00')
                        order.created_at_api = datetime.fromisoformat(date_str)
                    except: pass
                
                db.session.add(order)
            
            db.session.commit()
            logger.info("✅ تم حفظ الطلبات بنجاح.")
            return True

        except Exception as e:
            logger.error(f"❌ [SyncEngine] خطأ تقني: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def _execute_mutation(mutation, variables):
        try:
            response = requests.post(
                SyncEngine.API_URL, 
                json={'query': mutation, 'variables': variables}, 
                headers=SyncEngine._get_headers()
            )
            return response.json()
        except Exception as e:
            logger.error(f"❌ [SyncEngine] خطأ Mutation: {e}")
            return None

    @staticmethod
    def cancel_order(order_id):
        mutation = "mutation($id: ID!) { cancelOrder(id: $id) { _id status } }"
        return SyncEngine._execute_mutation(mutation, {"id": order_id})

    @staticmethod
    def mark_as_fulfilled(order_id):
        mutation = "mutation($id: ID!) { markOrderFulfilled(id: $id) { _id status } }"
        return SyncEngine._execute_mutation(mutation, {"id": order_id})

    @staticmethod
    def update_order_status(order_id, new_status):
        mutation = "mutation($id: ID!, $status: String!) { updateOrderStatus(id: $id, status: $status) { _id status } }"
        return SyncEngine._execute_mutation(mutation, {"id": order_id, "status": new_status})
