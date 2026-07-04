# coding: utf-8
# 📂 apps/admin_platform_treasury/registry.py

# لا نستورد هنا لتجنب الـ Circular Import
LINKS = {
    "الخزينة المركزية": "treasury_bp.dashboard" 
}

def register_module(app):
    """
    تسجيل الموديول وتفعيله ليظهر في القائمة الجانبية.
    """
    try:
        from apps.admin_platform_treasury.routes import treasury_bp
        app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'Admin Platform Treasury' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
