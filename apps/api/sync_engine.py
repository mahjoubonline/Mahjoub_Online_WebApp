# coding: utf-8
# 📂 apps/api/sync_engine.py - المحرك السيادي للمزامنة (نسخة التشخيص والعمل)

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
        logger.info("🔄 بدء المزامنة الموسعة...")
        
        # الاستعلام الذي اعتمدته
        query = """
        query {
            findAllOrders(input: {}) {
                data {
                    _id
                    totalPrice
                    createdAt
                    status { code }
                    items { productId }
                    customer { name phone }
                    shipping { city address }
                }
            }
        }
        """
        
        try:
            response = requests.post(SyncEngine.API_URL, json={'query': query}, headers=SyncEngine._get_headers(), timeout=120)
            result = response.json()
            
            # معالجة الأخطاء الذكية
            if 'errors' in result:
                # تسجيل الخطأ بوضوح لتتمكن من معرفة الحقل المرفوض
                error_msg = result['errors'][0].get('message', 'خطأ غير معروف في GraphQL')
                logger.error(f"❌ خطأ GraphQL: {error_msg}")
                return False
            
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            for item in orders_data:
                order_id = str(item.get('_id'))
                if not order_id: continue
                
                order = ProcessedOrder.query.filter_by(id=order_id).first() or ProcessedOrder(id=order_id)
                
                # 1. البيانات الأساسية
                order.order_id = order_id[-8:]
                order.total_price = float(item.get('totalPrice') or 0.0)
                order.order_status = item.get('status', {}).get('code', 'pending')
                order.items_count = len(item.get('items') or [])
                
                # 2. بيانات العميل
                cust = item.get('customer') or {}
                order.customer_name = cust.get('name') or "غير معروف"
                order.customer_phone = cust.get('phone')
                
                # 3. بيانات الشحن
                ship = item.get('shipping') or {}
                order.shipping_city = ship.get('city') or "غير محدد"
                order.shipping_street = ship.get('address')
                
                db.session.add(order)
            
            db.session.commit()
            logger.info(f"✅ تمت مزامنة {len(orders_data)} طلب بنجاح.")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ خطأ فني غير متوقع أثناء المزامنة: {str(e)}")
            return False
