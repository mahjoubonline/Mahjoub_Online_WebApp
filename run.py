import os
from flask import Flask
from core.extensions import db, login_manager
from apps.supplier_app.routes import supplier_bp

def create_app():
    app = Flask(__name__, static_folder='static')
    
    # تحميل الإعدادات من النواة
    from core.config import Config
    app.config.from_object(Config)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)

    # تسجيل المحركات (Blueprints)
    app.register_blueprint(supplier_bp)

    @app.route('/')
    def index():
        return "🛡️ نظام محجوب أونلاين السيادي يعمل بنجاح. اذهب إلى /suppliers"

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
