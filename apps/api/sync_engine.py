# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المحاسبي (النسخة النهائية والمصححة)

import logging
from decimal import Decimal
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.wallet_db import WalletTransaction, SupplierWallet
from apps.models.sync_log import SyncLog 
from apps.models.financials_db import OrderFinancial
from apps.models.order_items_db import OrderItem
from apps.api.tracker_service import TrackerService

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
        """دالة المزامنة اليدوية التي تستدعي معالجة الطلبات"""
        logger.info("بدء المزامنة اليدوية للطلبات...")
        # هنا ستضع الكود الخاص بجلب الطلبات من المصدر (Qumra)
        # عند جلب البيانات، قم بتمرير كل طلب لدالة process_financials
        return True

    @staticmethod
    def process_financials(order_data):
        """معالجة مالية شاملة للطلب"""
        order_id = str(order_data.get('id'))
        supplier_id = order_data.get('supplier_id')
        total_price = Decimal(str(order_data.get('total_price', 0)))
        tracking_tag = order_data.get('tracking_tag')
        product_currency = order_data.get('currency', 'SAR')
        items = order_data.get('items', [])

        try:
            # [تعديل هام] التأكد من وجود سجل في جدول الطلبات أولاً
            order = Order.query.get(order_id)
            if not order:
                order = Order(
                    id=order_id,
                    order_id_display=f"Q-{order_id[-6:]}",
                    customer_name=order_data.get('customer_name', 'عميل'),
                    supplier_id=supplier_id,
                    total_price=float(total_price),
                    status='pending'
                )
                db.session.add(order)
                db.session.flush() # لتوليد الربط

            # 1. التحقق من وجود محفظة للمورد
            wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
            if not wallet:
                raise Exception(f"لا توجد محفظة نشطة للمورد ID: {supplier_id}")

            # 2. تسجيل المنتجات (OrderItem)
            for item in items:
                new_item = OrderItem(
                    order_id=order_id,
                    title=item.get('title'),
                    qty=item.get('qty', 1),
                    subtotal=Decimal(str(item.get('subtotal', 0))),
                    sku=item.get('sku')
                )
                db.session.add(new_item)

            # 3. توزيع الحصص المالية وتشفيرها
            supplier_cost = total_price * Decimal('0.80')
            platform_profit = total_price * Decimal('0.20')
            
            # تسجيل إيراد المورد
            db.session.add(WalletTransaction(
                wallet_id=wallet.id, amount=supplier_cost,
                trans_type='sale_revenue', currency=product_currency,
                description=f"إيراد مبيعات الطلب {order_id}",
                reference_number=order_id
            ))

            # 4. التوثيق في المركز المالي (OrderFinancial)
            financial_record = OrderFinancial(
                order_id=order_id,
                supplier_id=supplier_id,
                currency=product_currency,
                total_paid=float(total_price),
                mahjoub_commission=float(platform_profit),
                supplier_cost=float(supplier_cost),
                settlement_status='pending'
            )
            db.session.add(financial_record)
            
            db.session.commit()
            SyncEngine._log_to_db(order_id, supplier_id, 'financial_sync', 'success')
            return True

        except Exception as e:
            db.session.rollback()
            SyncEngine._log_to_db(order_id, supplier_id, 'financial_sync', 'failed', error=str(e))
            logger.error(f"❌ خطأ حرج في معالجة الطلب {order_id}: {e}")
            return False
