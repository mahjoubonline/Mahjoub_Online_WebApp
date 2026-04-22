import os
from flask import Flask
from config import Config
from core.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    with app.app_context():
        # إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة
        db.create_all()
        print("قاعدة البيانات جاهزة والجداول تم إنشاؤها بنجاح!")

    @app.route('/')
    def index():
        return "<h1>محجوب أونلاين - السيرفر يعمل وقاعدة البيانات متصلة!</h1>"

    return app

app = create_app()

if __name__ == "__main__":
    # الحصول على المنفذ (Port) من رويال أو استخدام 8080 كافتراضي
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
