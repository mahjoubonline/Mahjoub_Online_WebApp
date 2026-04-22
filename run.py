import os
from flask import Flask, render_template
from config import Config
from core.models import db
from jinja2 import ChoiceLoader, FileSystemLoader

def create_app():
    # إنشاء تطبيق Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. تهيئة قاعدة البيانات
    db.init_app(app)

    # 2. حل مشكلة المسارات (الجزء الأهم لـ Railway)
    # نجعل Flask يبحث في المجلد الرئيسي وفي مجلدات البوابات (Admin & Supplier)
    root_path = os.getcwd()
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(os.path.join(root_path, 'templates')),
        FileSystemLoader(os.path.join(root_path, 'admin_panel', 'templates')),
        FileSystemLoader(os.path.join(root_path, 'supplier_panel', 'templates')),
    ])

    # 3. تسجيل البوابات (Blueprints)
    from admin_panel.routes import admin_bp
    from supplier_panel.routes import supplier_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)

    # 4. إنشاء الجداول في قاعدة البيانات عند التشغيل
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Database error: {e}")

    # 5. المسار الرئيسي للموقع
    @app.route('/')
    def index():
        return render_template('login.html')

    return app

# تشغيل التطبيق
app = create_app()

if __name__ == "__main__":
    # الحصول على المنفذ من بيئة التشغيل (مهم لـ Railway)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
