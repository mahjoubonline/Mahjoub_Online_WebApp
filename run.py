# 📂 run.py - الحارس الأمني للتشغيل مع الزراعة التلقائية
import os
import sys
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser

def setup_sovereign_identity():
    """محاولة زراعة المستخدم السيادي تلقائياً"""
    with app.app_context():
        try:
            # اسم المستخدم محجوب بالعربي
            u, p = "محجوب", "123"
            existing = AdminUser.query.filter_by(username=u).first()
            if not existing:
                new_admin = AdminUser(username=u, phone_number="0000000000", role='Owner')
                new_admin.set_password(p)
                db.session.add(new_admin)
                db.session.commit()
                print(f"✅ تم زرع الهوية السيادية: {u}")
            else:
                print(f"ℹ️ الهوية {u} موجودة مسبقاً.")
        except Exception as e:
            print(f"⚠️ فشل الحقن التلقائي (قد لا تكون الجداول جاهزة بعد): {e}")

# إنشاء التطبيق
app = create_app()

# تفعيل الزراعة التلقائية
setup_sovereign_identity()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
