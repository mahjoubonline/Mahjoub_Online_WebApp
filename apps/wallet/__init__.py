# coding: utf-8
from flask import Blueprint

# تعريف البلوبرينت مع تحديد مجلد القوالب (templates)
# هذا التحديد يضمن أن Flask سيبحث عن ملفات HTML داخل المجلد الفرعي
wallet_blueprint = Blueprint(
    'wallet', 
    __name__, 
    template_folder='templates'
)

# ملاحظة: لا تستورد routes هنا لمنع الـ Circular Import.
# يتم استيراد الـ routes وتسجيل البلوبرينت في ملف apps/__init__.py الرئيسي.
