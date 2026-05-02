from flask import Blueprint

# تعريف بوابة الإدارة المركزية
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المنطق من الملفات المستقلة
from . import auth
from . import routes
