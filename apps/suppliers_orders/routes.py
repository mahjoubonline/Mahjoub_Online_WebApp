# coding: utf-8
# 📂 apps/suppliers_orders/registry.py

from apps.suppliers_orders.routes import suppliers_orders_bp

# 1. إعدادات التعريف (المتوافقة مع النظام الجديد)
MODULE_NAME = "طلبات الزبائن"
MODULE_ICON = "fas fa-shopping-cart"
SHOW_IN_SUPPLIER = True  # ليظهر في قائمة المورد

# 2. تعريف الروابط (نظام القاموس الجديد)
LINKS = {
    "قائمة الطلبات": "suppliers_orders_portal.dashboard"
}

def register_module(app):
    """
    تسجيل الموديول برمجياً وتفعيله ليظهر في النظام.
    """
    try:
        # تسجيل الـ Blueprint
        app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers/orders')
        print("✅ [Registry]: تم تسجيل موديول 'طلبات الزبائن' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'suppliers_orders': {e}")
