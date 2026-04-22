import os
from flask import Flask
from admin_panel.models import db, User
from admin_panel.admin_routes import admin_bp
from flask_login import LoginManager

app = Flask(__name__)

# 1. إعدادات الأمان وقاعدة البيانات
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_secret_key_2026')

# رابط قاعدة البيانات من Render (تأكد أن الرابط يبدأ بـ postgresql:// وليس postgres://)
uri = "رابط_القاعدة_الذي_أرسلته_هنا" 
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. ربط قاعدة البيانات
db.init_app(app)

# 3. نظام إدارة الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 4. تسجيل الـ Blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

# 5. تهيئة الجداول والمستخدم الأول
with app.app_context():
    try:
        db.create_all()
        # إضافة القائد علي محجوب إذا لم يكن موجوداً
        admin_user = User.query.filter_by(username='علي محجوب').first()
        if not admin_user:
            new_admin = User(username='علي محجوب', role='SuperAdmin')
            new_admin.set_password('ضع_كلمة_مرورك_هنا') # غيرها لكلمة سر قوية
            db.session.add(new_admin)
            db.session.commit()
            print("✅ تم ربط القاعدة بنجاح وإنشاء حساب القائد.")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == '__main__':
    # Render يطلب المنفذ 8080 غالباً
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
