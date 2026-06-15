# 📂 apps/utils/orders_engine.py
from flask import current_app
from apps.extensions import db
from apps.models.order_db import Order
import logging
import requests

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        self.api_url = current_app.config.get('QUMRA_API_URL', "https://mahjoub.online/admin/graphql")
        self.api_key = current_app.config.get('QUMRA_API_KEY')
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        """جلب الطلبات باستخدام الاستعلام الصحيح (GraphQL)"""
        
        # وفقاً للصورة التي أرسلتها، يجب أن يكون الهيكل مطابقاً لما هو مكتوب في Sandbox
        query_payload = {
            "query": """
            query {
              orders {
                _id
                customer {
                  name
                }
                total
                status
              }
            }
            """
        }
        
        try:
            response = requests.post(self.api_url, json=query_payload, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                # نرجع البيانات من دالة orders كما هو متوقع
                return result.get('data', {}).get('orders', [])
            else:
                logger.error(f"خطأ: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"خطأ أثناء الاتصال: {str(e)}")
            return []

    def sync_orders_to_db(self):
        """مزامنة الطلبات"""
        raw_orders = self.fetch_orders_from_qumra()
        
        if not raw_orders:
            logger.warning("لم يتم جلب أي طلبات (تحقق من اسم الدالة في الـ GraphQL).")
            return

        for o in raw_orders:
            # استخدام _id كما ظهر في الصورة
            q_id = str(o.get('_id'))
            
            existing = Order.query.filter_by(order_id_qumra=q_id).first()
            if not existing:
                new_order = Order(
                    order_id_qumra=q_id,
                    customer_name=o.get('customer', {}).get('name', 'غير معروف'),
                    total=float(o.get('total', 0)),
                    status=o.get('status', 'pending')
                )
                db.session.add(new_order)
        
        db.session.commit()
        logger.info("تمت المزامنة بنجاح.")
