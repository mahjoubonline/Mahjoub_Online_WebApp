# apps/vendors/__init__.py
from flask import Blueprint

# هذا هو "مدير القسم"
vendors_manager = Blueprint('vendors_manager', __name__, url_prefix='/vendors')

# هنا يتم تجميع كل موديلات وقوالب ومسارات المورد داخل هذا القسم فقط
from . import routes, models
