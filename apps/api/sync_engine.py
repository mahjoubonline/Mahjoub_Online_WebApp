# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المدعوم بالتصفح (Pagination)

import os
import requests
import logging
from apps.extensions import db
from apps.models.orders_db import Order

logger = logging.getLogger(__name__)

class SyncEngine:
    API_URL = "https://mahjoub.online/admin/graphql"  

    @staticmethod
    def _get_headers():
        api_key = os.environ.get("QUMRA_API_KEY", "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def fetch_and_sync_order():
        logger.info("🔄 بدء عملية المزامنة الشاملة (جميع الصفحات)...")
        
        page = 1
        total_synced = 0
        has_more = True
        
        while has_more:
            # استعلام يدعم التصفح (Pagination) - تأكد أن الـ API الخاص بك يدعم page و limit
            query = """
            query($page: Int!) {
                findAllOrders(page: $page, limit: 50) {
                    data {
                        _id
                        orderId
                        totalPrice
                        createdAt
                        status { code }
                        account { firstName lastName }
                        items { _id }
                    }
                    pagination {
                        hasNextPage
                    }
                }
            }
            """
            
            try:
                response = requests.post(
                    SyncEngine.API_URL, 
                    json={'query': query, 'variables': {'page': page}}, 
                    headers=SyncEngine._get_headers(), 
                    timeout=60
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ خطأ اتصال في الصفحة {page}: {response.text}")
                    break

                result = response.json()
                data_wrapper = result.get('data', {}).get('findAllOrders', {})
                orders_data = data_wrapper.get('data', [])
                has_more = data_wrapper.get('pagination', {}).get('hasNextPage', False)
                
                for item in orders_data:
                    unique_id = str(item.get('_id'))
                    if not unique_id: continue
                    
                    order = Order.query.filter_by(id=unique_id).first() or Order(id=unique_id)
                    
                    # استخدام الحقول الصحيحة التي ذكرتها
                    order.order_id_display = str(item.get('orderId', ''))
                    order.total_price = float(item.get('totalPrice') or 0.0)
                    order.created_at = item.get('createdAt')
                    order.order_status = item.get('status', {}).get('code', 'pending')
                    order.items_count = len(item.get('items', []))
                    
                    # دمج الاسم بشكل صحيح
                    acc = item.get('account') or {}
                    order.customer_name = f"{acc.get('firstName', '')} {acc.get('lastName', '')}".strip() or "عميل"
                    
                    db.session.add(order)
                    total_synced += 1
                
                db.session.commit()
                logger.info(f"✅ تمت مزامنة الصفحة {page} بنجاح.")
                
                if has_more:
                    page += 1
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"❌ خطأ فني أثناء المزامنة في الصفحة {page}: {str(e)}")
                break
        
        logger.info(f"🏁 انتهت عملية المزامنة. إجمالي الطلبات المحدثة: {total_synced}")
        return True
