# apps/add_supplier/__init__.py
# coding: utf-8

from flask import Blueprint

# إنشاء البلوبرينت وتحديد مسار القوالب لضمان وصول جينجا إليها
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    url_prefix='/admin/supplier',
    template_folder='../../templates' # توجيه صريح لمجلد القوالب الرئيسي لمنع الـ TemplateNotFound
)

# الاستيراد المتأخر هنا يمنع الـ Circular Import نهائياً أثناء إقلاع Gunicorn
from apps.add_supplier import routes
