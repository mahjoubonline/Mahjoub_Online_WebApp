# apps/add_supplier/__init__.py
# coding: utf-8
import os
from flask import Blueprint

# 1. تحديد المسار المطلق لضمان عمل المجلدات في البيئات السحابية والمحلية بمرونة
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
static_path = os.path.join(current_dir, 'static')

# 2. تعريف البلوبرينت السيادي للموردين مع المسارات الدقيقة المطلقة
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder=template_path,  # المسار المطلق للملفات التفاعلية (Templates)
    static_folder=static_path       # المسار المطلق للملفات الثابتة (Static)
)

# 3. ربط المسارات (Routes) بعد تعريف البلوبرينت مباشرة لضمان حقن الدوال بداخل السجل
from apps.add_supplier import routes
