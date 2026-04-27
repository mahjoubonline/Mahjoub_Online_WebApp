from flask import Blueprint

# 1. تعريف البلوبرينت (Blueprint) الخاص بلوحة الإدارة
# نحدد اسم البوابة 'admin_panel'
# ونحدد مجلد القوالب 'templates' ليعرف النظام أين يبحث عن ملفات HTML الخاصة بالإدارة
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# 2. استيراد الروابط (Routes) من ملف routes.py التابع لنفس المجلد
# وضعنا الاستيراد في الأسفل لتجنب مشكلة "الاستيراد الدوري" (Circular Import)
# لكي يتمكن ملف routes من استخدام كائن admin_bp الذي عرفناه هنا
from . import routes
