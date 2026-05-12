from flask import Flask
from core.extensions import db, login_manager
from core.setup.initializer import initialize_sovereign_system
import os

def create_app():
    app = Flask(__name__)
    
    # تحميل الإعدادات من ملف config
    app.config.from_object('config.Config')

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)

    # 🚀 تفعيل محرك الهيكلة التلقائية
    initialize_sovereign_system(app)

    # تسجيل البلوبرنتات (ستقوم بتفعيلها تدريجياً)
    # from apps.supplier_app.routes import supplier_bp
    # app.register_blueprint(supplier_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
