from .routes import vendors_bp # استيراد الـ Blueprint من ملف المسارات الخاص بك

def register_app(app):
    # هنا يتم تسجيل التطبيق تلقائياً عند تشغيل المصنع الأم
    app.register_blueprint(vendors_bp, url_prefix='/vendors')
