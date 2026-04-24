from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# تعريف كائن قاعدة البيانات (سيتم ربطه لاحقاً في دالة المصنع)
db = SQLAlchemy()

def create_app():
    # 1. إنشاء نسخة التطبيق
    # ملاحظة: أزلنا تحديد template_folder هنا لنسمح للـ Blueprints باستخدام مجلداتها الخاصة
    app = Flask(__name__, 
                static_folder='../static')
    
    # 2. تحميل الإعدادات من ملف config.py
    app.config.from_object(Config)
    
    # 3. تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)
    
    # 4. تسجيل الـ Blueprints (الأجزاء المختلفة للمشروع)
    # ملاحظة: تأكد أن ملفات routes.py داخل المجلدات تستخدم template_folder='templates'
    try:
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        from webhooks.routes import webhooks_bp
        
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')
        app.register_blueprint(webhooks_bp, url_prefix='/webhooks')
        
        print("✅ تم تسجيل جميع الـ Blueprints بنجاح.")
    except ImportError as e:
        print(f"❌ خطأ في استيراد الـ Blueprints: {e}")

    # 5. صفحة رئيسية بسيطة للفحص السريع (Health Check)
    @app.route('/')
    def index():
        return """
        <div style="text-align:center; margin-top:50px; font-family:Arial;">
            <h1 style="color: #4B0082;">Mahjoub Online System is Running!</h1>
            <p>السيرفر يعمل بنجاح، جرب الدخول لروابط الإدارة أو المورد.</p>
            <a href="/admin">لوحة الإدارة</a> | <a href="/supplier">لوحة المورد</a>
        </div>
        """

    # 6. طباعة خريطة المسارات في الـ Logs للتأكد (اختياري)
    with app.app_context():
        print("🔗 قائمة المسارات النشطة:")
        for rule in app.url_map.iter_rules():
            print(f"-> {rule}")

    return app
