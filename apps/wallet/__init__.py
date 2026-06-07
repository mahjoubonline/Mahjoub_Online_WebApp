# 📂 apps/wallet/__init__.py
from flask import Blueprint

# تعريف الـ Blueprint فقط
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# ملاحظة هامة جداً: لا تقم باستيراد routes هنا! 
# تسجيل المسارات سيتم عبر الـ Blueprint الذي قمت بتسجيله في apps/__init__.py الرئيسي.
