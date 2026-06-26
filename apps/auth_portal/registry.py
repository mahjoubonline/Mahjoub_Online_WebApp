# coding: utf-8
# 📂 apps/auth_portal/registry.py

from .routes import auth_portal

def register_module(app):
    """
    دالة التسجيل الديناميكي: 
    يتم استدعاؤها من قبل المصنع (Factory) لاكتشاف وتسجيل 
    الـ Blueprints الخاصة بموديول البوابة.
    """
    # تسجيل الـ Blueprint الخاص بالبوابة
    app.register_blueprint(auth_portal, url_prefix='/auth')
    
    # يمكنك إضافة أي تهيئة إضافية خاصة بهذا الموديول هنا، مثل:
    # app.logger.info("تم تفعيل موديول Auth Portal بنجاح")
