import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # الإعدادات
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_9046_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'supplier_panel.login'

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith('/admin_control_9046'):
            return redirect(url_for('admin_panel.admin_login'))
        return redirect(url_for('supplier_panel.login'))

    with app.app_context():
        # تسجيل بوابة الموردين
        from supplier_panel import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # تسجيل بوابة الإدارة بطريقة (Dynamic Import) لتجنب خطأ الاسم
        try:
            import admin_panel
            # هنا نقوم بالبحث عن أي كائن من نوع Blueprint داخل المجلد وتسجيله تلقائياً
            for item in dir(admin_panel):
                obj = getattr(admin_panel, item)
                if hasattr(obj, 'name') and item.endswith('_bp'): # سيبحث عن أي اسم ينتهي بـ _bp
                    app.register_blueprint(obj, url_prefix='/admin_control_9046')
                    print(f"✅ تم تسجيل البوابة: {item}")
        except Exception as e:
            print(f"⚠️ تنبيه: لم يتم العثور على بوابة في مجلد الإدارة أو حدث خطأ: {e}")

        db.create_all()

    return app

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
