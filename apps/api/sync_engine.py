# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المستقر والمطابق الفعلي لسيرفر قمرة (النسخة النهائية الشاملة)

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
            logger.info(f"🔄 جاري جلب ومزامنة الصفحة: {page} بالحقول المحدثة الرسمية من قمرة")
            
            # تحديث الـ Query لطلب الحقول والأعمدة الصريحة التي كشفها فريق قمرة
            query = """
            query($page: Int) {
                findAllOrders(input: {page: $page, limit: 10}) {
                    data {
                        _id
                        orderId
                        orderStatus
                        financialStatus
                        fulfillmentStatus
                        totalPrice
                        customerName
                        customerPhone
                        paymentType
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
                
                result = response.json()
                
                # التحقق الصارم من وجود الأخطاء في الجذر (Root) لمنع انهيار المعالجة
                if 'errors' in result:
                    logger.error(f"❌ خطأ تدوين من سيرفر قمرة: {result['errors']}")
                    return False
                
                if 'data' in result and result['data'].get('findAllOrders'):
                    data_wrapper = result['data']['findAllOrders']
                    orders_data = data_wrapper.get('data', [])
                    
                    for item in orders_data:
                        # جلب المعرف الفريد للتخزين المحلي
                        id_api = str(item.get('_id'))
                        
                        # البحث عن الطلب محلياً أو إنشاء كائن جديد بالكامل
                        order = ProcessedOrder.query.get(id_api) or ProcessedOrder(id=id_api)
                        
                        # 1. ربط حقول الهوية والرقم التسلسلي الظاهري
                        order.order_id = item.get('orderId')
                        
                        # 2. حقن الحالات الثلاث المستقلة القادمة من قمرة مباشرة
                        order.order_status = item.get('orderStatus', 'pending')
                        order.financial_status = item.get('financialStatus', 'unpaid')
                        order.fulfillment_status = item.get('fulfillmentStatus', 'unfulfilled')
                        
                        # 3. مزامنة بيانات العميل الحقيقية المستخرجة
                        order.customer_name = item.get('customerName') or "عميل متجر محجوب"
                        order.customer_phone = item.get('customerPhone')
                        
                        # 4. وسيلة الدفع والقيمة المالية (المشفرة آلياً بالـ Setter)
                        order.payment_type = item.get('paymentType', 'manual')
                        order.total_price = float(item.get('totalPrice', 0))
                        
                        # 5. معالجة التاريخ والوقت النصي القادم من قمرة وتحويله لكائن datetime
                        created_at_str = item.get('createdAt')
                        if created_at_str:
                            try:
                                # إزالة حرف Z والكسور لتسهيل التحويل البرمجي المستقر
                                clean_date = created_at_str.split('.')[0].replace('Type', '').replace('Z', '')
                                order.created_at_api = datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S")
                            except Exception as date_err:
                                logger.warning(f"⚠️ فشل تحليل صيغة الوقت للطلب {id_api}: {date_err}")
                                order.created_at_api = datetime.utcnow()
                        
                        # حقول الحساب والإحصائيات التكميلية
                        order.source = 'QumraCloud'
                        order.items_count = 1  # قيمة افتراضية لحين مزامنة الـ items بشكل منفصل
                        
                        db.session.add(order)
                    
                    db.session.commit()
                    has_next_page = data_wrapper.get('pagination', {}).get('hasNextPage', False)
                    page += 1
                else:
                    logger.error(f"❌ فشل مطابقة البنية أو استجابة فارغة: {result}")
                    return False
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"❌ خطأ برمجي أثناء المعالجة أو الربط: {str(e)}")
                return False
        return True

    @staticmethod
    def _execute_mutation(mutation, variables):
        try:
            response = requests.post(
                SyncEngine.API_URL, 
                json={'query': mutation, 'variables': variables}, 
                headers=SyncEngine._get_headers(),
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"❌ خطأ أثناء تنفيذ الـ Mutation: {e}")
            return None

    @staticmethod
    def cancel_order(order_id):
        """إرسال أمر إلغاء الطلب عبر المعرف الفريد"""
        mutation = """
        mutation($id: ID!) { 
            cancelOrder(id: $id) { 
                _id 
                orderStatus
            } 
        }
        """
        return SyncEngine._execute_mutation(mutation, {"id": order_id})

    @staticmethod
    def mark_as_fulfilled(order_id):
        """تحديث الطلب كـ مشحون ومجهز برمجياً"""
        mutation = """
        mutation($id: ID!) { 
            markOrderFulfilled(id: $id) { 
                _id 
                fulfillmentStatus
            } 
        }
        """
        return SyncEngine._execute_mutation(mutation, {"id": order_id})

    @staticmethod
    def update_order_status(order_id, new_status):
        """تحديث مخصص لحالة الطلب بناءً على الحالات المعتمدة"""
        mutation = """
        mutation($id: ID!, $status: String!) { 
            updateOrderStatus(id: $id, status: $status) { 
                _id 
                orderStatus
            } 
        }
        """
        return SyncEngine._execute_mutation(mutation, {"id": order_id, "status": new_status})
