# 📂 apps/orders/registry.py
from apps.orders.routes import orders_bp

MODULE_NAME = "الطلبات"
MODULE_ICON = "fa-shopping-cart"

# التعديل هنا: استخدم الاسم الجديد الموحد للبلوبرينت
LINKS = {
    "قائمة الطلبات": "supplier_orders_module_unique.dashboard"
}

def register_module(app):
    try:
        # تأكد أن هذا لا يتعارض مع أي تسجيل آخر
        app.register_blueprint(orders_bp, url_prefix='/orders')
        print("✅ [Registry]: تم تسجيل موديول 'Orders' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'Orders': {e}")
