# coding: utf-8
# 🔑 مستند تهيئة حزمة العمليات المالية والمحافظ - منصة محجوب أونلاين 2026

from flask import Blueprint

# 👑 مصنع ولادة بلوبرينت المحفظة الماليّة وعزل المسار السيادي لإدارة الأرصدة
admin_wallet = Blueprint(
    'admin_wallet', 
    __name__, 
    template_folder='templates',
    url_prefix='/admin/wallet'
)

# 🛡️ استيراد المسارات بعد تعريف البلوبرينت مباشرة لمنع التداخل والتعليق البرمجي
from . import routes
