from flask import Flask, redirect, url_for
import os
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

app = Flask(__name__)

# --- إعدادات السيادة والحماية (مركزية محجوب 2026) ---
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026'

# تصحيح مسار قاعدة البيانات ليتوافق مع Postgres في بيئات الاستضافة
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 1. ربط محرك قاعدة البيانات
db.init_app(app)

# 2. إنشاء الهياكل الرقمية (الجداول) قبل تفعيل المسارات
with app.app_context():
    try:
        db.create_all()
        print("✅ تم تعميد جميع الجداول في منظومة محجوب بنجاح.")
    except Exception as e:
        print(f"⚠️ تنبيه سيادي: تعذر إنشاء الجداول، قد تكون موجودة مسبقاً: {e}")

# 3. تسجيل البوابات (Blueprints) مع ضبط النطاقات لضمان الروابط
try:
    from apps.admin_dashboard.routes import admin_bp
    from apps.auth_portal.routes import auth_bp
    from apps.add_supplier.routes import add_supplier_bp
    
    # بوابة المصادقة
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # بوابة الإدارة المركزية
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # بوابة إضافة الموردين
    # ملاحظة: نستخدم url_prefix='/admin' هنا أيضاً لأننا نريد استدعاؤها بـ 'admin.add_supplier'
    # كما هو موضح في التصميم الأرجواني والذهبي الذي اعتمدناه.
    app.register_blueprint(add_supplier_bp, url_prefix='/admin')
    
    print("🚀 تم تفعيل جميع البوابات الرقمية بنجاح.")
except Exception as e:
    print(f"❌ خطأ حرج في ربط المسارات: {e}")

# المسار الافتراضي (التحويل التلقائي لبوابة الدخول)
@app.route('/')
def root():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # التشغيل على المنفذ المخصص أو الافتراضي 5000
    port = int(os.environ.get('PORT', 5000))
    # التشغيل على 0.0.0.0 ليسمح بالوصول من الشبكة المحلية أو السحابية
    app.run(host='0.0.0.0', port=port, debug=True)
