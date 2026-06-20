# 📂 apps/vendors/registry.py
from apps.vendors.routes import vendors_bp

def register_app(app):  # <-- قمنا بتغيير الاسم هنا ليتطابق مع المصنع
    app.register_blueprint(vendors_bp, url_prefix='/vendors')
