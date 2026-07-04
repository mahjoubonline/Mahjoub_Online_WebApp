# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

from apps.admin_suppliers_list.routes import suppliers_bp

# هذه المتغيرات العامة هي ما يبحث عنه النظام لرسم القائمة الجانبية
MODULE_NAME = "سجل الشركاء"
MODULE_ICON = "fas fa-handshake"
LINKS = {
    "قائمة الشركاء": "suppliers_bp.list_suppliers"
}

def register_module(app):
    # تسجيل مسارات الموردين/الشركاء في النظام
    app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
    print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_list' بنجاح.")
