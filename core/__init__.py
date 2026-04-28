import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية للنظام
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 2. جلب الإعدادات (دعم Railway و Render و SQLite)
    try:
        from config import Config
        app.config.from_object(Config)
    except ImportError:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///mahjoub_online.db'
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub-secret-key-123'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 4. إعدادات إدارة الدخول
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # 5. استيراد الموديلات
        from core.models.user import User
        from core.models.product import Product
        from core.models.supplier import Supplier
        
        # --- 🚧 إجراء التطهير السيادي (يُنفذ لمرة واحدة فقط لحل تضارب Render) 🚧 ---
        try:
            print("🧹 جاري تصفير الجداول القديمة في Render...")
            db.drop_all() # حذف الجداول التي تفتقد للأعمدة الجديدة
            
            print("🏗️ جاري إعادة بناء الجداول بالهيكلية الصحيحة...")
            db.create_all() # إنشاء الجداول بوجود password_hash و status و role
            print("✅ تم تجهيز قاعدة البيانات بنجاح")
        except Exception as e:
            print(f"⚠️ تنبيه أثناء التحديث: {e}")
        # -----------------------------------------------------------------------

        # 6. تسجيل البوابات
        try:
            from supplier_panel.routes import supplier_bp
            if 'supplier_panel' not in app.blueprints:
                app.register_blueprint(supplier_bp, url_prefix='/supplier')
        except Exception as e:
            print(f"⚠️ خطأ بوابة الموردين: {e}")

        try:
            from admin_panel.routes import admin_bp 
            if 'admin_panel' not in app.blueprints:
                app.register_blueprint(admin_bp, url_prefix='/admin')
        except Exception as e:
            print(f"⚠️ خطأ بوابة الإدارة: {e}")

        # 7. تعميد الحسابات السيادية فوراً بعد البناء الجديد
        try:
            # تعميد حساب المورد
            if not User.query.filter_by(username="محجوب أونلاين").first():
                sys_supplier = User(username="محجوب أونلاين", role="supplier", status="approved")
                sys_supplier.set_password("123")
                db.session.add(sys_supplier)
            
            # تعميد حساب المدير (علي محجوب)
            if not User.query.filter_by(username="علي محجوب").first():
                admin_user = User(username="علي محجوب", role="admin", status="approved")
                admin_user.set_password("123")
                db.session.add(admin_user)
                
            db.session.commit()
            print("✨ تم تعميد الحسابات السيادية بنجاح (كلمة السر الافتراضية: 123)")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ فشل في عملية التعميد الآلي: {e}")

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    try:
        return db.session.get(User, int(user_id))
    except:
        return None
