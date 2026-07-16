# 📂 apps/orders/registry.py
from apps.orders.routes import orders_bp

MODULE_NAME = "الطلبات"
MODULE_ICON = "fas fa-shopping-cart"

# التصحيح: يجب أن يبدأ المفتاح باسم الـ Blueprint (orders) وليس باسم المتغير (orders_bp)
LINKS = {
    "orders.dashboard": "قائمة الطلبات" 
}

def register_module(app):
    try:
        app.register_blueprint(orders_bp, url_prefix='/orders')
        print("✅ [Registry]: تم تسجيل موديول 'Orders' بنجاح تحت المسار /orders.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'Orders': {e}")
