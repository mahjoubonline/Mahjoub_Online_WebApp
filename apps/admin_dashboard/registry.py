# 📂 apps/admin_dashboard/registry.py

from .routes import admin_dashboard

MODULE_NAME = "لوحة التحكم"
MODULE_ICON = "fas fa-tachometer-alt"

# التعديل الصحيح:
# المفتاح (Key) هو المسار البرمجي، والقيمة (Value) هي النص العربي
LINKS = {
    "admin_dashboard.dashboard": "الإحصائيات"
}

def register_module(app):
    if admin_dashboard:
        app.register_blueprint(admin_dashboard, url_prefix='/admin')
        print(f"✅ [Registry]: تم تسجيل موديول 'admin_dashboard' بنجاح على المسار (/admin).")
