from flask import Blueprint

# تعريف الـ Blueprint الخاص بالإدارة مع تحديد مجلدات القوالب والملفات الثابتة
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد ملفات المنطق لربطها بالـ Blueprint
# تأكد من استدعاء auth لكي تعمل صفحة تسجيل الدخول (علي محجوب / 123)
from . import auth
from . import routes
