# apps/vendors/__init__.py
from flask import Blueprint

# تعريف الـ Blueprint الخاص بالموردين
# name: 'vendors' (اسم الـ Blueprint)
# import_name: __name__ (يخبر Flask بموقع هذا التطبيق)
# template_folder: 'templates' (المكان الذي سيجلب منه ملفات الـ HTML)
vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

# استيراد المسارات لربطها بالـ Blueprint
# نضعها في الأسفل لتجنب مشكلة "الاستيراد الدائري" (Circular Import)
from . import routes
