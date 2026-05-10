# admin_panel/__init__.py
from flask import Blueprint

# 1. إعلان الهوية السيادية لمنطقة الإدارة (The Admin Core)
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/admin' 
)

# 2. بروتوكول الربط السيادي (Sovereign Linkage)
# يتم الاستيراد بهذا الترتيب لضمان استقرار "بوابة الولوج" أولاً
from . import auth                 # محرك الحماية والولوج (Security First)
from . import routes               # محرك Dashboard والإحصائيات العامة
from . import add_supplier_routes   # محرك نافذة الموردين (نافذة مستقلة)

# مستقبلاً: أي نافذة جديدة (مناديب، مخازن، منتجات) تضاف هنا بسطر واحد
# من أجل الحفاظ على مبدأ "النوافذ المستقلة" الذي تتبعه.
# from . import manage_warehouse

"""
رسالة تأكيد للمؤسس علي محجوب:
بهذا الترتيب، نضمن أن النظام يفتح 'auth' أولاً ليتعرف على مسار login، 
ثم يفتح 'routes' ليعرف الـ dashboard، وأخيراً 'add_supplier_routes' 
لتعميد الموردين. الآن الترسانة متصلة ببعضها ككتلة واحدة صلبة.
"""
