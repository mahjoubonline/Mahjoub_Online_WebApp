# coding: utf-8
from flask import Blueprint

# 🛡️ تعريف الـ Blueprint الخاص بـ "تعميد الموردين"
# هذا يجعل كل المسارات المعرفة في routes.py تابعة لهذه الحزمة
admin_suppliers_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد الـ routes لربطها بالـ blueprint
from . import routes
