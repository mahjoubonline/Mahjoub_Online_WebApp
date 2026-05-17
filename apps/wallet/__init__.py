# coding: utf-8
# 🔑 مستند تهيئة حزمة العمليات المالية والمحافظ - منصة محجوب أونلاين 2026

from flask import Blueprint

# إنشاء البلوبرينت المعزول والمستقل لإدارة الحوكمة المالية والمحافظ
# تم تعيين بادئة المسارات الموحدة لتكون '/admin/wallet' لجميع عمليات الإدارة
admin_wallet = Blueprint(
    'admin_wallet', 
    __name__, 
    template_folder='templates',
    url_prefix='/admin/wallet'
)

# استيراد المسارات (Routes) بعد تعريف البلوبرينت لحمايتها من التداخل والتعليق البرمجي (Circular Imports)
from . import routes
