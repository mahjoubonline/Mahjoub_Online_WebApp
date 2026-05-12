from flask import Flask, redirect, url_for
import os
from models.admin_db import db, AdminUser  # استدعاء المحرك وموديل المسؤولين

# استيراد البوابات (Blueprints) بناءً على الهيكلية الصحيحة للمجلدات
from apps.admin_dashboard.routes import admin_bp
from apps.auth_portal.routes import auth_bp  # تم التعديل هنا ليطابق مجلد auth_portal
from apps.add_supplier.routes import add_supplier_bp

app = Flask(__name__)

# --- إعدادات الحماية والسيادة ---

# المفتاح السري لتشفير الجلسات ومنع التلاعب
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026_@_PRIVATE'

# إعداد مسار قاعدة البيانات (يدعم Postgres على Railway أو SQLite محلياً)
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- ربط المكونات بالمنظومة ---

db.init_app(app)

# تسجيل البوابات ببادئات واضحة لضمان التنظيم
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(add_supplier_bp, url_prefix='/admin')

@app.route('/')
def root():
    """ توجيه تلقائي لبوابة الدخول لضمان الهوية السيادية للمنصة """
    return redirect(url_for('auth.login'))

# --- تهيئة المنظومة وإنشاء الحساب القيادي ---

def setup_database():
    with app.app_context():
        # إنشاء الجداول تلقائياً في Postgres إذا تم حذفها يدوياً
        db.create_all()
        
        # التأكد من وجود حساب "علي محجوب" بكلمة السر "123"
        check_admin = AdminUser.query.filter_by(username='ali_mahjoub').first()
        if not check_admin:
            founder = AdminUser(
                username='ali_mahjoub',
                full_name='علي محجوب',
                role='founder'
            )
            founder.set_password('123') # تشفير كلمة السر 123
            db.session.add(founder)
            db.session.commit()
            print("🛡️ تم تأمين حساب المؤسس علي محجوب في المنظومة.")

# --- تشغيل المحرك المركزي ---

if __name__ == '__main__':
    setup_database() # تنفيذ تهيئة البيانات والتحقق من الجداول
    
    # ضبط المنفذ ليتوافق مع بيئة Railway السحابية
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
