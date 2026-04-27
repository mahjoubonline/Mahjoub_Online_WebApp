from flask import Blueprint

admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المسارات لربطها بالبلوبرنت
from . import routes
