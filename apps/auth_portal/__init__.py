# 📂 apps/auth_portal/__init__.py
from flask import Blueprint

# تعريف الـ Blueprint
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

# استيراد المسارات هنا لتسجيلها في الـ Blueprint
from . import routes
