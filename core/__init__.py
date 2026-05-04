import re
import random
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
        try:
            db.create_all() 
            print("✅ تم فحص وتحديث هيكل الترسانة الرقمية بنجاح.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه حوكمة البيانات: تعذر تحديث الهيكل تلقائياً: {e}")
        
        @login_manager.user_loader
        def load_user(user_id):
            """
            تحميل المستخدم مع معالجة الأخطاء لمنع انهيار النظام (Crash) 
            في حالة وجود تضارب في الجلسات أو قواعد البيانات.
            """
            try:
                # محاولة جلب المستخدم من قاعدة البيانات
                return User.query.get(int(user_id))
            except Exception as e:
                # في حالة حدوث خطأ (مثل نقص أعمدة في الجدول)، نقوم بعمل Rollback
                # لمنع تعليق الاتصال بقاعدة البيانات في Railway
                db.session.rollback()
                print(f"❌ User Loader Error: {e}")
                return None

        @app.context_processor
        def utility_processor():
            def get_sovereign_data():
                """
                توليد البيانات السيادية الموحدة (المعرف والمحفظة) برقم تسلسلي واحد.
                الهدف: MAH-9631 و W-MAH-9631
                """
                base_prefix = "MAH-963"
                try:
                    # نستخدم استعلاماً سريعاً للحصول على العدد لضمان عدم استهلاك الموارد
                    count = db.session.query(Vendor.id).count() if Vendor else 0
                    next_num = count + 1
                    
                    final_serial = f"{base_prefix}{next_num}"
                    
                    return {
                        "id": final_serial,
                        "wallet": f"W-{final_serial}"
                    }
                except Exception as e:
                    db.session.rollback()
                    print(f"⚠️ خطأ في توليد البيانات السيادية: {e}")
                    # حالة احتياطية تعتمد على رقم عشوائي مؤقت لمنع توقف الصفحة
                    rand_id = random.randint(100, 999)
                    return {"id": f"{base_prefix}{rand_id}", "wallet": f"W-{base_prefix}{rand_id}"}

            sov_data = get_sovereign_data()
            
            # جعل المعرفات متاحة في جميع القوالب (Templates)
            return dict(
                next_id=sov_data['id'],
                next_wallet=sov_data['wallet']
            )

        # تسجيل البلوبيرنت الخاص بلوحة الإدارة (مركز القيادة)
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
