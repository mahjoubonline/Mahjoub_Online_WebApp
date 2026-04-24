from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# تهيئة الكائنات الأساسية خارج الدالة لضمان توفرها في كامل النظام
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الملفات
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. إعدادات نظام الحماية وتسجيل الدخول
    login_manager.login_view = 'admin_panel.login'  # المسار الافتراضي
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات هنا لمنع الـ Circular Import (الاستيراد الدائري)
        from core import models
        
        # --- نظام التعرف الذكي على نوع المستخدم ---
        @login_manager.user_loader
        def load_user(user_id):
            # أولاً: البحث في جدول الإدارة (Admin)
            user = models.User.query.get(int(user_id))
            if user:
                return user
            # ثانياً: البحث في جدول الموردين (Supplier)
            return models.Supplier.query.get(int(user_id))

        # --- تسجيل بوابات النظام (Blueprints) مع معالجة الأخطاء ---
        
        try:
            # تسجيل لوحة الإدارة
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # تسجيل بوابة الموردين (شركاء النجاح)
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم ربط جميع البوابات بنجاح (الإدارة + الموردين).")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في تحميل أحد المسارات: {e}")

        # 4. تحديث قاعدة البيانات آلياً (مهم جداً لإضافة حقول المحفظة والأسماء العربية)
        db.create_all()
        
        print("🚀 [System] منصة محجوب أونلاين في وضع الاستعداد التام.")

    return app
