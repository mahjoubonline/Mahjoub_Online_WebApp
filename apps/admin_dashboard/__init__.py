from flask import Blueprint
import os

# تحديد مسار المجلد الحالي لضمان دقة الوصول للقوالب
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# إنشاء البلوبرينت مع تحديد مجلد القوالب بشكل صريح
# هذا التعديل يضمن أن القوالب ستعمل حتى في بيئة Linux على Railway
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder=template_path
)

# استيراد المسارات (Routes) في نهاية الملف لكسر حلقة الاستيراد الدائري
# ولضمان أن البلوبرينت قد تم تعريفه قبل استخدامه في ملف routes.py
from . import routes
