# coding: utf-8
from .routes import admin_dashboard

def register_module(app):
    """
    تسجيل موديول لوحة تحكم المسؤول (admin_dashboard)
    تم إضافة url_prefix='/admin' لعزل مسارات الإدارة.
    """
    # إضافة url_prefix='/admin' هنا هو الحل الجذري
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    
    print(f"✅ [Registry] تم تسجيل admin_dashboard بنجاح على المسار (/admin).")
