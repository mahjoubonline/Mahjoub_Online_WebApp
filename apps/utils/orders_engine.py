# 📂 apps/utils/orders_engine.py
from apps.extensions import db
from apps.models.order_db import Order
import requests
import logging

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        self.api_url = "https://mahjoub.online/admin/graphql"
        self.api_key = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        print("DEBUG: تنفيذ الاستعلام الفعلي لجلب الطلبات...")
        # استخدام الأسماء الحقيقية التي اكتشفناها من الـ Schema
        payload = {
            "query": """
            query {
                findAllOrders(input: { limit: 50, page: 1 }) {
                    data {
                        _id
                        totalPrice
                        status { name }
                        account { name }
                        items {
                            # سنحتاج لاحقاً لجلب تفاصيل المنتجات للربط بالموردين
                            # مؤقتاً نكتفي بجلب البيانات الأساسية
                        }
                    }
                }
            }
            """
        }
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            result = response.json()
            
            orders = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            print(f"DEBUG: تم جلب {len(orders)} طلب بنجاح.")
            return orders
        except Exception as e:
            print(f"DEBUG: خطأ أثناء جلب الطلبات: {str(e)}")
            return []

    def sync_orders_to_db(self):
        print("DEBUG: بدء عملية المزامنة وحفظ البيانات...")
        orders = self.fetch_orders_from_qumra()
        
        count = 0
        for item in orders:
            order_id = str(item.get('_id'))
            if not order_id: continue
            
            # البحث عن الطلب أو إنشاؤه
            order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
            
            # تحديث الحقول الأساسية
            order.total = float(item.get('totalPrice', 0))
            # الحالة تأتي ككائن {name: "..."}
            status_obj = item.get('status')
            order.status = status_obj.get('name') if isinstance(status_obj, dict) else "unknown"
            
            # اسم العميل
            account_obj = item.get('account')
            order.customer_name = account_obj.get('name') if isinstance(account_obj, dict) else "غير معروف"
            
            order.raw_data = item
            db.session.add(order)
            count += 1
        
        db.session.commit()
        print(f"DEBUG: تمت المزامنة بنجاح، تم تحديث {count} طلب.")
