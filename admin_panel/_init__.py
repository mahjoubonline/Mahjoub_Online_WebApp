from flask import Blueprint

# قمنا بتغيير اسم الكائن إلى admin_blueprint لتمييزه عن اسم المجلد
# وتحديد مسار القوالب ليكون المجلد templates داخل admin_panel
admin_blueprint = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# استيراد المسارات لربطها بالبلوبرنت
from . import routes
