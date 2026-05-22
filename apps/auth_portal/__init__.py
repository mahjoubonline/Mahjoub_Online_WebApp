# apps/auth_portal/__init__.py
from flask import Blueprint

# يجب أن يكون الاسم 'auth_blueprint' ليطابق ما استوردته في routes.py
auth_blueprint = Blueprint('auth_portal', __name__, template_folder='templates')

from . import routes
