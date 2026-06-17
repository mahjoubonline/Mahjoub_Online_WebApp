# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة النهائي (المتوافق مع بنية GraphQL لسيرفر قمرة المحدثة)

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
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def fetch_and_sync_order():
        page = 1
        has_next_page = True
        
        while has_next_page:
            logger.info(f"🔄 جاري جلب الصفحة: {page} بالحقول المعتمدة من السيرفر")
            
            # تم تنظيف الاستعلام من الحقول غير المدعومة وتصحيح الكائنات بناءً على الـ Validation المرتجع من قمرة
            query = """
            query($page: Int) {
                findAllOrders(input: {page: $page, limit: 10}) {
                    data {
                        _id
                        status {
                            _id
                            title
                        }
                        totalPrice
                        createdAt
                        paymentMethod {
                            title
                        }
                        account {
                            username
                        }
                        shippingAddress {
                            address
                        }
                        items {
                            quantity
                        }
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
                
                result = response.json()
                logger.info(f"🔄 استجابة السيرفر لطلب المزامنة: {result}")
                
                if 'data' in result and result['data'].get('findAllOrders'):
                    data_wrapper = result['data']['findAllOrders']
                    orders_data = data_wrapper.get('data', [])
                    
                    for item in orders_data:
                        order_id = str(item.get('_id'))
                        order = ProcessedOrder.query.get(order_id) or ProcessedOrder(id=order_id)
                        
                        # 1. حالة الطلب الرئيسية
                        status_obj = item.get('status', {})
                        if isinstance(status_obj, dict):
                            order.status = status_obj.get('title') or status_obj.get('_id') or 'قيد الانتظار'
                        else:
                            order.status = 'قيد الانتظار'
                        
                        # 2. استخراج اسم العميل من كائن الحساب account (البديل المعتمد لـ customer)
                        account_obj = item.get('account') or {}
                        order.customer_name = account_obj.get('username', '---')
                        
                        # 3. استخراج تفاصيل عنوان الشحن (استخدام حقل address المعتمد)
                        address_obj = item.get('shippingAddress') or {}
                        order.shipping_address = address_obj.get('address', '---')
                        
                        # 4. الحقول المالية وحساب الحالات ذكياً لتغذية لوحة التحكم بدون أخطاء
                        order.total_price = float(item.get('totalPrice', 0))
                        
                        pay_method_obj = item.get('paymentMethod') or {}
                        order.payment_method = pay_method_obj.get('title', '---')
                        
                        # استنباط الحالات مالياً وبناءً على حالة الطلب العامة
                        order.payment_status = 'مدفوع' if order.status in ['مكتمل', 'نجاح', 'settled'] else 'غير مدفوع'
                        order.shipping_status = 'تم التوصيل' if order.status in ['مكتمل'] else 'غير مجهز'
                        
                        # 5. حساب عدد المنتجات الإجمالي ديناميكياً من مصفوفة العناصر (بديل itemsCount)
                        items_list = item.get('items', [])
                        total_items = 0
                        if isinstance(items_list, list):
                            for i in items_list:
                                total_items += int(i.get('quantity', 1))
                        order.items_count = total_items if total_items > 0 else 1
                        
                        db.session.add(order)
                    
                    db.session.commit()
                    has_next_page = data_wrapper.get('pagination', {}).get('hasNextPage', False)
                    page += 1
                else:
                    logger.error(f"❌ فشل مطابقة البيانات المستلمة: {result}")
                    return False
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"❌ خطأ برمجي أثناء المعالجة: {str(e)}")
                return False
        return True

    @staticmethod
    def _execute_mutation(mutation, variables):
        try:
            response = requests.post(SyncEngine.API_URL, json={'query': mutation, 'variables': variables}, headers=SyncEngine._get_headers())
            return response.json() if response.status_code == 200 else None
        except: return None

    @staticmethod
    def cancel_order(order_id):
        return SyncEngine._execute_mutation("mutation($id: ID!) { cancelOrder(id: $id) { _id } }", {"id": order_id})

    @staticmethod
    def mark_as_fulfilled(order_id):
        return SyncEngine._execute_mutation("mutation($id: ID!) { markOrderFulfilled(id: $id) { _id } }", {"id": order_id})

    @staticmethod
    def update_order_status(order_id, new_status):
        return SyncEngine._execute_mutation("mutation($id: ID!, $status: String!) { updateOrderStatus(id: $id, status: $status) { _id } }", {"id": order_id, "status": new_status})
