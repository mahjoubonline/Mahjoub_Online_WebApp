from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) السيادي لمجتمع شركاء النجاح
# تم ضبط المسارات لضمان وصول النظام للقوالب والملفات الثابتة بدقة
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    url_prefix='/supplier' # تأمين المسار تحت بادئة المورد
)

# 2. ربط المكونات الحيوية بالبلوبرنت
# نستخدم الاستيراد المتأخر هنا لكسر أي حلقة استيراد دائرية (Circular Import)
# هذا الجزء هو المسؤول عن تفعيل "حارس البرزخ" و "منطق التحقق" و "المسارات"
from . import routes
from . import decorators
from . import auth_logic

# 🛡️ رسالة تشغيل في الـ Terminal للتأكد من التحميل
print("🚀 [System] تم تفعيل نظام الترسانة السيادي (Supplier Panel) بنجاح.")
