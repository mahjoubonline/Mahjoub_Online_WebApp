from core import create_app, db
from core.models import User

app = create_app()

with app.app_context():
    print("--- بدء عملية الربط مع قاعدة Render ---")
    # إنشاء الجداول إذا لم تكن موجودة
    db.create_all()
    print("1. تم إنشاء هيكلية الجداول بنجاح.")

    # التأكد من عدم تكرار الحساب
    admin_exists = User.query.filter_by(username='ali_mahjoub').first()
    
    if not admin_exists:
        # إنشاء حساب الأدمن الخاص بك
        new_admin = User(
            username='ali_mahjoub',
            email='ali@mahjoub-online.com',
            role='admin' # تحديد الصفة السيادية للمنصة
        )
        new_admin.set_password('Ali@2026') # كلمة مرور مؤقتة (قم بتغييرها لاحقاً)
        
        db.session.add(new_admin)
        db.session.commit()
        print(f"2. تم إنشاء حساب الأدمن بنجاح: {new_admin.username}")
    else:
        print("2. حساب الأدمن موجود مسبقاً في القاعدة.")

    print("--- انتهت العملية، المنصة الآن جاهزة للتشغيل ---")
