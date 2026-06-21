# 📂 apps/vendor_dashboard/registry.py

from apps.vendor_dashboard.routes import dashboard_bp

def register_app(app):
    """
    هذه الدالة هي "مفتاح التشغيل" الذي يستدعيه المصنع تلقائياً.
    تقوم بتسجيل Blueprint لوحة التحكم تحت المسار /supplier
    """
    app.register_blueprint(dashboard_bp, url_prefix='/supplier')
