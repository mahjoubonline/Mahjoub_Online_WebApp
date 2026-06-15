# 📂 apps/utils/orders_engine.py
from apps.extensions import db
from apps.models.order_db import Order
import logging
import requests # تأكد من وجود مكتبة requests في requirements.txt

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        # تأكد من وضع الـ API Token الخاص بك هنا
        self.api_url = "https://api.qumra.cloud/v1/orders" 
        self.headers = {
            "Authorization": "Bearer YOUR_API_TOKEN_HERE",
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        """جلب الطلبات من API منصة قمرة"""
        try:
            response = requests.get(self.api_url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get('data', []) # نفترض أن البيانات داخل مفتاح 'data'
            else:
                logger.error(f"فشل الاتصال بـ API قمرة: {response.status_code}")
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
            # استخدام الحقول المباشرة (Flat Fields) حسب إفادة شهاب
            q_id = str(o.get('orderId'))
            
            # التحقق من وجود الطلب لمنع التكرار
            existing = Order.query.filter_by(order_id_qumra=q_id).first()
            
            if not existing:
                # إنشاء الطلب الجديد مع مطابقة الحقول المسطحة
                new_order = Order(
                    order_id_qumra=q_id,
                    customer_name=o.get('customerName', 'غير معروف'),
                    total=float(o.get('totalPriceWithTax', 0)),
                    status='pending', # الحالة الافتراضية
                    payment_status='unpaid'
                )
                db.session.add(new_order)
        
        db.session.commit()
        logger.info("تمت مزامنة الطلبات بنجاح إلى قاعدة البيانات.")
