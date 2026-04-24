import os
from core import create_app, db

# 1. إنشاء نسخة التطبيق عبر دالة المصنع (Factory Function)
# دالة create_app الآن تحتوي على الـ with app.app_context() الذي يحل مشكلة الـ Blueprint
app = create_app()

# 2. التأكد من اتصال قاعدة بيانات رندر وإنشاء الجداول
with app.app_context():
    try:
        db.create_all()
        print("✅ [Database] Tables are synced with Render DB.")
    except Exception as e:
        print(f"⚠️ [Database] Connection skipped during startup: {e}")

if __name__ == "__main__":
    # 3. جلب المنفذ (Port) من Railway
    port = int(os.environ.get("PORT", 8080))
    
    # 4. تشغيل السيرفر
    # ملاحظة: debug=False ضروري لضمان عدم حدوث استدعاءات مزدوجة تسبب أخطاء في الـ Port
    print(f"🚀 Mahjoub Online is launching on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
