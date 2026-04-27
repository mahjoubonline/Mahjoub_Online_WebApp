from core import create_app

# إنشاء نسخة التطبيق من "العاصمة" core
app = create_app()

if __name__ == '__main__':
    # تشغيل السيرفر
    # ملاحظة: عند الرفع على Railway، السيرفر يستخدم Gunicorn ويقرأ من هذا الملف
    app.run(debug=True)
