import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# إنشاء كائنات النظام الأساسية (العمود الفقري)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # رؤوس CORS للسماح بالعمليات المتقاطعة (التواصل السيادي بين الأنظمة)
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # تهيئة الإضافات داخل التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حوكمة الدخول
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد النماذج لضمان تسجيلها في SQLAlchemy قبل إنشاء الجداول
        from core.models.user import User
        from core.models.vendor import Vendor
        
        # 🛡️ تصحيح الترسانة: ضمان وجود الجداول وتحديث الهيكل
        db.session.rollback()
        try:
            db.create_all() 
            print("✅ تم فحص وتحديث هيكل الترسانة الرقمية بنجاح.")
        except Exception as e:
            print(f"⚠️ تنبيه حوكمة البيانات: تعذر تحديث الهيكل تلقائياً: {e}")
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.context_processor
        def utility_processor():
            def get_next_vendor_id():
                """
                منطق جلب المعرف السيادي التالي بناءً على التسلسل المطلوب:
                MAH-963 + (1, 2, 3...) -> MAH-9631
                """
                base_prefix = "MAH-963"
                try:
                    db.session.rollback()
                    # جلب عدد الموردين الحاليين لضمان التسلسل التصاعدي المستقر
                    # نعتمد على العد (Count) لضمان أن المورد الأول يأخذ رقم 1
                    count = db.session.query(Vendor).count()
                    next_num = count + 1
                    
                    # النتيجة المرجوة: MAH-9631 للمورد الأول، MAH-9632 للثاني...
                    return f"{base_prefix}{next_num}"
                    
                except Exception as e:
                    print(f"⚠️ خطأ في توليد المعرف السيادي: {e}")
                    return f"{base_prefix}1"

            # استخراج المعرف الحالي ليتم استخدامه في القوالب
            current_id = get_next_vendor_id()
            
            # جعل next_id و next_wallet متاحين في جميع واجهات القوالب (Jinja2)
            # المحفظة تتبع المعرف تلقائياً: W-MAH-9631
            return dict(
                next_id=current_id,
                next_wallet=f"W-{current_id}"
            )

        # تسجيل البلوبيرنت الخاص بلوحة الإدارة (مركز القيادة)
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
