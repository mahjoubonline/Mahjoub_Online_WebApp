# coding: utf-8
# 📂 apps/orders/services.py

import requests
from apps.extensions import db  # استخدام المسار الآمن
from apps.models.sync_log import SyncLog
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.supplier_wallet.services import WalletService

class OrderService:
    API_URL = "https://mahjoub.online/admin/graphql"
    
    @staticmethod
    def get_headers(api_key):
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    @staticmethod
    def fetch_and_sync_orders(api_key, supplier_id):
        query = """
        query GetCompletedOrders {
            orders(status: "COMPLETED") {
                id
                netAmount
                currency
                customerName
            }
        }
        """
        try:
            response = requests.post(OrderService.API_URL, json={'query': query}, headers=OrderService.get_headers(api_key))
            if response.status_code != 200:
                raise Exception(f"خطأ API: {response.status_code}")

            data = response.json().get('data', {}).get('orders', [])
            
            for order_data in data:
                # 1. التحقق إذا كان الطلب موجوداً لتجنب التكرار
                if not Order.query.filter_by(id=order_data['id']).first():
                    
                    # 2. إنشاء كائن الطلب
                    new_order = Order(
                        id=order_data['id'],
                        customer_name=order_data.get('customerName', 'عميل'),
                        status='completed'
                    )
                    db.session.add(new_order)
                    
                    # 3. إنشاء السجل المالي (سيتم تشفيره تلقائياً بفضل الـ Properties)
                    new_financial = OrderFinancial(
                        order_id=new_order.id,
                        supplier_id=supplier_id,
                        total_paid=order_data['netAmount'],
                        supplier_cost=0, # سيتم تحديثها لاحقاً
                        mahjoub_commission=order_data['netAmount'],
                        settlement_status='pending'
                    )
                    db.session.add(new_financial)
                
                # 4. تحديث المحفظة
                WalletService.sync_order_payment(
                    supplier_id=supplier_id,
                    order_id=order_data['id'],
                    amount=order_data['netAmount'],
                    currency=order_data['currency']
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
        log = SyncLog(supplier_id=supplier_id, sync_type=sync_type, status=status, error_message=error_message)
        db.session.add(log)
        db.session.commit()
