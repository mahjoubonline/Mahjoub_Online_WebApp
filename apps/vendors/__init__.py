from flask import Blueprint

# هذا هو "المدير" المسؤول عن قسم الموردين
vendors_manager = Blueprint('vendors', __name__, template_folder='templates')

# استدعاء المسارات (التي تحتوي على logic الموردين)
from . import routes
