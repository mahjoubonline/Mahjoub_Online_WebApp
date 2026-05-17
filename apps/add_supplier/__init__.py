# apps/add_supplier/__init__.py
# coding: utf-8

from flask import Blueprint

# تعريف البلوبرينت بشكل مستقل دون الإشارة لمجلدات قوالب فرعية وهمية
admin_suppliers = Blueprint(
    'admin_suppliers',
    __name__,
    url_prefix='/admin/suppliers'
)

# الاستدعاء المتأخر في الأسفل لمنع الـ Circular Import تماماً
from apps.add_supplier import routes
