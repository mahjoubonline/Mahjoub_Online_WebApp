# 📂 apps/vendors/registry.py
from .routes import vendors_bp 

def register_app(app):
    """
    دالة التسجيل الذاتي للتطبيق في المصنع الأم.
    هذه الدالة تُستدعى تلقائياً من قبل apps/__init__.py
    """
    # تسجيل مسارات الموردين تحت البادئة /vendors
    app.register_blueprint(vendors_bp, url_prefix='/vendors')
    
    # يمكن إضافة أي إعدادات خاصة بالموردين هنا مستقبلاً
    # مثل تسجيل الـ Context Processors أو أي إضافات خاصة بهم
