from flask import Blueprint

# تعريف البلوبرينت باسم مستقل
add_supplier_bp = Blueprint(
    'admin_suppliers', # الاسم البرمجي للاستدعاء
    __name__,
    template_folder='templates'
)

from . import routes
