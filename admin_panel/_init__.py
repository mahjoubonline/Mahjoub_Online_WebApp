# 7. تسجيل بوابة الإدارة (برج الرقابة 🏛️)
        try:
            # هنا نقوم بالاستيراد المباشر من ملف routes داخل مجلد الإدارة
            from admin_panel.routes import admin_bp 
            app.register_blueprint(admin_bp, url_prefix='/admin')
            print("✅ تم تفعيل برج الرقابة المركزية بنجاح")
        except ImportError as e:
            print(f"❌ خطأ استيراد: {e}")
        except Exception as e:
            print(f"⚠️ خطأ عام في بوابة الإدارة: {e}")
