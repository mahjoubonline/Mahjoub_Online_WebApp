# 📂 apps/vendors/__init__.py
from flask import Blueprint

# تعريف الـ Blueprint الخاص بالموردين
# مع تحديد المجلدات الخاصة بالقوالب والملفات الثابتة لضمان الاستقلالية
vendors_bp = Blueprint(
    'vendors', 
    __name__, 
    template_folder='templates', 
    static_folder='static',
    static_url_path='/vendors/static'
)

# استيراد المسارات لربطها بالـ Blueprint
# نضعها في الأسفل لتجنب مشكلة "الاستيراد الدائري" (Circular Import)
from . import routes
