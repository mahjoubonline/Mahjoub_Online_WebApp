import os
from flask import Flask
from models.supplier_db import db

def create_mahoub_app():
    app = Flask(__name__)
    
    # إعدادات قاعدة البيانات من Railway
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'MAHJOUB_2026_SOVEREIGN'

    db.init_app(app)

    # تسجيل المحركات (Blueprints)
    from apps.admin_portal.routes import admin_bp
    from apps.supplier_portal.routes import supplier_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)

    @app.route('/')
    def index():
        return "🛡️ منصة محجوب أونلاين: الهيكل الجديد يعمل بنجاح. جرب /admin/dashboard"

    return app

app = create_mahoub_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
