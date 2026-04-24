from flask import Blueprint

# هذا السطر هو مفتاح الحل
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

from . import routes
