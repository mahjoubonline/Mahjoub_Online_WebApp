# 📂 apps/orders/registry.py
from apps.orders.routes import orders_bp

MODULE_NAME = "الطلبات"
MODULE_ICON = "fas fa-shopping-cart" # أضفت 'fas' لضمان عمل الأيقونة

# التصحيح: الـ Key هو المسار البرمجي، والـ Value هو النص الظاهر للمستخدم
LINKS = {
    "orders_bp.dashboard": "قائمة الطلبات" 
}

def register_module(app):
    try:
        app.register_blueprint(orders_bp, url_prefix='/orders')
        print("✅ [Registry]: تم تسجيل موديول 'Orders' بنجاح تحت المسار /orders.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'Orders': {e}")
