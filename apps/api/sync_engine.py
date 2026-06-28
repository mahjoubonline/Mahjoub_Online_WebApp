# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المدعوم بالتصفح (Pagination) وتسجيل السجلات

import os
import requests
import logging
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.sync_log import SyncLog

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
            # استعلام الـ GraphQL
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
                    error_msg = f"خطأ اتصال في الصفحة {page}: {response.text}"
                    logger.error(f"❌ {error_msg}")
                    SyncEngine._log_sync('orders', 'failed', error_msg)
                    break

                result = response.json()
                data_wrapper = result.get('data', {}).get('findAllOrders', {})
                orders_data = data_wrapper.get('data', [])
                has_more = data_wrapper.get('pagination', {}).get('hasNextPage', False)
                
                for item in orders_data:
                    unique_id = str(item.get('_id'))
                    if not unique_id: continue
                    
                    order = Order.query.filter_by(id=unique_id).first() or Order(id=unique_id)
                    
                    order.order_id_display = str(item.get('orderId', ''))
                    order.total_price = float(item.get('totalPrice') or 0.0)
                    order.created_at = item.get('createdAt')
                    order.status = item.get('status', {}).get('code', 'pending')
                    order.items_count = len(item.get('items', []))
                    
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
                err_str = str(e)
                logger.error(f"❌ خطأ فني أثناء المزامنة في الصفحة {page}: {err_str}")
                SyncEngine._log_sync('orders', 'failed', err_str)
                break
        
        # تسجيل نجاح العملية النهائية
        SyncEngine._log_sync('orders', 'success', f"تم مزامنة {total_synced} طلب بنجاح.")
        logger.info(f"🏁 انتهت عملية المزامنة. إجمالي الطلبات المحدثة: {total_synced}")
        return True

    @staticmethod
    def _log_sync(sync_type, status, message):
        """دالة مساعدة لتسجيل الأحداث في SyncLog"""
        try:
            log = SyncLog(sync_type=sync_type, status=status, error_message=message)
            db.session.add(log)
            db.session.commit()
        except:
            db.session.rollback()
