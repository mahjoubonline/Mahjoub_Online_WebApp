# coding: utf-8
from apps.suppliers_orders.routes import suppliers_orders_bp

# تأكد من أن اسم الموديول (suppliers_orders) لا يتكرر
def register_module(app):
    # نستخدم url_prefix خاص لتجنب أي تداخل
    app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers_orders')
