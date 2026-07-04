# coding: utf-8
# 📂 apps/admin_platform_treasury/registry.py

from apps.admin_platform_treasury.routes import treasury_bp

MODULE_NAME = "الخزينة"
MODULE_ICON = "fa-vault"

# تم تعديل الرابط ليتطابق مع اسم الدالة التي سنعدلها (أو يمكنك استخدام treasury_bp.index)
LINKS = {
    "خزينة المنصة": "treasury_bp.dashboard" 
}

def register_module(app):
    try:
        app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'Admin Platform Treasury' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
