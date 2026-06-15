# 📂 apps/utils/orders_engine.py
from apps.utils.bridge_engine import QumraBridgeEngine
from apps.models.order_db import Order
from apps.extensions import db
import logging

logger = logging.getLogger(__name__)

class OrdersEngine(QumraBridgeEngine):
    
    def fetch_all_orders(self, page=1):
        """
        جلب قائمة الطلبات وربطها بالموردين محلياً إذا لزم الأمر
        """
        query = """
        query {
            findAllOrders {
                orderId
                status
                total
                createdAt
                paymentMethod
                customer {
                    name
                    phone
                }
                items {
                    title
                    qty
                }
                shipping {
                    city
                    street
                }
            }
        }
        """
        result = self.execute_query(query)
        
        if not result or 'data' not in result:
            return []

        raw_orders = result.get('data', {}).get('findAllOrders', [])
        
        processed_orders = []
        for o in raw_orders:
            # البحث عن الطلب في قاعدة البيانات المحلية لجلب الـ supplier_id
            order_record = Order.query.filter_by(order_id_qumra=o.get('orderId')).first()
            
            processed_orders.append({
                "id": order_record.id if order_record else None,
                "order_id_qumra": o.get('orderId'),
                "status": o.get('status'),
                "payment_status": order_record.payment_status if order_record else 'unpaid',
                "total": o.get('total', 0),
                "created_at": o.get('createdAt'),
                "customer_name": o.get('customer', {}).get('name', 'غير معروف'),
                "customer_phone": o.get('customer', {}).get('phone', '-'),
                "shipping_address": f"{o.get('shipping', {}).get('city', '')} - {o.get('shipping', {}).get('street', '')}",
                "payment_method": o.get('paymentMethod', 'غير محدد'),
                "source": "من المتجر", # يمكنك جعلها ديناميكية بناءً على مصدر API
                "supplier": order_record.supplier if order_record and order_record.supplier else None
            })
            
        return processed_orders

    def sync_orders_to_db(self):
        """
        مزامنة الطلبات من قمرة إلى قاعدة البيانات المحلية لربط الموردين
        """
        orders = self.fetch_all_orders()
        for o in orders:
            existing = Order.query.filter_by(order_id_qumra=o['order_id_qumra']).first()
            if not existing:
                new_order = Order(
                    order_id_qumra=o['order_id_qumra'],
                    customer_name=o['customer_name'],
                    total=o['total']
                    # يتم تعيين supplier_id لاحقاً بناءً على مطابقة المنتج
                )
                db.session.add(new_order)
        db.session.commit()
        logger.info("تمت مزامنة الطلبات بنجاح")
