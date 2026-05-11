# core/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect  # 🛡️ درع الحماية السيادي
from .extensions import db, login_manager 
from .setup import auth_loaders 

# تهيئة درع الحماية عالمياً لمنع هجمات التزييف
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # تحميل الإعدادات المركزية
    app.config.from_object('config.Config')
    
    # --- تفعيل الترسانة الرقمية والخدمات المركزية ---
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) 
    
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"

    with app.app_context():
        # 1. استيراد الموديلات لضمان وعي المحرك بها
        from .models import User, Supplier, SupplierStaff
        
        # 2. بروتوكول التحديث التلقائي للهيكل (Auto-Migration)
        try:
            db.create_all()
            
            # قائمة التحديثات لضمان توافق قاعدة البيانات مع الكود الجديد
            db_updates = [
                ("suppliers", "email", "VARCHAR(150)"),
                ("suppliers", "identity_image", "VARCHAR(255)"),
                ("suppliers", "balance_yer", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("suppliers", "balance_sar", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("suppliers", "balance_usd", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("suppliers", "sovereign_id", "VARCHAR(100) UNIQUE"),       
                ("suppliers", "tier", "VARCHAR(50) DEFAULT 'مبتدئ'"),
                ("users", "full_name", "VARCHAR(150)"),
                ("users", "permissions", "TEXT DEFAULT '{}'"),
                ("users", "role", "VARCHAR(50) DEFAULT 'admin'"),
                ("users", "last_ip", "VARCHAR(45)")
            ]
            
            for table, col_name, col_type in db_updates:
                try:
                    db.session.execute(db.text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                except Exception:
                    pass 

            db.session.commit()
            
            # --- 3. بروتوكول الترقية السيادية للقائد (حل مشكلة رفض الدخول) ---
            try:
                # البحث عن حسابك بالاسم المحدد وتحديث بياناته
                commander = User.query.filter_by(username='علي محجوب').first()
                
                if commander:
                    commander.role = 'admin'  # منح رتبة القيادة
                    commander.set_password('123')  # تثبيت كلمة المرور
                    db.session.commit()
                    print(f"👑 تم تعميد القائد {commander.username} بالصلاحيات الكاملة.")
                else:
                    # في حال لم يكن الحساب موجوداً، نقوم بإنشائه فوراً
                    new_boss = User(username='علي محجوب', role='admin', full_name='علي محجوب')
                    new_boss.set_password('123')
                    db.session.add(new_boss)
                    db.session.commit()
                    print("✨ تم إنشاء حساب القائد علي محجوب لأول مرة بالصلاحيات السيادية.")
                
                # تعميد الهوية السيادية في جدول الموردين
                boss_supplier = Supplier.query.filter_by(trade_name="علي محجوب").first()
                if boss_supplier and not boss_supplier.sovereign_id:
                    boss_supplier.generate_sovereign_codes() 
                    db.session.commit()
                    print("✅ تم تعميد الهوية السيادية للمورد بنجاح.")
                    
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ تنبيه أثناء الترقية السيادية: {e}")

            print("✅ تم استكمال الترسانة وتطهير الهيكل بنجاح.")
            
        except Exception as e:
            print(f"⚠️ عطل في التهيئة: {e}")
            db.session.rollback()

        # 4. تسجيل البلوبرنتات والروابط
        from admin_panel import admin_bp
        from admin_panel import supplier_service_routes 
        from admin_panel import staff_routes
        
        app.register_blueprint(admin_bp) 

    return app
