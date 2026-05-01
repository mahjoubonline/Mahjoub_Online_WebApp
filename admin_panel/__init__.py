from flask import Blueprint

# تعريف البلوبرنت المركزي للإدارة
# ملاحظة: تم تثبيت الاسم 'admin' ليتوافق مع روابط url_for('admin.login') في القوالب
admin_blueprint = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'  # أضفنا هذا تحسباً لإضافة ملفات CSS/JS خاصة لاحقاً
)

# استيراد المسارات (routes) لربطها بالبلوبرنت وتفعيلها
# نضعه في الأسفل لتجنب مشاكل الاستيراد الدائري (Circular Import)
from . import routes
