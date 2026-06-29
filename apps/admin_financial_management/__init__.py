# coding: utf-8
# 📂 apps/admin_financial_management/__init__.py

"""
حزمة إدارة الطلبات المالية
تحتوي على:
- routes.py: منطق المعالجة والتحكم.
- registry.py: تسجيل الموديول تلقائياً.
- templates/: واجهات المستخدم الخاصة بالمالية.
"""

# استيراد الـ Blueprint لتسهيل الوصول إليه عند الحاجة
from .routes import admin_financial_bp

# لا تضع منطقاً معقداً هنا، اترك هذا الملف بسيطاً للحفاظ على هيكلية الموديول
