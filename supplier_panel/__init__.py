from flask import Blueprint

# إضافة template_folder لضمان توجه النظام للمجلد الصحيح
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

from . import routes
