# 📂 apps/wallet/__init__.py
from flask import Blueprint

# تعريف الـ Blueprint للمحفظة
# 'wallet_app' هو الاسم الذي سنستخدمه في تسجيل الـ Blueprint في __init__.py الرئيسي
# __name__ يخبر Flask أن هذا الـ Blueprint يقع في نفس الحزمة (package)
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

# لا تنسى أن تقوم باستيراد المسارات في نهاية هذا الملف لكي يتم تحميلها
from apps.wallet import routes
