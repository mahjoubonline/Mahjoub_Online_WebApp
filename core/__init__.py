from core import create_app, db
import os

# إنشاء نسخة التطبيق
app = create_app()

# كود اختياري: إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables checked/created successfully.")
    except Exception as e:
        print(f"⚠️ Note: Database connection failed during startup: {e}")

if __name__ == "__main__":
    # الحصول على المنفذ من إعدادات البيئة (مهم لـ Railway)
    port = int(os.environ.get("PORT", 8080))
    # تشغيل التطبيق محلياً للتجربة
    app.run(host='0.0.0.0', port=port)
