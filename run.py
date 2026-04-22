import os
from flask import Flask
from flask_login import LoginManager
# استيراد المكونات من ملفاتك المنفصلة
from admin_panel.models import db, User
from admin_panel.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)

    # 1. إعدادات الأمان وقاعدة البيانات
    # ملاحظة: تم تعديل الرابط ليتوافق مع SQLAlchemy (postgresql://)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_sovereign_key_2026')
    
    # وضع الرابط الذي زودتني به
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mahjoub_online_1_db_user:S7dxtVGcKwrsM1QEzGOuPPcRL8dKxgXk@dpg-d79tuthr0fns73epej4g-a/mahjoub_online_1_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 2. ربط قاعدة البيانات بالتطبيق
    db.init_app(app)

    # 3. إعداد نظام إدارة الدخول (Login Manager)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login' # اسم المسار في الـ Blueprint

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4. تسجيل الـ Blueprint الخاص بلوحة التحكم
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 5. تهيئة قاعدة البيانات وإنشاء مستخدم القائد
    with app.app_context():
        try:
            db.create_all()
            # التحقق من وجود حساب "علي محجوب" بالعربي
            admin_user = User.query.filter_by(username='علي محجوب').first()
            if not admin_user:
                new_admin = User(username='علي محجوب', role='SuperAdmin')
                # نضع كلمة مرور افتراضية، يرجى تغييرها فور الدخول
                new_admin.set_password('123456') 
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم إنشاء حساب القائد (علي محجوب) بنجاح في قاعدة البيانات.")
            else:
                print("✅ تم الاتصال بقاعدة البيانات، حساب القائد موجود مسبقاً.")
        except Exception as e:
            print(f"❌ فشل الاتصال بالقاعدة أو إنشاء الجداول: {str(e)}")

    return app

app = create_app()

if __name__ == '__main__':
    # Railway و Render يتطلبون الاستماع على 0.0.0.0 والمنفذ 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
