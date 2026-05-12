import os
from flask import Flask
from models.supplier_db import db  # تأكد أنك أنشأت مجلد models وبداخله هذا الملف

def create_mahoub_app():
    app = Flask(__name__)
    
    # 1. إعدادات قاعدة البيانات
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'MAHJOUB_ROYAL_2026'

    # 2. تهيئة قاعدة البيانات
    db.init_app(app)

    # 3. تسجيل البوابات (Blueprints)
    from apps.admin_portal.routes import admin_bp
    from apps.supplier_portal.routes import supplier_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)

    # --- [ الجزء البديل لـ init_db.py ] ---
    with app.app_context():
        db.create_all() # سيقوم بإنشاء الجداول تلقائياً عند تشغيل الموقع
        print("✅ تم تأسيس قاعدة البيانات السيادية بنجاح داخل run.py")

    @app.route('/')
    def index():
        return "<h1 style='color:gold; background:black; text-align:center;'>🛡️ محجوب أونلاين: النظام يعمل بكفاءة</h1>"

    return app

app = create_mahoub_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
