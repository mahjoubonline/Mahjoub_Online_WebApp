# run.py
# المحرك التشغيلي لمنصة محجوب أونلاين - إصدار التطهير السيادي
import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

# بناء التطبيق بناءً على الإعدادات المركزية
app = create_app()

def initialize_sovereign_system():
    """تطهير شامل وإعادة بناء الترسانة الرقمية"""
    with app.app_context():
        try:
            print("🚨 جاري بدء عملية التطهير الشامل لقاعدة البيانات...")
            
            # 1. قطع العلاقات ومسح الجداول بالقوة (CASCADE)
            # هذا الأمر يجبر PostgreSQL على حذف الجداول حتى لو كانت مرتبطة ببيانات أخرى
            db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
            db.session.execute(text('DROP TABLE IF EXISTS "suppliers" CASCADE;'))
            db.session.execute(text('DROP TABLE IF EXISTS "orders" CASCADE;'))
            db.session.commit()
            print("🧹 تم مسح الجداول القديمة بنجاح.")

            # 2. بناء الجداول بالهيكلية الجديدة (بما في ذلك role و is_active_account)
            db.create_all()
            print("🛠️ تم إعادة بناء الترسانة الرقمية بالمعايير الجديدة.")

            # 3. زرع حساب القائد (علي محجوب)
            # نتحقق أولاً للتأكد (رغم أن المسح يضمن عدم وجوده)
            if not User.query.filter_by(username="علي محجوب").first():
                admin = User(
                    username="علي محجوب",
                    role='admin',
                    is_active_account=True
                )
                admin.set_password('123') # كلمة المرور الافتراضية
                db.session.add(admin)
                db.session.commit()
                
                print(f"👑 تم إرساء سلطة القائد: {admin.username}")
                print(f"🛡️ الرتبة: {admin.role} | الحالة: نشط")

        except Exception as e:
            db.session.rollback()
            print(f"❌ فشل حرج في تهيئة المنظومة: {e}")
            # لا نوقف التطبيق لكي نتمكن من رؤية الأخطاء في سجلات Railway
            raise e

if __name__ == "__main__":
    # تشغيل التهيئة عند إقلاع الحاوية في Railway
    initialize_sovereign_system()

    # جلب المنفذ من البيئة المحيطة (Railway يخصص PORT تلقائياً)
    port = int(os.environ.get("PORT", 8080))
    
    print(f"🚀 المحرك الرقمي يعمل الآن على المنفذ: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
