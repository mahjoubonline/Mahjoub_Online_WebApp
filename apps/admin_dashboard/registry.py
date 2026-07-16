# 📂 apps/admin_dashboard/registry.py
from .routes import admin_dashboard_bp 

MODULE_NAME = "لوحة التحكم"
MODULE_ICON = "fas fa-tachometer-alt"

LINKS = {
    "admin_dashboard_bp.dashboard": "الإحصائيات"
}

def register_module(app):
    try:
        app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
        
        # التعديل الذكي لإصلاح الـ BuildError في القوالب دون تعديلها:
        app.blueprints['admin_dashboard'] = admin_dashboard_bp
        
        print("✅ [Registry]: تم تسجيل موديول 'admin_dashboard_bp' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول الإحصائيات: {e}")
