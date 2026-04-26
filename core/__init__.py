from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# --- 🛡️ تهيئة الترسانة البرمجية الأساسية ---
# يتم تعريف الكائنات هنا لضمان توفرها في كامل النظام دون تداخل
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الموارد
    # تم ضبط المسارات لضمان وصول السيرفر للملفات الثابتة والقوالب بدقة
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بنواة التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. بروتوكولات الحماية وتسجيل الدخول الافتراضية
    login_manager.login_view = 'admin_panel.login'  
    login_manager.login_message = "يرجى إثبات هويتك للوصول إلى هذه المنطقة السيادية."
    login_manager.login_message_category = "info"

    with app.app_context():
        # --- 📦 استيراد النماذج (Models) داخل السياق لمنع التداخل ---
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product
        
        # --- 🔐 نظام الفصل الذكي بين الهويات (Advanced Multi-Auth) ---
        @login_manager.user_loader
        def load_user(user_id):
            try:
                # نعتمد على 'user_type' المخزن في الجلسة (Session) عند تسجيل الدخول
                # لضمان عدم حدوث تداخل في حال تشابهت المعرفات (IDs) بين جدول القادة والموردين
                user_type = session.get('user_type')

                if user_type == 'supplier':
                    return Supplier.query.get(int(user_id))
                
                # الافتراضي هو البحث في جدول المستخدمين (الأدمن/القادة)
                return User.query.get(int(user_id))
            
            except Exception as e:
                app.logger.error(f"⚠️ [Auth Error] فشل التعرف على الهوية: {e}")
                return None

        # --- 🔗 تسجيل بوابات النظام (Blueprints Registration) ---
        try:
            # 1. بوابة الإدارة المركزية (برج الرقابة)
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # 2. بوابة الموردين (نظام الحوكمة اللامركزي)
            # تأكد من أن المجلد يحتوي على ملف __init__.py يُعرف الـ blueprint
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم تفعيل البوابات السيادية وفصل الصلاحيات بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] خطأ في ربط بوابات النظام: {e}")

        # --- 📊 معالج البيانات الشامل (Context Processor) ---
        # جعل البيانات الهامة متوفرة في كل القوالب تلقائياً (مثل تنبيهات الشريط الجانبي)
        @app.context_processor
        def inject_global_data():
            try:
                # حساب عدد الموردين الذين ينتظرون "الاعتماد السيادي"
                p_suppliers = Supplier.query.filter_by(is_approved=False).count()
                return dict(pending_suppliers_count=p_suppliers)
            except Exception:
                return dict(pending_suppliers_count=0)

        # --- 🛠️ تهيئة قاعدة البيانات اللحظية ---
        # يقوم بإنشاء الجداول في Postgres إذا لم تكن موجودة عند أول تشغيل
        db.create_all()

    return app
