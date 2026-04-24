from core import create_app, db
import os

# 1. إنشاء التطبيق
# دالة create_app هي التي تقوم بربط الـ Blueprints (الإدارة والموردين)
app = create_app()

# 2. التأكد من إنشاء الجداول في قاعدة بيانات Render عند الإقلاع
with app.app_context():
    try:
        db.create_all()
        print("✅ [Database] Connection verified and tables are ready.")
    except Exception as e:
        print(f"⚠️ [Database] Connection issue: {e}")

if __name__ == "__main__":
    # 3. الحصول على المنفذ من بيئة تشغيل Railway
    port = int(os.environ.get("PORT", 8080))
    
    # 4. التشغيل الرسمي للموقع
    # host='0.0.0.0' ضروري جداً ليتمكن الجمهور من دخول الموقع
    print(f"🚀 Mahjoub Online is running on port {port}...")
    
    # نضع debug=False في الرفع الفعلي (Production) لضمان الأمان والسرعة
    app.run(host='0.0.0.0', port=port, debug=False)
