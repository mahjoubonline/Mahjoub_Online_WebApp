# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المتكامل مع منصة قمرة (GraphQL)

import requests
import logging
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
        """جلب جميع الطلبات ومزامنتها مع قاعدة البيانات المحلية"""
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

            for item in orders_data:
                # البحث عن الطلب محلياً
                order = ProcessedOrder.query.get(str(item['orderId']))
                if not order:
                    order = ProcessedOrder(id=str(item['orderId']))
                
                # تحديث البيانات (المشفرة)
                order.customer_name = item['customerName']
                order.total_price = float(item['total'])
                order.status = item['status']
                
                db.session.add(order)
            
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"❌ [SyncEngine] خطأ أثناء الجلب: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def _execute_mutation(mutation, variables):
        """دالة مساعدة لتنفيذ إجراءات قمرة"""
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
        """إلغاء الطلب في قمرة"""
        mutation = "mutation($id: ID!) { cancelOrder(id: $id) { id status } }"
        return SyncEngine._execute_mutation(mutation, {"id": order_id})

    @staticmethod
    def mark_as_fulfilled(order_id):
        """تعليم الطلب كمشحون في قمرة"""
        mutation = "mutation($id: ID!) { markOrderFulfilled(id: $id) { id status } }"
        return SyncEngine._execute_mutation(mutation, {"id": order_id})

    @staticmethod
    def update_order_status(order_id, new_status):
        """تحديث حالة الطلب يدوياً"""
        mutation = "mutation($id: ID!, $status: String!) { updateOrderStatus(id: $id, status: $status) { id status } }"
        return SyncEngine._execute_mutation(mutation, {"id": order_id, "status": new_status})
