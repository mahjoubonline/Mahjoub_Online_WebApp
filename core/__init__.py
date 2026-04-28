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

    # 2. جلب الإعدادات (دعم Railway و SQLite)
    try:
        from config import Config
        app.config.from_object(Config)
    except ImportError:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///mahjoub_online.db'
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub-secret-key-123'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. تهيئة الإضافات وربطها بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 4. إعدادات إدارة الدخول والوصول السيادي
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # 5. استيراد الموديلات لضمان التعرف على الجداول
        from core.models.user import User
        from core.models.product import Product
        from core.models.supplier import Supplier
        
        # 6. تسجيل بوابة الموردين (بشكل آمن لتفادي أخطاء الاستيراد)
        try:
            from supplier_panel.routes import supplier_bp
            if 'supplier_panel' not in app.blueprints:
                app.register_blueprint(supplier_bp, url_prefix='/supplier')
                print("✅ تم تفعيل بوابة الموردين بنجاح")
        except Exception as e:
            print(f"⚠️ تنبيه: خطأ في استيراد بوابة الموردين: {e}")

        # 7. تسجيل بوابة الإدارة (برج الرقابة 🏛️)
        try:
            from admin_panel.routes import admin_bp 
            if 'admin_panel' not in app.blueprints:
                app.register_blueprint(admin_bp, url_prefix='/admin')
                print("✅ تم تفعيل برج الرقابة المركزية بنجاح")
        except Exception as e:
            print(f"⚠️ خطأ في بوابة الإدارة: {e}")

        # 8. إدارة قاعدة البيانات والبيانات السابقة
        try:
            # محاولة إنشاء الجداول الجديدة فقط دون التأثير على البيانات القديمة
            db.create_all() 
            
            # 9. تعميد حساب المورد الأول (بشكل مرن لامتصاص أخطاء الجداول القديمة)
            if not User.query.filter_by(username="محجوب أونلاين").first():
                print("🚀 جاري محاولة تعميد حساب المورد...")
                sys_supplier = User(username="محجوب أونلاين", role="supplier")
                
                # التحقق البرمجي من وجود العمود 'status' لتجنب انهيار السيرفر في حال قدم الجدول
                if hasattr(sys_supplier, 'status'):
                    sys_supplier.status = "approved"
                
                sys_supplier.set_password("123")
                db.session.add(sys_supplier)
                db.session.commit()
                print("✨ تم إنشاء حساب المورد بنجاح")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ ملاحظة: السيرفر يعمل ولكن هناك تعارض مع الجداول السابقة: {e}")
            print("💡 نصيحة: إذا استمر الخطأ، يفضل تحديث قاعدة البيانات (Migration) أو مسحها.")

    return app

# 10. محمل المستخدم (User Loader)
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    try:
        # استخدام الطريقة المستقرة لجلب الهوية السيادية
        return db.session.get(User, int(user_id))
    except Exception as e:
        return None
