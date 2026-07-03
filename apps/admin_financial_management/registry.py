# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

from apps.admin_suppliers_list.routes import suppliers_bp

def register_module(app):
    """
    تسجيل موديول إدارة الموردين.
    """
    app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
    print("✅ [Registry]: تم تسجيل موديول 'Admin Suppliers List' بنجاح.")
