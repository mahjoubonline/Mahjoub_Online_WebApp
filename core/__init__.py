from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# 1. تعريف كائن قاعدة البيانات المركزي
db = SQLAlchemy()

def create_app():
    # 2. إنشاء نسخة التطبيق
    app = Flask(__name__, static_folder='../static')
    
    # 3. تحميل الإعدادات
    app.config.from_object(Config)
    
    # 4. تهيئة قاعدة البيانات
    db.init_app(app)
    
    # 5. تسجيل الـ Blueprints (التعديل هنا لكسر الحلقة الدائرية)
    with app.app_context():
        try:
            # استيراد المسارات داخل بلوك الـ context يضمن أن التطبيق جاهز تماماً
            from admin_panel.routes import admin_bp
            from supplier_panel.routes import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ تم تسجيل Blueprints الإدارة والموردين بنجاح.")
        except Exception as e:
            print(f"❌ خطأ في استيراد الـ Blueprints: {e}")

    # 6. الواجهة الرئيسية الترحيبية
    @app.route('/')
    def index():
        return """
        <div style="text-align:center; margin-top:50px; font-family: 'Segoe UI', Tahoma, sans-serif; direction:rtl;">
            <h1 style="color: #6a0dad;">🚀 نظام محجوب أونلاين يعمل بنجاح!</h1>
            <p style="font-size: 18px; color: #555;">المحرك متصل الآن بقاعدة بيانات رندر وبوابة قمرة.</p>
            <div style="margin-top: 30px;">
                <a href="/admin/sync_now" style="display:inline-block; padding:15px 30px; background:#6a0dad; color:white; text-decoration:none; border-radius:25px; font-weight:bold; box-shadow: 0 4px 10px rgba(106, 13, 173, 0.3);">
                    دخول عرض المنتجات اللحظي ⬅️
                </a>
            </div>
        </div>
        """

    # 7. طباعة المسارات النشطة للتشخيص
    with app.app_context():
        print("🔗 المسارات المتاحة حالياً في النظام:")
        for rule in app.url_map.iter_rules():
            print(f"-> {rule}")

    return app
