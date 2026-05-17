# apps/auth_portal/__init__.py
# coding: utf-8
from flask import Blueprint
import os

# 1. تحديد مسار المجلد الحالي لضمان دقة الوصول للقوالب في Railway (Linux)
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء البلوبرينت الخاص ببوابة الدخول (Authentication Portal)
# تعديل الاسم إلى auth_blueprint ليتطابق 100% مع المصنع المركزي في النواة
auth_blueprint = Blueprint(
    'auth', 
    __name__, 
    template_folder=template_path
)

# 3. كسر حلقة الاستيراد الدائري (Circular Import Fix)
from . import routes
