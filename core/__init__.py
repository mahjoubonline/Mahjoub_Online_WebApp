from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# تهيئة الكائنات الأساسية للمنصة السيادية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # بديل CORS: إضافة رؤوس الاستجابة يدويًا للسماح بالطلبات المتقاطعة
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # ربط الإضافات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات نظام تسجيل الدخول
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    with app.app_context():
        # --- حل مشكلة التبعية (Foreign Key Error) ---
        # استيراد كافة النماذج هنا لضمان تسجيلها في MetaData الخاص بـ SQLAlchemy
        from core.models.user import User
        from core.models.vendor import Vendor
        
        # --- إجراء التحديث الجذري لقاعدة البيانات ---
        # الآن drop_all ستعرف بوجود جدول 'users' ولن تظهر رسالة الخطأ
        try:
            db.drop_all() 
            db.create_all()
            print("🛡️ الترسانة الرقمية: تم إعادة بناء الجداول السيادية بنجاح.")
        except Exception as e:
            print(f"⚠️ فشل في تحديث الجداول: {e}")
        
        # إعداد محمل المستخدم لنظام Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # --- دالة توليد الرقم السيادي للموردين ---
        @app.context_processor
        def utility_processor():
            def get_next_vendor_id():
                try:
                    # جلب آخر مورد مسجل لزيادة الرقم التسلسلي
                    last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
                    
                    if last_vendor and last_vendor.e_wallet and '-' in last_vendor.e_wallet:
                        # استخراج الجزء الرقمي من MAH-9631 وزيادته
                        parts = last_vendor.e_wallet.split('-')
                        if len(parts) > 1:
                            current_num = int(parts[1])
                            return f"MAH-{current_num + 1}"
                    
                    return "MAH-9631" # القيمة الافتراضية لأول مورد
                except Exception:
                    return "MAH-9631"
            
            return dict(next_id=get_next_vendor_id())

        # تسجيل الـ Blueprints (لوحة التحكم الإدارية)
        # ملاحظة: يتم الاستيراد هنا لتجنب Circular Import
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
