# run.py
# الملف الرئيسي لتشغيل محرك منصة محجوب أونلاين
from core import create_app

# بناء التطبيق باستخدام المصنع (Factory Pattern)
app = create_app()

if __name__ == "__main__":
    # تشغيل السيرفر محلياً للتجارب (على Railway يتم استخدام Gunicorn)
    app.run(host='0.0.0.0', port=8080)
