
# coding: utf-8
# 📂 apps/suppliers_product/registry.py

"""
تسجيل تطبيق منتجات الموردين في المنصة
"""

from flask import Blueprint

# تعريف الـ Blueprint الرئيسي
suppliers_product_bp = Blueprint(
    'suppliers_product_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/suppliers_product/static'
)


def register_plugin(app):
    """
    تسجيل التطبيق في التطبيق الرئيسي
    """
    # استيراد الـ routes بعد تعريف الـ Blueprint لتجنب Circular Import
    from apps.suppliers_product import routes
    
    # تسجيل الـ Blueprint
    app.register_blueprint(suppliers_product_bp, url_prefix='/supplier')
    
    return app
