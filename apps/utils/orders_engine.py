# 📂 apps/utils/orders_engine.py
from flask import current_app
from apps.extensions import db
from apps.models.order_db import Order
import logging
import requests

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        # استخدام الرابط والمفتاح من الإعدادات (config.py)
        # تأكد من أن هذه القيم في Render Environment هي الصحيحة
        self.api_url = current_app.config.get('QUMRA_API_URL', "https://api.qumra.cloud/v1/orders")
        self.api_key = current_app.config.get('QUMRA_API_KEY')
        
        # التعديل هنا: استخدام المفتاح الحقيقي من الإعدادات
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        """جلب الطلبات من API منصة قمرة"""
        try:
            response = requests.get(self.api_url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get('data', [])
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
            q_id = str(o.get('orderId'))
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
