from core import create_app, db
import os

# 1. إنشاء نسخة التطبيق من دالة المصنع
app = create_app()

# 2. التأكد من وجود الجداول عند الإقلاع (اختياري ولكن مفيد في رندر)
with app.app_context():
    try:
        # هذا الأمر لن يمسح البيانات القديمة، سيفقط ينشئ الجداول الناقصة
        db.create_all()
        print("✅ Database connection verified and tables are ready.")
    except Exception as e:
        print(f"⚠️ Startup Note: Could not connect to database or create tables: {e}")

if __name__ == "__main__":
    # 3. الحصول على المنفذ من المتغيرات البيئية (ضروري جداً لـ Railway)
    # القيمة الافتراضية 8080 هي المعتمدة في أغلب إعداداتك
    port = int(os.environ.get("PORT", 8080))
    
    # 4. تشغيل التطبيق
    # host='0.0.0.0' تسمح باستقبال الاتصالات الخارجية من الويب
    app.run(host='0.0.0.0', port=port, debug=False)س
