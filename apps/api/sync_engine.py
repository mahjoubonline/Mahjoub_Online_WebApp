# coding: utf-8
# 📂 apps/api/sync_engine.py - النسخة السيادية النهائية للمزامنة (مصححة)

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
        logger.info("🔄 بدء المزامنة الشاملة مع قمرة...")
        
        # استعلام GraphQL مخفف لضمان نجاح الاتصال أولاً
        query = """
        query {
            findAllOrders(input: {}) {
                data {
                    _id
                    totalPrice
                    status {
                        code
                    }
                    createdAt
                    items {
                        _id
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(SyncEngine.API_URL, json={'query': query}, headers=SyncEngine._get_headers(), timeout=120)
            result = response.json()
            
            if 'errors' in result:
                logger.error(f"❌ خطأ GraphQL تفصيلي: {result['errors']}")
                return False
            
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            for item in orders_data:
                id_api = str(item.get('_id'))
                if not id_api: continue
                    
                order = ProcessedOrder.query.filter_by(id=id_api).first() or ProcessedOrder(id=id_api)
                
                # إسناد القيم الأساسية
                order.order_id = id_api[:8]
                order.total_price = float(item.get('totalPrice') or 0.0)
                
                # معالجة الحالة
                status_obj = item.get('status') or {}
                order.order_status = status_obj.get('code', 'pending')
                
                # قيم افتراضية للحقول التي كانت تسبب خطأ
                order.customer_name = "عميل"
                order.financial_status = "unpaid"
                order.fulfillment_status = "unfulfilled"
                order.items_count = len(item.get('items') or [])
                order.source = 'QumraCloud'
                
                # معالجة التاريخ
                if item.get('createdAt'):
                    try:
                        order.created_at_local = datetime.fromisoformat(item.get('createdAt').replace('Z', '+00:00'))
                    except:
                        pass
                
                db.session.add(order)
            
            db.session.commit()
            logger.info(f"✅ تمت المزامنة بنجاح لـ {len(orders_data)} طلب.")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ فشل المزامنة بسبب استثناء: {e}")
            return False
