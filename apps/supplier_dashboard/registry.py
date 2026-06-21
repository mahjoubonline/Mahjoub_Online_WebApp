# coding: utf-8
# 📂 apps/supplier_dashboard/registry.py

from apps.supplier_dashboard.routes import supplier_bp

def register_app(app):
    """
    هذه الدالة هي "مفتاح التسجيل" الذي يبحث عنه المصنع الرئيسي.
    بدونها، لن يتم ربط لوحة تحكم المورد بالمشروع.
    """
    # ربط الـ Blueprint الخاص بلوحة تحكم المورد
    # سيتم الوصول للمسارات عبر: /supplier/dashboard, /supplier/products, إلخ.
    app.register_blueprint(supplier_bp)
    
    # سجل في الـ Logs لتأكيد الربط
    print("LOG: [System] Supplier Dashboard subsystem registered successfully.")
