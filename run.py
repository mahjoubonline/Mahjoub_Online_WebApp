import os
from flask import Flask, render_template
from config import Config
from core.models import db

# استيراد البوابات (Blueprints)
# ملاحظة: تأكد أن ملفات routes.py موجودة داخل هذه المجلدات
from admin_panel.routes import admin_bp
from supplier_panel.routes import supplier_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. تهيئة قاعدة البيانات
    db.init_app(app)

    # 2. تسجيل البوابات (Blueprints) لربط المجلدات
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)

    # 3. محاولة إنشاء الجداول بأمان
    with app.app_context():
        try:
            db.create_all()
            print("✅ قاعدة البيانات جاهزة والجداول تعمل بنجاح!")
        except Exception as e:
            print(f"⚠️ تحذير: لم يتم الاتصال بالقاعدة بعد. الخطأ: {e}")

    # 4. الصفحة الرئيسية العامة
    @app.route('/')
    def index():
        # هذه ستعرض صفحة الدخول الرئيسية (سوقك الذكي)
        return render_template('login.html')

    return app

app = create_app()

if __name__ == "__main__":
    # التوافق مع بورت Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
