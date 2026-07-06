# coding: utf-8
from flask import Flask
from apps.suppliers_dashboard.routes import suppliers_dashboard_bp

def register_suppliers_dashboard(app: Flask):
    """
    تسجيل الـ Blueprint الخاص بلوحة تحكم المورد في تطبيق Flask الرئيسي.
    """
    # تسجيل الـ Blueprint مع تحديد بادئة المسار (URL Prefix)
    # هذا سيجعل جميع المسارات تبدأ بـ /supplier/...
    app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
    
    print("✓ تم تسجيل لوحة تحكم المورد بنجاح.")

# ملاحظة: يتم استدعاء هذه الدالة لاحقاً في ملف `__init__.py` الرئيسي للتطبيق.
