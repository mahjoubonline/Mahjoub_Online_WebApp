# 📂 apps/admin_exchange/registry.py
from apps.admin_exchange.routes import admin_exchange_bp

MODULE_NAME = "أسعار الصرف"
MODULE_ICON = "fas fa-exchange-alt"

# إضافة الروابط لجعلها تظهر في القائمة الجانبية بشكل صحيح
LINKS = {
    "admin_exchange_bp.index": "إدارة أسعار الصرف"
}

def register_module(app):
    app.register_blueprint(admin_exchange_bp, url_prefix='/admin/exchange')
    print("✅ [Registry]: تم تسجيل موديول 'admin_exchange' بنجاح.")
