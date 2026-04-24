from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# تعريف كائن قاعدة البيانات
db = SQLAlchemy()

def create_app():
    # 1. إنشاء نسخة التطبيق
    app = Flask(__name__, static_folder='../static')
    
    # 2. تحميل الإعدادات من ملف config.py
    app.config.from_object(Config)
    
    # 3. تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)
    
    # 4. تسجيل الـ Blueprints الأساسية (تمت إزالة الويب هوك)
    try:
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        
        # ربط لوحة الإدارة ولوحة الموردين
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')
        
        print("✅ تم تسجيل Blueprints الإدارة والموردين بنجاح.")
    except ImportError as e:
        print(f"❌ خطأ في استيراد الـ Blueprints: {e}")

    # 5. الصفحة الرئيسية لـ "محجوب أونلاين"
    @app.route('/')
    def index():
        return """
        <div style="text-align:center; margin-top:50px; font-family: 'Segoe UI', Tahoma, sans-serif; direction:rtl;">
            <h1 style="color: #6a0dad;">🚀 نظام محجوب أونلاين يعمل بنجاح!</h1>
            <p style="font-size: 18px; color: #555;">المحرك متصل الآن بقاعدة بيانات رندر وبوابة قمرة.</p>
            <div style="margin-top: 30px;">
                <a href="/admin/" style="display:inline-block; padding:15px 30px; background:#6a0dad; color:white; text-decoration:none; border-radius:25px; font-weight:bold; box-shadow: 0 4px 10px rgba(106, 13, 173, 0.3);">
                    دخول لوحة الإدارة ⬅️
                </a>
            </div>
        </div>
        """

    # 6. طباعة المسارات النشطة للتأكد من الحالة
    with app.app_context():
        print("🔗 المسارات النشطة حالياً:")
        for rule in app.url_map.iter_rules():
            print(f"-> {rule}")

    return app
