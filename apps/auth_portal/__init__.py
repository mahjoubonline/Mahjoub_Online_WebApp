from flask import Blueprint
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')
from . import routes
