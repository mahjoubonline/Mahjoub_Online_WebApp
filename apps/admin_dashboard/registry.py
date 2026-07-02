# 📂 apps/admin_dashboard/registry.py

# نستخدم الاستيراد النسبي للوصول إلى البلوبرينت المعرف في routes.py
from .routes import admin_dashboard

def register_module(app):
    """
    تسجيل موديول لوحة تحكم المسؤول (admin_dashboard).
    """
    # التأكد من وجود البلوبرينت قبل تسجيله
    if admin_dashboard:
        app.register_blueprint(admin_dashboard, url_prefix='/admin')
        print(f"✅ [Registry]: تم تسجيل موديول 'admin_dashboard' بنجاح على المسار (/admin).")
    else:
        print(f"❌ [Registry]: فشل تسجيل 'admin_dashboard' - البلوبرينت غير معرف.")
