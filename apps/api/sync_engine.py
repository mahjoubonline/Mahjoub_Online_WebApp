# coding: utf-8
import requests
import logging
from datetime import datetime
from apps.models.orders_db import ProcessedOrder, db

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
        page = 1
        has_next_page = True
        
        while has_next_page:
            logger.info(f"🔄 جاري جلب الصفحة: {page}")
            
            # الاستعلام المحدث ليتطابق مع توثيق قمرة
            query = """
            query($page: Int) {
                findAllOrders(input: {page: $page, limit: 10}) {
                    data {
                        _id
                        status
                        totalPrice
                        createdAt
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
                    timeout=30
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ خطأ اتصال {response.status_code}: {response.text}")
                    return False

                result = response.json()
                # استخدام المسار الصحيح الموضح في التوثيق
                data_wrapper = result.get('data', {}).get('findAllOrders', {})
                orders_data = data_wrapper.get('data', [])
                pagination = data_wrapper.get('pagination', {})
                
                has_next_page = pagination.get('hasNextPage', False)

                for item in orders_data:
                    order_id = str(item.get('_id'))
                    order = ProcessedOrder.query.get(order_id) or ProcessedOrder(id=order_id)
                    order.status = item.get('status')
                    order.total_price = float(item.get('totalPrice', 0))
                    db.session.add(order)
                
                db.session.commit()
                page += 1
            except Exception as e:
                logger.error(f"❌ خطأ برمجي: {str(e)}")
                return False
        return True
