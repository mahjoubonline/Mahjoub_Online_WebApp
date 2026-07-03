# coding: utf-8
# 📂 apps/admin_platform_treasury/registry.py

from apps.admin_platform_treasury.routes import treasury_bp

# البيانات التعريفية للظهور التلقائي في القائمة الجانبية
MODULE_NAME = "خزينة المنصة"
MODULE_ICON = "fa-vault"

def register_module(app):
    """تسجيل موديول الخزينة بشكل آمن."""
    app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
    print("✅ [Registry]: تم تسجيل موديول 'admin_platform_treasury' بنجاح.")
