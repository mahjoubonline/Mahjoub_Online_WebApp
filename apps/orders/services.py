# coding: utf-8
# 📂 apps/orders/services.py

import requests
from apps.extensions import db
from apps.models.sync_log import SyncLog
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.supplier_wallet.services import WalletService

class OrderService:
    API_URL = "https://mahjoub.online/admin/graphql"
    
    @staticmethod
    def get_headers(api_key):
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def fetch_and_sync_orders(api_key, supplier_id):
        query = """
        query GetCompletedOrders {
            orders(status: "COMPLETED") {
                orderId
                customerName
                status
                total
                currency
            }
        }
        """
        try:
            response = requests.post(
                OrderService.API_URL, 
                json={'query': query}, 
                headers=OrderService.get_headers(api_key)
            )
            
            if response.status_code != 200:
                raise Exception(f"خطأ في الاتصال: {response.status_code}")

            data = response.json().get('data', {}).get('orders', [])
            
            for item in data:
                # استخدام .get() مع مفاتيح المتجر لتجنب أخطاء عدم وجود الحقل
                order_id = item.get('orderId')
                if not order_id: continue # تخطي الطلب إذا لم يحتوي على معرف
                
                # التحقق من عدم التكرار
                if not Order.query.filter_by(id=str(order_id)).first():
                    
                    # 1. إنشاء الطلب
                    new_order = Order(
                        id=str(order_id),
                        customer_name=item.get('customerName', 'عميل'),
                        status=item.get('status', 'completed')
                    )
                    db.session.add(new_order)
                    
                    # 2. إنشاء السجل المالي
                    new_financial = OrderFinancial(
                        order_id=str(order_id),
                        supplier_id=supplier_id,
                        total_paid=float(item.get('total', 0)),
                        supplier_cost=0, 
                        mahjoub_commission=float(item.get('total', 0)),
                        settlement_status='pending'
                    )
                    db.session.add(new_financial)
                
                # 3. تحديث المحفظة
                WalletService.sync_order_payment(
                    supplier_id=supplier_id,
                    order_id=str(order_id),
                    amount=float(item.get('total', 0)),
                    currency=item.get('currency', 'SAR')
                )
            
            db.session.commit()
            OrderService.log_sync(supplier_id, 'orders', 'SUCCESS', "تمت المزامنة بنجاح")
            return True

        except Exception as e:
            db.session.rollback()
            OrderService.log_sync(supplier_id, 'orders', 'FAILED', str(e))
            return False

    @staticmethod
    def log_sync(supplier_id, sync_type, status, error_message=None):
        log = SyncLog(
            supplier_id=supplier_id,
            sync_type=sync_type,
            status=status,
            error_message=str(error_message)
        )
        db.session.add(log)
        db.session.commit()
