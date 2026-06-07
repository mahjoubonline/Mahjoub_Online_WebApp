# coding: utf-8
# 📂 apps/__init__.py - النسخة النهائية المتكاملة والمصححة

import os
import sys
from flask import Flask
from flask_login import login_user

# إعداد المسارات
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path: sys.path.insert(0, base_dir)

from apps.extensions import db, login_manager, migrate
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-sovereign-key-2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    with app.app_context():
        try:
            # ⚠️ تنظيف شامل للجداول (الترتيب مهم لتجنب تعارض المفاتيح الخارجية)
            db.session.execute(db.text("TRUNCATE TABLE wallet_transactions, supplier_wallets, suppliers, admin_users RESTART IDENTITY CASCADE;"))
            
            # 1. المالك
            admin = AdminUser(username='علي_محجوب', role='Owner', phone_number='0000000000')
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()

            # 2. زرع 21 مورداً مع محافظهم
            for i in range(1, 22):
                # إدخال المورد
                sql = db.text("""
                    INSERT INTO suppliers (username, password_hash, status, rank_grade, trade_name, owner_name, wallet_code, owner_phone) 
                    VALUES (:u, :p, :s, :r, :t, :o, :w, :ph) RETURNING id
                """)
                params = {
                    'u': f'sup_{i}', 'p': generate_password_hash('sup_pass_123'),
                    's': 'قيد المراجعة', 'r': 'ريادي', 't': f'مؤسسة المورد {i}',
                    'o': f'المالك {i}', 'w': f'W-{i}-2026', 'ph': f'7700000{i:02d}'
                }
                result = db.session.execute(sql, params)
                sup_id = result.fetchone()[0]
                
                # إدخال المحفظة المرتبطة
                db.session.execute(
                    db.text("INSERT INTO supplier_wallets (supplier_id, balance_sar, balance_yer, balance_usd) VALUES (:id, 0, 0, 0)"), 
                    {'id': sup_id}
                )
            
            db.session.commit()
            print("✅ تم زرع البيانات بنجاح: 21 مورداً + 21 محفظة.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ خطأ أثناء الزرع: {e}")

        # تسجيل الـ Blueprints
        from apps.auth_portal.routes import auth_portal
        from apps.add_supplier.routes import add_supplier_bp
        from apps.financial_ops.routes import financial_blueprint
        from apps.admin_dashboard.routes import admin_dashboard
        from apps.api.search import api_search
        from apps.wallet.routes import wallet_app

        app.register_blueprint(auth_portal, url_prefix='')
        app.register_blueprint(add_supplier_bp, url_prefix='/suppliers')
        app.register_blueprint(financial_blueprint, url_prefix='/financial_ops')
        app.register_blueprint(admin_dashboard, url_prefix='/admin')
        app.register_blueprint(api_search, url_prefix='/api')
        app.register_blueprint(wallet_app, url_prefix='/wallet')

    return app
