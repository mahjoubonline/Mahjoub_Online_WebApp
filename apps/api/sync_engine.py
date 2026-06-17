# coding: utf-8
# 📂 apps/api/sync_engine.py - محرك المزامنة المتطور (يدعم المنتجات)

import logging
import requests
from config import Config
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder, OrderItem

logger = logging.getLogger(__name__)

class SyncEngine:
    
    @staticmethod
    def sync_order_data(order_data):
        """يقوم بمزامنة الطلب مع قائمة المنتجات التفصيلية"""
        try:
            order_id = str(order_data.get('id', ''))
            if not order_id: return False

            order = ProcessedOrder.query.get(order_id) or ProcessedOrder(id=order_id)
            order.status = order_data.get('status', 'pending')
            
            # تحديث السعر
            total_amount = order_data.get('total', {}).get('amount', 0.0)
            order.total_price = float(total_amount)
            
            db.session.add(order)
            
            # --- معالجة المنتجات (السر في ظهور البيانات) ---
            # حذف المنتجات القديمة للطلب قبل إضافة الجديدة لتجنب التكرار
            OrderItem.query.filter_by(order_id=order_id).delete()
            
            items = order_data.get('items', []) # نفترض أن قمرا ترسل المنتجات هنا
            for item in items:
                new_item = OrderItem(
                    order_id=order_id,
                    product_name=item.get('name', 'منتج غير معروف'),
                    quantity=item.get('quantity', 1),
                    price=float(item.get('price', 0.0))
                )
                db.session.add(new_item)
            
            db.session.commit()
            logger.info(f"🔄 [SyncEngine] تمت مزامنة الطلب {order_id} مع {len(items)} منتجات.")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ [SyncEngine] خطأ أثناء مزامنة المنتجات للطلب {order_id}: {e}")
            return False
