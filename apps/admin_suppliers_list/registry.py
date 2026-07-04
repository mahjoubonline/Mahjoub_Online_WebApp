# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

from apps.admin_suppliers_list.routes import suppliers_bp

def register_module(app):
    # تسجيل مسارات الموردين/الشركاء في النظام
    app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
    
    # هذه البيانات هي التي ستجعل الموديول يظهر في القائمة الجانبية (Sidebar)
    return {
        "name": "سجل الشركاء",                  # الاسم الذي سيظهر في لوحة التحكم
        "icon": "fas fa-handshake",              # أيقونة معبرة عن الشركاء/الموردين
        "endpoint": "suppliers_bp.list_suppliers" # الدالة التي ستعمل عند النقر على الرابط
    }
