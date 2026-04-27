from flask import Blueprint

admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

from . import routesfrom flask import Blueprint

# تعريف البوابة السيادية للإدارة
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المسارات لربطها بالبوابة بعد تعريف admin_bp
from . import routes
