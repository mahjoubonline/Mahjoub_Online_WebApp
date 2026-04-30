from flask import Blueprint

# تعريف البلوبرنت بوضوح
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')

# استيراد المسارات لربطها بالبلوبرنت
from . import routes

# هذا السطر يضمن تصدير الكائن بشكل صحيح للسيرفر
__all__ = ['admin_panel']
