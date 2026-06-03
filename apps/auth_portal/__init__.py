# 📂 apps/auth_portal/__init__.py
from flask import Blueprint

# الاسم الموحد: auth_portal
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

# هذا يكفي، لا داعي لدالة تسجيل معقدة، سنقوم بالتسجيل في الملف الرئيسي
from . import routes
