# coding: utf-8
# 🚀 ملف إقلاع التطبيق الرسمي - منصة محجوب أونلاين

from apps import create_app

# إنشاء التطبيق باستخدام الـ Factory Pattern
app = create_app()

if __name__ == "__main__":
    # هذا السطر يعمل فقط عند التشغيل المحلي على جهازك
    # Render يتجاهل هذا الجزء ويستخدم Gunicorn مباشرة
    app.run(host="0.0.0.0", port=5000, debug=True)
