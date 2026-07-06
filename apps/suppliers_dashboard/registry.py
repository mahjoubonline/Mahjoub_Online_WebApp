def register_module(app):
    # استخدام اسم الـ blueprint بدلاً من الموديول بالكامل
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل موديول 'suppliers_dashboard' بنجاح.")
    else:
        # إذا كان مسجلاً، لا تفعل شيئاً (تجاهل التكرار)
        pass
