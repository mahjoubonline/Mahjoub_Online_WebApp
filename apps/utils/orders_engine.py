# 📂 apps/utils/orders_engine.py
from flask import current_app
from apps.extensions import db
from apps.models.order_db import Order
import logging
import requests

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        # جلب الإعدادات من ملف الـ Config
        self.api_url = current_app.config.get('QUMRA_API_URL', "https://mahjoub.online/admin/graphql")
        self.api_key = current_app.config.get('QUMRA_API_KEY')
        
        # الـ Headers اللازمة لاتصال GraphQL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        """جلب الطلبات من API منصة قمرة باستخدام GraphQL"""
        
        # الاستعلام (Query) لجلب الطلبات
        # تأكد من مطابقة الحقول هنا مع ما توفره منصة قمرة في الـ Schema الخاص بها
        query = {
            "query": """
            query {
              orders {
                orderId
                customerName
                totalPriceWithTax
              }
            }
            """
        }
        
        try:
            # GraphQL يتطلب إرسال الطلب كـ POST
            response = requests.post(self.api_url, json=query, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                # جلب البيانات من مسار 'data.orders' الخاص بـ GraphQL
                return result.get('data', {}).get('orders', [])
            else:
                logger.error(f"فشل الاتصال بـ API قمرة: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"خطأ أثناء جلب الطلبات: {str(e)}")
            return []

    def sync_orders_to_db(self):
        """مزامنة الطلبات وحفظها في قاعدة البيانات المحلية"""
        raw_orders = self.fetch_orders_from_qumra() 
        
        if not raw_orders:
            logger.warning("لم يتم جلب أي طلبات من المنصة.")
            return

        for o in raw_orders:
            # استخدام الحقول كما يتم استرجاعها من الـ GraphQL Query
            q_id = str(o.get('orderId'))
            
            # التحقق من وجود الطلب لمنع التكرار
            existing = Order.query.filter_by(order_id_qumra=q_id).first()
            
            if not existing:
                new_order = Order(
                    order_id_qumra=q_id,
                    customer_name=o.get('customerName', 'غير معروف'),
                    total=float(o.get('totalPriceWithTax', 0)),
                    status='pending',
                    payment_status='unpaid'
                )
                db.session.add(new_order)
        
        db.session.commit()
        logger.info("تمت مزامنة الطلبات بنجاح إلى قاعدة البيانات.")
