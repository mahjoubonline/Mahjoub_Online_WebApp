from flask import Blueprint

# تعريف البلوبرنت الخاص بالموردين
# سنستخدم اسم 'supplier_panel' لكي يتوافق مع استدعاءات url_for
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates' # يخبر Flask بالبحث عن HTML داخل مجلد templates الخاص بالموردين
)

# استيراد المسارات (Routes) في الأسفل لتجنب مشكلة الاستيراد الدائري (Circular Import)
from . import routes
