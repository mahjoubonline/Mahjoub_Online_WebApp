# coding: utf-8
# 📂 apps/admin_platform_treasury/registry.py

# لا تستورد هنا في الأعلى لتجنب الـ Circular Import
# from apps.admin_platform_treasury.routes import treasury_bp 

# القائمة فارغة ليختفي الموديول من القائمة الجانبية (لأننا ربطناه في موديول الرقابة المالية)
LINKS = {} 

def register_module(app):
    """
    تسجيل الموديول باستخدام استيراد داخلي لتجنب التعارض الدائري.
    """
    try:
        # نقوم بالاستيراد هنا فقط عند التشغيل
        from apps.admin_platform_treasury.routes import treasury_bp
        
        app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'Admin Platform Treasury' بنجاح (مخفي من القائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
