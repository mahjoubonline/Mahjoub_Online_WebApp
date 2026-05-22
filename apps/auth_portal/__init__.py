# apps/auth_portal/__init__.py
from flask import Blueprint

# هذا الاسم 'auth_blueprint' يجب أن يطابق ما تستورده في auth_portal/routes.py
auth_blueprint = Blueprint('auth_portal', __name__, template_folder='templates')

from . import routes
