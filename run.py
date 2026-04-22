from flask import Flask
from core.models import db
import os

def create_app():
    app = Flask(__name__)
    
    # إعدادات قاعدة البيانات (محلياً سنستخدم SQLite لسهولة البدء)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mahjoub_online.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mahjoub_secret_key_2026'

    db.init_app(app)

    # تسجيل المسارات (Routes) - سنفعلها غداً بالتفصيل
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('admin/login.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() # إنشاء الجداول تلقائياً عند التشغيل
        print("✅ تم إنشاء قاعدة البيانات بنجاح!")
    
    app.run(debug=True, port=5000)
