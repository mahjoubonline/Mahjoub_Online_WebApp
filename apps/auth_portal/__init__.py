# coding: utf-8
# 📂 apps/auth_portal/__init__.py

from flask import Blueprint

# تعريف الـ Blueprint مع تحديد مسار القوالب بدقة
auth_portal = Blueprint(
    'auth_portal', 
    __name__, 
    template_folder='templates',  # Flask سيبحث داخل apps/auth_portal/templates/
    static_folder='static'        # Flask سيبحث داخل apps/auth_portal/static/
)

# استيراد المسارات بعد تعريف الـ Blueprint لتجنب مشاكل الاستيراد الدائري
from . import routes
