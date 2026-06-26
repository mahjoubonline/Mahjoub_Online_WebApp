# coding: utf-8
# 📂 apps/admin_dashboard/registry.py

"""
مسجل موديول لوحة تحكم المسؤول (admin_dashboard)
يقوم هذا الملف بربط بلوبرينت الإدارة بالتطبيق الرئيسي مع عزل كامل للمسارات.
"""

from .routes import admin_dashboard

def register_module(app):
    """
    تسجيل موديول لوحة تحكم المسؤول في التطبيق.
    url_prefix='/admin' يضمن أن جميع المسارات داخل هذا الموديول
    تبدأ بـ /admin (مثال: /admin/dashboard).
    """
    # تسجيل البلوبرينت مع بادئة المسار
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    
    # رسالة تأكيد في سجلات التشغيل (Console) لمراقبة عملية التسجيل
    print(f"✅ [Registry] تم تسجيل موديول 'admin_dashboard' بنجاح على المسار (/admin).")
