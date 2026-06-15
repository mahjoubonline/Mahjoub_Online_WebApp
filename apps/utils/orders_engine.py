# 📂 apps/utils/orders_engine.py
from flask import current_app
from apps.extensions import db
from apps.models.order_db import Order
import logging
import requests

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        # تأكد أن الرابط والتوكن في إعدادات Render صحيحة
        self.api_url = "https://mahjoub.online/admin/graphql"
        self.api_key = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        """جلب الطلبات باستخدام الدالة findAllOrders"""
        query_name = "findAllOrders"
        
        # استعلام GraphQL مطابق لهيكلية الـ Sandbox
        payload = {
            "query": f"""
            query {{
                {query_name} {{
                    data {{
                        _id
                        total
                        status
                    }}
                }}
            }}
            """
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            result = response.json()
            
            # التحقق من وجود البيانات في الرد
            if 'data' in result and result['data'].get(query_name):
                logger.info(f"✅ نجح الاتصال وجلب البيانات باستخدام {query_name}")
                return result['data'][query_name].get('data', [])
            else:
                logger.error(f"❌ فشل جلب البيانات. رد السيرفر: {result}")
                return []
                
        except Exception as e:
            logger.error(f"❌ خطأ تقني أثناء الاتصال بـ API قمرة: {str(e)}")
            return []

    def sync_orders_to_db(self):
        """مزامنة الطلبات من قمرة إلى قاعدة البيانات المحلية"""
        orders = self.fetch_orders_from_qumra()
        
        if not orders:
            logger.warning("لم يتم العثور على طلبات للمزامنة.")
            return

        count = 0
        for item in orders:
            order_id = str(item.get('_id'))
            
            # التحقق من عدم تكرار الطلب في قاعدة البيانات
            if not Order.query.filter_by(order_id=order_id).first():
                new_order = Order(
                    order_id=order_id,
                    total=float(item.get('total', 0)),
                    status=str(item.get('status', 'pending'))
                )
                db.session.add(new_order)
                count += 1
        
        try:
            db.session.commit()
            logger.info(f"🚀 تمت مزامنة {count} طلب جديد بنجاح.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ خطأ أثناء حفظ الطلبات في قاعدة البيانات: {str(e)}")
