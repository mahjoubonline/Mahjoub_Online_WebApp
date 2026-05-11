# core/__init__.py
from flask import Flask
from .extensions import db, login_manager 
# استيراد محرك الهوية لضمان التعرف على الجلسات (الموردين والموظفين)
from .setup import auth_loaders 

def create_app():
    # 1. تهيئة التطبيق وتحديد مسارات الواجهة (الترسانة الأم)
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # 2. تحميل الإعدادات السيادية من ملف Config
    app.config.from_object('config.Config')
    
    # 3. ربط المحركات الأساسية (Database & Auth)
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حماية الوصول وبوابة الدخول السيادية
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"
    login_manager.login_message_category = "info"

    with app.app_context():
        # 4. استيراد الموديلات من النقطة المركزية لضمان بناء الجداول
        from .models import User, Supplier, SupplierStaff
        
        # 5. بروتوكول تعميد وتحديث الجداول الشامل (بدون مسح بيانات)
        try:
            # بناء الجداول الجديدة فقط إذا لم تكن موجودة
            db.create_all()
            
            # --- مصفوفة التحديث الجبري للأعمدة المفقودة في PostgreSQL ---
            # تحديث جدول المستخدمين (Users)
            user_updates = [
                ("is_active", "BOOLEAN DEFAULT TRUE"),
                ("email", "VARCHAR(150)"),
                ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                ("role", "VARCHAR(50) DEFAULT 'admin'")
            ]
            
            for col_name, col_type in user_updates:
                try:
                    # إضافة العمود فقط إذا لم يكن موجوداً (للحفاظ على البيانات)
                    db.session.execute(db.text(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                except Exception:
                    pass 

            # تحديث جدول الموردين (Suppliers) ليشمل العملات الثلاث والهيكل الجديد
            supplier_updates = [
                ("email", "VARCHAR(150)"),
                ("identity_image", "VARCHAR(255)"),
                ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                ("identity_type", "VARCHAR(50)"),
                ("balance_yer", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("balance_sar", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("balance_usd", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("sovereign_id", "VARCHAR(100) UNIQUE"),       
                ("tier", "VARCHAR(50) DEFAULT 'مبتدئ'")
            ]
            
            for col_name, col_type in supplier_updates:
                try:
                    # الحماية: لا يتم حذف البيانات، يتم إضافة الأعمدة الناقصة فقط
                    db.session.execute(db.text(f"ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                except Exception:
                    pass

            db.session.commit()
            print("✅ تم استكمال الترسانة وإضافة الأعمدة المفقودة بنجاح.")
            
        except Exception as e:
            print(f"⚠️ تنبيه أثناء تحديث الهيكل: {e}")
            db.session.rollback()

        # 6. بروتوكول معالجة البيانات المفقودة (Data Migration Patch)
        # يقوم بتوليد الأكواد للموردين القدامى دون المساس ببياناتهم الأخرى
        try:
            missing_codes = Supplier.query.filter(Supplier.sovereign_id == None).all()
            for s in missing_codes:
                s.generate_sovereign_codes() 
            db.session.commit()
        except:
            db.session.rollback()

        # 7. تسجيل لوحة تحكم الإدارة (Blueprint)
        try:
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp) 
            print("✅ تم تسجيل لوحة التحكم بنجاح تحت مسار /admin")
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل لوحة التحكم: {e}")

    return app
