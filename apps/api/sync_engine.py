# coding: utf-8
import requests
import logging
from apps.extensions import db

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
        from apps.models import ProcessedOrder
        
        logger.info("🔄 بدء المزامنة الكاملة من محجوب أونلاين...")
        
        # استعلام GraphQL محسن ومتوافق مع المعايير
        query = """
        query {
            findAllOrders {
                data {
                    _id
                    totalPrice
                    createdAt
                    status { code }
                    items { productTitle quantity price }
                    account { name phone email }
                    shippingAddress { city address1 }
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
            
            # في حال وجود خطأ 400 أو غيره، سنطبع المحتوى لمعرفة السبب الدقيق
            if response.status_code != 200:
                logger.error(f"❌ فشل الاتصال بالسيرفر! الكود: {response.status_code}")
                logger.error(f"📝 تفاصيل استجابة السيرفر: {response.text}")
                return False

            result = response.json()
            
            if 'errors' in result:
                logger.error(f"❌ خطأ GraphQL: {result['errors']}")
                return False
            
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            if not orders_data:
                logger.warning("⚠️ لم يتم استرجاع أي بيانات من السيرفر.")
                return True
            
            sync_count = 0
            for item in orders_data:
                order_id = str(item.get('_id'))
                if not order_id: continue
                
                # جلب الطلب أو إنشاؤه
                order = ProcessedOrder.query.filter_by(id=order_id).first() or ProcessedOrder(id=order_id)
                
                # تحديث البيانات (الموديل سيقوم بتشفيرها تلقائياً عبر ה-setters)
                order.order_id = order_id[-8:]
                order.total_price = float(item.get('totalPrice') or 0.0) 
                order.order_status = item.get('status', {}).get('code', 'pending')
                
                acc = item.get('account') or {}
                order.customer_name = acc.get('name') or "---"
                order.customer_phone = acc.get('phone') or "---"
                order.customer_email = acc.get('email') or "---"
                
                ship = item.get('shippingAddress') or {}
                order.shipping_city = ship.get('city') or "---"
                order.shipping_street = ship.get('address1') or "---"
                
                db.session.add(order)
                sync_count += 1
            
            db.session.commit()
            logger.info(f"✅ تمت مزامنة {sync_count} طلب بنجاح.")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ خطأ فني أثناء المزامنة: {str(e)}")
            return False
