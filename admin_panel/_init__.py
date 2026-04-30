from flask import Blueprint

# تعريف البلوبرنت قبل استيراد المسارات
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')

from . import routes
