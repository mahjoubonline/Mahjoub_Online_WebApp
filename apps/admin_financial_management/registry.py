# coding: utf-8
# 📂 apps/admin_financial_management/registry.py

from apps.admin_financial_management.routes import admin_financial_bp

def register_module(app):
    """
    تسجيل موديول الإدارة المالية للطلبات.
    يتم تسجيله على المسار /admin/financial
    """
    app.register_blueprint(admin_financial_bp, url_prefix='/admin/financial')
    print("✅ [Registry]: تم تسجيل موديول 'Admin Financial Management' بنجاح على المسار /admin/financial")
