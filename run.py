from core import create_app, db
from flask_migrate import Migrate

# 1. إنشاء نسخة التطبيق من النواة
app = create_app()

# 2. إعداد نظام المهاجرة لربط الجداول (Users, Suppliers, Products)
migrate = Migrate(app, db)

if __name__ == '__main__':
    """
    تشغيل المحرك الرقمي لمنصة محجوب أونلاين.
    يتم التفعيل هنا لضمان عمل كافة الأدوات والروابط.
    """
    # في بيئة التطوير نستخدم debug=True لرصد التغييرات فوراً
    # عند الرفع على Render يتم التحكم في التشغيل عبر Gunicorn
    app.run(debug=True)
