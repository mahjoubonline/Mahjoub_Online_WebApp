# 📂 apps/wallet/__init__.py

from flask import Blueprint

# تعريف الـ Blueprint الخاص بمحفظة الموردين
# تأكد أن اسم الـ Blueprint (wallet_app) هو نفس الاسم المستخدم في routes.py
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# استيراد الـ routes لتسجيل المسارات في الـ Blueprint
from apps.wallet import routes
