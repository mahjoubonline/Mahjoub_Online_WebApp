# coding: utf-8
from .routes import admin_dashboard

def register_module(app):
    """
    تسجيل موديول لوحة تحكم المسؤول (admin_dashboard) في تطبيق Flask.
    يتم استدعاء هذه الدالة تلقائياً بواسطة نظام الـ Auto-Discovery.
    """
    # تسجيل الـ Blueprint
    # ملاحظة: تم تعريف url_prefix داخل الـ Blueprint نفسه في routes.py،
    # لذا لا نحتاج لإضافته هنا لضمان عدم تكرار المسار.
    app.register_blueprint(admin_dashboard)
    
    print(f"✅ [Registry] تم تسجيل admin_dashboard بنجاح.")
