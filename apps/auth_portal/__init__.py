# coding: utf-8
# 🔑 بوابة النفاذ السيادية - منصة محجوب أونلاين 2026
# ملف تهيأة حزمة المصادقة الرقمية والتحكم في الولوج

from flask import Blueprint

# 🛡️ تعريف البلوبرينت مع تحديد المسمى النصي الدقيق 'auth_portal' لتجنب أخطاء الـ BuildError في التوجيه
auth_blueprint = Blueprint(
    'auth_portal', 
    __name__,
    template_folder='templates'
)

# 🔄 استيراد المسارات والمحركات في أسفل الملف بعد تعريف الكائن 
# هذا الإجراء هندسي وإلزامي في فلاسك لمنع حدوث ثغرة التداخل الدائري (Circular Import) أثناء إقلاع السيرفر
from . import routes
