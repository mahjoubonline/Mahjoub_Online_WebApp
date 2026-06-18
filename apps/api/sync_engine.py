# coding: utf-8
# 📂 apps/api/sync_engine.py - النسخة السيادية النهائية للمزامنة

import requests
import logging
from apps.models.orders_db import ProcessedOrder, db
from datetime import datetime

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
        logger.info("🔄 بدء المزامنة الشاملة مع قمرة للقيادة المركزية...")
        
        # استعلام موسع لجلب كافة البيانات المطلوبة للجدول والبطاقات
        query = """
        query {
            findAllOrders(input: {}) {
                data {
                    _id
                    totalPrice
                    status
                    financialStatus
                    fulfillmentStatus
                    createdAt
                    customer {
                        name
                        shippingAddress
                    }
                    items {
                        _id
                        quantity
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
                id_api = str(item.get('_id'))
                if not id_api: continue
                    
                # جلب أو إنشاء الطلب
                order = ProcessedOrder.query.filter_by(id=id_api).first() or ProcessedOrder(id=id_api)
                
                # إسناد القيم المباشرة
                order.order_id = id_api[:8]
                order.total_price = float(item.get('totalPrice', 0.0))
                order.order_status = item.get('status', 'pending')
                
                # إسناد بيانات العميل والعنوان
                customer = item.get('customer') or {}
                order.customer_name = customer.get('name', 'عميل غير معروف')
                order.shipping_city = customer.get('shippingAddress', '---')
                
                # حساب عدد العناصر للعمود المطلوب
                items_list = item.get('items') or []
                order.items_count = len(items_list)
                
                # الحالات السيادية
                order.financial_status = item.get('financialStatus', 'unpaid')
                order.fulfillment_status = item.get('fulfillmentStatus', 'unfulfilled')
                order.source = 'QumraCloud'
                
                # معالجة التاريخ
                try:
                    if item.get('createdAt'):
                        order.created_at_local = datetime.fromisoformat(item.get('createdAt').replace('Z', '+00:00'))
                except:
                    pass
                
                db.session.add(order)
            
            db.session.commit()
            logger.info(f"✅ تم بنجاح مزامنة {len(orders_data)} طلب ببياناتها الكاملة.")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ فشل المزامنة الشاملة: {e}")
            return False
