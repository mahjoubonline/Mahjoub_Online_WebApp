# 📂 apps/vendors/registry.py
from apps.vendors.routes import vendors_bp

def register_app(app):
    """
    هذه الدالة تستدعى تلقائياً من قبل المصنع الرئيسي (apps/__init__.py)
    لأن المصنع يبحث عن اسم register_app تحديداً.
    """
    app.register_blueprint(vendors_bp, url_prefix='/vendors')
