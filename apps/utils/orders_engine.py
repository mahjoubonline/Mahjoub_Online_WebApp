# coding: utf-8
# 📂 apps/utils/__init__.py

import os
import logging

# إعداد الـ Logger لتشخيص المسارات
logger = logging.getLogger(__name__)

# سطر كود تشخيصي للتأكد من المسار الذي يقرأه السيرفر فعلياً (سيظهر في الـ Logs)
logger.info(f"DEBUG: Loading bridge_engine from: {os.path.abspath(os.path.dirname(__file__))}")

# استيراد الأدوات
from .security import AESCipher
from .bridge_engine import QumraBridgeEngine
from .orders_engine import OrdersEngine

# تصدير الأدوات لتكون متاحة للمشروع
__all__ = [
    'AESCipher', 
    'QumraBridgeEngine',
    'OrdersEngine'
]
