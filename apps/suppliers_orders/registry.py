# coding: utf-8
from apps.suppliers_orders.routes import suppliers_orders_bp

# إعطاء بيانات وصفية للمصنع ليتمكن من التسجيل دون تكرار
MODULE_CONFIG = {
    "name": "suppliers_orders", # اسم البلوبرينت
    "blueprint": suppliers_orders_bp,
    "url_prefix": "/suppliers_orders",
    "is_admin_module": False # هذا هو المفتاح! لن يظهر في القائمة الجانبية للإدارة
}
