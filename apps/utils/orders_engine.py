# 📂 apps/utils/orders_engine.py
import hashlib
import json
from apps.utils.bridge_engine import QumraBridgeEngine
from apps.extensions import db
from apps.models.order_db import Order
import logging

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        self.bridge = QumraBridgeEngine()

    def generate_fingerprint(self, item):
        """توليد معرف فريد بناءً على بيانات الطلب لتجنب التكرار"""
        # نأخذ الحقول الثابتة للطلب ونحولها لنص ثم نشفرها
        content = f"{item.get('account', {}).get('name')}-{item.get('totalPrice')}-{item.get('createdAt')}"
        return hashlib.md5(content.encode()).hexdigest()

    def sync_orders_to_db(self):
        orders = self.bridge.fetch_latest_orders()
        if not orders: return 0

        count = 0
        for item in orders:
            # 1. إنشاء معرف فريد (سواء من قمرة أو توليدنا الخاص)
            qumra_id = str(item.get('_id') or self.generate_fingerprint(item))
            
            # 2. البحث عن الطلب (Upsert Logic)
            order = Order.query.filter_by(order_id_qumra=qumra_id).first()
            if not order:
                order = Order(order_id_qumra=qumra_id)
                db.session.add(order)
            
            # 3. حفظ البيانات تلقائياً
            order.raw_data = item
            order.total = float(item.get('totalPrice', 0))
            order.status = item.get('status', {}).get('name', 'pending')
            order.customer_name = item.get('account', {}).get('name', 'غير معروف')
            
            count += 1
            
        db.session.commit()
        return count
