from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from sqlalchemy import text # لاستخدام أوامر SQL المباشرة

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'admin.admin_login'

    from core.models.user import User 
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # --- منطق التحديث التلقائي (Auto-Update Logic) ---
        try:
            # تنفيذ أمر إضافة العمود إذا لم يكن موجوداً
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(120);'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT \'supplier\';'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;'))
            db.session.commit()
            print("✅ تم فحص وتحديث قاعدة البيانات بنجاح.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه: قاعدة البيانات محدثة بالفعل أو حدث خطأ بسيط: {e}")
        # -----------------------------------------------

        from admin_panel import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        @app.route('/')
        def index():
            return redirect(url_for('admin.admin_login'))

    return app
