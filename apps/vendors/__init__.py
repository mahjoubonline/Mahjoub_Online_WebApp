from flask import Blueprint

# 1. تعريف "المدير" (Blueprint)
# الاسم (مثلاً 'vendors') يجب أن يكون فريداً لكل تطبيق
# template_folder='templates' يضمن عزل قوالب هذا التطبيق عن غيره
manager = Blueprint('manager_name', __name__, template_folder='templates')

# 2. استيراد المسارات الخاصة بهذا التطبيق فقط
# يتم وضع المسارات في ملف routes.py داخل نفس المجلد
from . import routes
