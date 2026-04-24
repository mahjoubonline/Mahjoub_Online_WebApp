from core import create_app, db
import os

# 1. إنشاء نسخة التطبيق من دالة المصنع (Factory Function)
# تأكد أن دالة create_app تقوم بتسجيل admin_bp في ملف core/__init__.py
app = create_app()

# 2. التأكد من وجود الجداول عند الإقلاع
# هذه الخطوة حاسمة لضمان أن قاعدة بيانات Render جاهزة لاستقبال البيانات
with app.app_context():
    try:
        # الأمر db.create_all() ينشئ الجداول (Products, Suppliers, etc.) إذا لم تكن موجودة
        db.create_all()
        print("✅ Database connection verified and tables are ready.")
    except Exception as e:
        # في حال وجود خطأ في DATABASE_URL سيظهر هنا في السجلات
        print(f"⚠️ Startup Note: Could not connect to database or create tables: {e}")

if __name__ == "__main__":
    # 3. الحصول على المنفذ (Port) من المتغيرات البيئية لـ Railway
    # إذا لم يجد Railway المنفذ، سيستخدم 8080 كافتراضي
    port = int(os.environ.get("PORT", 8080))
    
    # 4. تشغيل التطبيق في وضع الإنتاج
    # host='0.0.0.0' ضروري جداً لكي يظهر الموقع على الإنترنت
    # debug=False يُفضل استخدامه عند الرفع الفعلي لضمان استقرار السيرفر
    print(f"🚀 Mahjoub Online is starting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
