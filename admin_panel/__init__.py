# admin_panel/__init__.py
from flask import Blueprint

# 1. تعريف الـ Blueprint أولاً
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات والتوثيق (بدون try/except معقدة حالياً)
# وضعهما في الأخير هو البروتوكول الصحيح لمنع الـ Circular Import
from . import routes
from . import auth
