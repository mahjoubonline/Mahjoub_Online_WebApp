from flask import Blueprint

# تعريف البلوبرنت المركزي للإدارة والتحكم
# تم ضبط الاسم 'admin' ليتوافق مع حوكمة المسارات في النواة
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المنطق (Logic) الخاص بالدخول والتحقق
# يتم الاستيراد هنا لضمان ربط الدوال بالبلوبرنت بعد تعريفه
from . import routes
