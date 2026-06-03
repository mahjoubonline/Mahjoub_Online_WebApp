from flask import Blueprint

# هذا المتغير auth_portal هو ما يبحث عنه ملف routes.py
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

from . import routes
