# coding: utf-8
# 📂 apps/api/__init__.py

"""
مركز خدمات الـ API.
يتم هنا تجميع الـ Blueprints والمحركات الأساسية لتسهيل الاستيراد.
"""

from .webhooks import webhooks_bp
from .sync_engine import SyncEngine

# إنشاء نسخة واحدة (Singleton) ليتم استخدامها في كامل التطبيق
# هذا يضمن توحيد حالة المحرك وسجلات العمليات
engine = SyncEngine()

# تحديد ما يتم تصديره عند استيراد 'from apps.api import *'
__all__ = [
    'webhooks_bp',
    'SyncEngine',
    'engine'
]
