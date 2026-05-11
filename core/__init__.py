# core/__init__.py
from flask import Flask
from .extensions import db, login_manager 
from .setup import auth_loaders 

def create_app():
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"

    with app.app_context():
        # 1. استيراد الموديلات المطهّرة من النقطة المركزية
        from .models import User, Supplier, SupplierStaff
        
        # 2. بروتوكول تحديث الجداول (PostgreSQL Migration)
        try:
            db.create_all()
            
            # تحديث حقول الموردين (الخزينة الثلاثية والهوية الرقمية)
            supplier_updates = [
                ("email", "VARCHAR(150)"),
                ("identity_image", "VARCHAR(255)"),
                ("balance_yer", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("balance_sar", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("balance_usd", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("sovereign_id", "VARCHAR(100) UNIQUE"),       
                ("tier", "VARCHAR(50) DEFAULT 'مبتدئ'")
            ]
            
            for col_name, col_type in supplier_updates:
                try:
                    db.session.execute(db.text(f"ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                except Exception:
                    pass

            db.session.commit()
            
            # 3. بروتوكول التحقق من "القائد" وتعميد الهوية السيادية
            # حل مشكلة 'Supplier' object has no attribute 'mint_sovereign_id'
            try:
                boss = Supplier.query.filter_by(trade_name="علي محجوب").first()
                if boss and not boss.sovereign_id:
                    boss.generate_sovereign_codes() # الدالة المعتمدة في الموديل
                    db.session.commit()
                    print("✅ تم تعميد الهوية السيادية للقائد بنجاح.")
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ تنبيه أثناء تعميد الهوية: {e}")

            print("✅ تم استكمال الترسانة وتطهير الهيكل بنجاح.")
            
        except Exception as e:
            print(f"⚠️ عطل سيادي في التهيئة: {e}")
            db.session.rollback()

        # 4. تسجيل لوحة التحكم (Admin Blueprint)
        # يتم الاستيراد هنا لتجنب الاستيراد الدائري (Circular Import)
        from admin_panel import admin_bp
        from admin_panel import supplier_service_routes # ضمان تسجيل مسارات الخدمات
        app.register_blueprint(admin_bp) 

    return app
