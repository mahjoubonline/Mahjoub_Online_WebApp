# coding: utf-8
# 📂 apps/suppliers_auth_portal/registry.py - مسجل موديول الموردين والمسوقين

from apps.suppliers_auth_portal.routes import suppliers_bp

def register_module(app):
    """
    تسجيل بوابة الموردين والمسوقين السيادية داخل تطبيق Flask الرئيسي.
    تم إزالة نظام التحقق (OTP) والاعتماد على الدخول المباشر.
    """
    try:
        # تسجيل الـ Blueprint
        app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
        
        print("✅ [Module Registry]: تم تسجيل بوابة الموردين (دخول مباشر) بنجاح (/suppliers)")
        
    except Exception as e:
        print(f"🚨 [Module Registry Error]: فشل تسجيل موديول الموردين: {e}")

# إعدادات الموديول الفنية
MODULE_CONFIG = {
    "module_name": "suppliers_auth_portal",
    "version": "2.1.0",
    "auth_type": "Direct Credentials",
    "secured": True
}
