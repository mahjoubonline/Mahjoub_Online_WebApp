from flask import Flask, redirect, url_for
import os
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

def create_app():
    app = Flask(__name__)

    # --- إعدادات الحماية والسيادة ---
    app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026'

    # إصلاح رابط قاعدة البيانات للبيئات السحابية (PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 1. ربط قاعدة البيانات
    db.init_app(app)

    # 2. تسجيل البوابات الرقمية (Blueprints)
    # ملاحظة: استيراد داخل الدالة لتجنب التكرار (Circular Import)
    try:
        from apps.auth_portal.routes import auth_bp
        from apps.admin_dashboard.routes import admin_bp
        from apps.add_supplier.routes import add_supplier_bp

        # تسجيل بوابة التحقق ببادئة /auth ليتطابق مع الرابط في صورتك
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
        # تسجيل لوحة التحكم والموردين
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(add_supplier_bp, url_prefix='/admin/supplier')

    except Exception as e:
        print(f"❌ خطأ في ربط المسارات الرقمية: {e}")

    # 3. إنشاء الجداول عند التشغيل الأول
    with app.app_context():
        try:
            db.create_all()
            print("✅ تم تعميد الجداول بنجاح في منظومة محجوب.")
        except Exception as e:
            print(f"⚠️ تنبيه قاعدة البيانات: {e}")

    # 4. التوجيه الرئيسي
    @app.route('/')
    def root():
        return redirect(url_for('auth.login')) # تأكد أن اسم الـ Blueprint هو 'auth'

    return app

# --- محرك التشغيل ---
app = create_app()

if __name__ == '__main__':
    # جلب المنفذ من Railway (غالباً 8080 أو متغير حسب البيئة)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
