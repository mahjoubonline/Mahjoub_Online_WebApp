# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المحدث

import requests
import logging
from apps.extensions import db
# تم تحديث الاستيراد ليعتمد على الموديل الجديد Order
from apps.models.orders_db import Order

logger = logging.getLogger(__name__)

class SyncEngine:
    API_URL = "https://mahjoub.online/admin/graphql"  
    API_TOKEN = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"

    @staticmethod
    def _get_headers():
        return {
            "Authorization": f"Bearer {SyncEngine.API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def fetch_and_sync_order():
        logger.info("🔄 بدء المزامنة مع استبعاد الحقول المرفوضة...")
        
        query = """
        query {
            findAllOrders {
                data {
                    _id
                    totalPrice
                    status { code }
                    account { 
                        firstName
                        lastName
                    }
                    shippingAddress { 
                        city { name } 
                        street 
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(
                SyncEngine.API_URL, 
                json={'query': query}, 
                headers=SyncEngine._get_headers(), 
                timeout=60
            )
            
            if response.status_code != 200:
                logger.error(f"❌ خطأ اتصال ({response.status_code}): {response.text}")
                return False

            result = response.json()
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            sync_count = 0
            for item in orders_data:
                unique_id = str(item.get('_id'))
                if not unique_id: continue
                
                # استخدام الكلاس المحدث Order
                order = Order.query.filter_by(id=unique_id).first() or Order(id=unique_id)
                
                # تحديث البيانات الأساسية
                order.total_price = float(item.get('totalPrice') or 0.0)
                order.order_status = item.get('status', {}).get('code', 'pending')
                
                # تحديث بيانات العميل
                acc = item.get('account') or {}
                first_name = acc.get('firstName', '')
                last_name = acc.get('lastName', '')
                order.customer_name = f"{first_name} {last_name}".strip() or "غير معروف"
                
                # بيانات الشحن
                ship = item.get('shippingAddress') or {}
                city_obj = ship.get('city') or {}
                order.shipping_city = city_obj.get('name') or "---"
                order.shipping_street = ship.get('street') or "---"
                
                db.session.add(order)
                sync_count += 1
            
            db.session.commit()
            logger.info(f"✅ تمت المزامنة بنجاح لعدد {sync_count} طلب.")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ خطأ فني أثناء المزامنة: {str(e)}")
            return False
