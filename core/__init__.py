import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # رؤوس CORS للسماح بالعمليات المتقاطعة
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد النماذج لضمان تسجيلها في SQLAlchemy قبل إنشاء الجداول
        from core.models.user import User
        from core.models.vendor import Vendor
        
        # 🛡️ تصحيح الترسانة: حل مشكلة العمود المفقود (user_id)
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
                منطق جلب المعرف السيادي التالي بناءً على التسلسل:
                MAH-963 + (1, 2, 3...) -> MAH-9631
                """
                base_prefix = "MAH-963"
                try:
                    db.session.rollback()
                    # جلب آخر مورد تمت إضافته للترسانة
                    last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
                    
                    if last_vendor and last_vendor.supplier_id:
                        # استخدام Regex لاستخراج الأرقام التي تأتي بعد MAH-963
                        # يبحث عن الرقم التسلسلي في المعرف الحالي
                        match = re.search(rf"{base_prefix}(\d+)", last_vendor.supplier_id)
                        if match:
                            next_num = int(match.group(1)) + 1
                            return f"{base_prefix}{next_num}"
                    
                    # إذا لم يوجد موردين سابقين، نبدأ بأول معرف سيادي
                    return f"{base_prefix}1" # النتيجة: MAH-9631
                except Exception as e:
                    print(f"⚠️ خطأ في توليد المعرف: {e}")
                    return f"{base_prefix}1"

            # جعل next_id و next_wallet متاحين في جميع القوالب (Templates)
            current_id = get_next_vendor_id()
            return dict(
                next_id=current_id,
                next_wallet=f"W-{current_id}"
            )

        # تسجيل البلوبيرنت الخاص بلوحة الإدارة
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
