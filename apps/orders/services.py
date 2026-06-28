# coding: utf-8
# 📂 apps/models/orders_db.py

from datetime import datetime
from cryptography.fernet import Fernet
from apps.extensions import db
import os

# تهيئة مفتاح التشفير (يجب أن يكون مخزناً في متغيرات البيئة)
cipher = Fernet(os.getenv('ENCRYPTION_KEY', Fernet.generate_key()))

class Order(db.Model):
    __tablename__ = 'orders'

    # [صمام الأمان]: فهرسة الحقول غير المشفرة لضمان سرعة الاستعلامات والربط
    # الفهارس لا تعمل على الحقول المشفرة، لذا نركز على أعمدة البحث والربط
    __table_args__ = (
        db.Index('idx_ord_supplier_id', 'supplier_id'),
        db.Index('idx_ord_ref', 'order_reference'),
        db.Index('idx_ord_status', 'status'),
        db.Index('idx_ord_created', 'created_at'),
        {'extend_
