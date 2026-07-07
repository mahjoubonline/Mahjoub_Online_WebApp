# coding: utf-8
# 📂 apps/api/sync_engine.py - نسخة محدثة لتتوافق مع GraphQL Schema

import logging
from decimal import Decimal, InvalidOperation
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.wallet_db import WalletTransaction, SupplierWallet
from apps.models.sync_log import SyncLog 
from apps.models.financials_db import OrderFinancial
from apps.models.order_items_db import OrderItem
from apps.models.supplier_db import Supplier
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

class SyncEngine:
    @staticmethod
    def _log_to_db(order_id, supplier_id, sync_type, status, error=None):
        try:
            log = SyncLog(
                supplier_id=supplier_id,
                order_id=order_id,
                sync_type=sync_type,
                status=status,
                error_message=str(error) if error else None
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            logger.error(f"فشل في تسجيل السجل: {e}")

    @staticmethod
    def run_manual_sync():
        logger.info("بدء المزامنة اليدوية للطلبات...")
        
        # ملاحظة: تم إزالة الترقيم (Pagination) مؤقتاً لأن الـ API يرفض limit/offset
        orders = QomrahGraphQLClient.fetch_orders()
        
        if not orders:
            logger.info("لم يتم جلب أي طلبات.")
            return False
            
        total_synced = 0
        for order_data in orders:
            if SyncEngine.process_financials(order_data):
                total_synced += 1
                
        logger.info(f"انتهت المزامنة بنجاح. إجمالي الطلبات المحدثة: {total_synced}")
        return True

    @staticmethod
    def process_financials(order_data):
        """معالجة مالية مع تصحيح أسماء الحقول بناءً على Schema قمرة"""
        # استخدام الأسماء الجديدة: _id بدلاً من id
        order_id = str(order_data.get('_id'))
        
        # محاولة تحديد المورد
        supplier_id = order_data.get('supplier_id')
        if not supplier_id:
            tracking_tag = order_data.get('tracking_tag')
            supplier = Supplier.query.filter_by(store_tag=tracking_tag).first()
            if supplier:
                supplier_id = supplier.id
            else:
                logger.error(f"❌ تعذر تحديد المورد للطلب {order_id}")
                return False

        # استخدام الأسماء الجديدة: totalPrice بدلاً من total_price
        try:
            total_price = Decimal(str(order_data.get('totalPrice', 0)))
        except (InvalidOperation, ValueError, TypeError):
            total_price = Decimal('0')
            
        product_currency = order_data.get('currency', 'SAR')
        items = order_data.get('items', [])

        try:
            order = Order.query.get(order_id)
            if not order:
                order = Order(
                    id=order_id,
                    order_id_display=f"Q-{order_id[-6:]}",
                    # استخدام الأسماء الجديدة: customerName بدلاً من customer_name
                    customer_name=order_data.get('customerName', 'عميل غير معروف'),
                    supplier_id=supplier_id,
                    total_price=float(total_price),
                    status='pending'
                )
                db.session.add(order)
                db.session.flush()

            OrderItem.query.filter_by(order_id=order_id).delete()
            for item in items:
                # استخدام الأسماء الجديدة: productName بدلاً من title
                new_item = OrderItem(
                    order_id=order_id,
                    title=item.get('productName', 'منتج غير معرف'),
                    qty=item.get('quantity', 1), # كان qty
                    subtotal=Decimal(str(item.get('price', 0))), # كان subtotal
                    sku=item.get('sku', 'N/A')
                )
                db.session.add(new_item)

            # ... (باقي كود المحفظة والمالية يظل كما هو)
            financial_record = OrderFinancial.query.filter_by(order_id=order_id).first()
            if not financial_record:
                financial_record = OrderFinancial(order_id=order_id, supplier_id=supplier_id)
            
            financial_record.total_paid = float(total_price)
            financial_record.mahjoub_commission = float(total_price * Decimal('0.20'))
            financial_record.supplier_cost = float(total_price * Decimal('0.80'))
            
            db.session.add(financial_record)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ خطأ حرج في معالجة الطلب {order_id}: {e}")
            return False
