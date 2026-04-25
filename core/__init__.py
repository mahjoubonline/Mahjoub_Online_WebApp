from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# تهيئة الكائنات الأساسية خارج الدالة لضمان توفرها في كامل النظام
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الملفات الثابتة والقوالب العامة
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. إعدادات نظام الحماية وتسجيل الدخول
    login_manager.login_view = 'admin_panel.login'  
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة السيادية."
    login_manager.login_message_category = "info"

    with app.app_context():
        # --- 🛡️ استيراد الموديلات المقسمة ---
        # هنا نقوم باستيراد الموديلات من المجلد الجديد لضمان تسجيلها في SQLAlchemy
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product
        
        # --- 🔐 نظام التعرف الذكي على الهوية (أدمن أو مورد) ---
        @login_manager.user_loader
        def load_user(user_id):
            try:
                # أولاً: البحث في الحسابات القيادية (User)
                admin = User.query.get(int(user_id))
                if admin:
                    return admin
                
                # ثانياً: البحث في حسابات شركاء النجاح (Supplier)
                # ضروري جداً لعمل المحفظة اللامركزية MAH-9046
                return Supplier.query.get(int(user_id))
            except Exception as e:
                print(f"⚠️ [Auth Error] فشل تحميل المستخدم: {e}")
                return None

        # --- 🔗 تسجيل بوابات النظام (Blueprints) ---
        try:
            # تسجيل لوحة الإدارة المركزية
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # تسجيل بوابة الموردين (نظام شركاء النجاح)
            from supplier_panel import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم ربط جميع المسارات السيادية بنجاح (الإدارة + الموردين).")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في تحميل بوابات النظام: {e}")

        # 4. تحديث وإنشاء جداول قاعدة البيانات
        # سيقوم بإنشاء الجداول بناءً على الملفات الثلاثة (user, supplier, product)
        db.create_all()
        
        print("🚀 [System] منصة محجوب أونلاين تعمل الآن بالهيكل الموزع.")

    return app
