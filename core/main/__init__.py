from flask import Blueprint

# تعريف البلوبرنت الرئيسي للمنصة
main_bp = Blueprint('main', __name__)

from . import routes  # استيراد المسارات بعد تعريف البلوبرنت
