# coding: utf-8
# 📂 apps/admin_financial_management/registry.py

from apps.admin_financial_management.routes import financial_bp

# تعريف البيانات التعريفية ليقرأها النظام تلقائياً
MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fa-wallet"

def register_module(app):
    """
    تسجيل موديول الإدارة المالية.
    """
    app.register_blueprint(financial_bp, url_prefix='/admin/financial')
    print("✅ [Registry]: تم تسجيل موديول 'Admin Financial Management' بنجاح.")
