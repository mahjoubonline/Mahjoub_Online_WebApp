from flask import Blueprint

# إعداد الـ Blueprint لبرج الرقابة
# نحدد اسم الـ Blueprint ومسار القوالب (Templates) التابعة له
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static' # إذا أردت إضافة ملفات CSS/JS خاصة بالإدارة لاحقاً
)

# هامة جداً: استيراد المسارات بعد تعريف الـ Blueprint لتجنب التعارض (Circular Import)
from . import routes
