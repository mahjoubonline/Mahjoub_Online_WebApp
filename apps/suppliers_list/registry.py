# coding: utf-8
# 📂 apps/suppliers_list/registry.py

from apps.suppliers_list.routes import supplier_bp

def register_module(app):
    """
    هذه الدالة هي التي يبحث عنها ملف apps/__init__.py 
    للقيام بالتسجيل التلقائي لموديول قائمة الشركاء (الموردين).
    """
    app.register_blueprint(supplier_bp, url_prefix='/suppliers')
    print("✅ [Registry]: تم تسجيل موديول 'Suppliers' بنجاح.")
