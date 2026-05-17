# coding: utf-8
# 🔑 بوابة النفاذ السيادية - منصة محجوب أونلاين 2026

from flask import Blueprint
import os

# 1. تحديد مسار المجلد الحالي لضمان دقة الوصول للقوالب في Railway (Linux)
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء البلوبرينت الموحد والمطابق بنسبة 100% للنواة والمسارات السيادية
auth_blueprint = Blueprint(
    'auth_portal',  # تم تعديل الاسم الداخلي هنا ليتطابق مع الاستدعاءات والـ url_for
    __name__, 
    template_folder=template_path
)

# 3. كسر حلقة الاستيراد الدائري واستدعاء المسارات بشكل آمن
from . import routes
