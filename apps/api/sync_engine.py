# coding: utf-8
import requests
import logging
from apps.models.orders_db import ProcessedOrder, db
from apps.models.sync_log import SyncLog

logger = logging.getLogger(__name__)

class SyncEngine:
    API_URL = "https://mahjoub.online/admin/graphql"  
    API_TOKEN = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"

    @staticmethod
    def _get_headers():
        return {
            "Authorization": f"Bearer {SyncEngine.API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apollo-require-preflight": "true"
        }

    @staticmethod
    def fetch_and_sync_order():
        logger.info("🔄 بدء المزامنة بالهيكل الجديد...")
        
        query = """
        query GetOrders {
            findAllOrders {
                data {
                    _id
                    status
                    paymentMethod
                    totalPrice
                    createdAt
                    customer { name phone email }
                    shippingAddress {
                        country { name }
                        city { name }
                        street
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(SyncEngine.API_URL, json={'query': query}, headers=SyncEngine._get_headers(), timeout=120)
            result = response.json()
            
            if 'errors' in result:
                logger.error(f"❌ خطأ GraphQL: {result['errors']}")
                return False
            
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            for item in orders_data:
                # 🎯 1. المعرف هو _id وليس id
                id_api = item.get('_id')
                if not id_api: continue
                    
                order = ProcessedOrder.query.get(id_api) or ProcessedOrder(id=id_api)
                
                # 🎯 2. تحديث الحقول (مع ملاحظة أن status و paymentMethod قد يحتاجان للتعامل كقيم)
                order.order_status = item.get('status')
                order.payment_type = str(item.get('paymentMethod'))
                order.total_price = float(item.get('totalPrice', 0.0))
                
                # بيانات العميل
                cust = item.get('customer') or {}
                order.customer_name = cust.get('name') or "عميل متجر"
                
                # 🎯 3. التعامل مع الكائنات (country و city أصبحا {name: "..."})
                ship = item.get('shippingAddress') or {}
                order.shipping_country = ship.get('country', {}).get('name', 'Yemen')
                order.shipping_city = ship.get('city', {}).get('name', '---')
                order.shipping_street = ship.get('street', '---')
                
                db.session.add(order)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ فشل المزامنة: {e}")
            return False

    # ... (باقي الميثودز الخاصة بالـ Mutation تبقى كما هي)
