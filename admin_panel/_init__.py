from flask import Blueprint

# تعريف البوابة مع تحديد مجلد القوالب الخاص بها
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates', # سيبحث داخل admin_panel/templates
    static_folder='static'
)

# استيراد المسارات لربطها بالبلوبرنت
from . import routes
