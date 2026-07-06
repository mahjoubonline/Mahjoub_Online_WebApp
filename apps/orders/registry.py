# 📂 apps/orders/registry.py
from apps.orders.routes import orders_bp

MODULE_NAME = "الطلبات"
MODULE_ICON = "fa-shopping-cart"

# هنا يكمن الحل: تأكد أن الـ endpoint يطابق ما يتوقعه النظام
# بما أن النظام يشتكي، سنستخدم 'suppliers_orders.dashboard'
LINKS = {
    "قائمة الطلبات": "suppliers_orders.dashboard"
}

def register_module(app):
    try:
        app.register_blueprint(orders_bp, url_prefix='/orders')
        print("✅ [Registry]: تم تسجيل موديول 'Orders' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'Orders': {e}")
