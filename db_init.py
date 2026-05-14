# coding: utf-8
# يتم وضعه في المجلد الرئيسي بجانب run.py
from run import app  
from models.admin_db import db
from models.supplier_db import Supplier

def initialize_suppliers_table():
    """
    عملية مزامنة قاعدة البيانات لتعميد جدول الموردين في محجوب أونلاين
    """
    with app.app_context():
        print("⚙️ جاري بدء عملية المزامنة السيادية...")
        try:
            # create_all ستنشئ الجدول suppliers فقط لأنه غير موجود حالياً
            db.create_all()
            print("✅ تم بنجاح: إنشاء جدول الموردين (suppliers).")
            print("📦 الحقول الجديدة: identity_image, sovereign_id أصبحت نشطة الآن.")
        except Exception as e:
            print(f"❌ خطأ فني أثناء التحديث: {str(e)}")

if __name__ == "__main__":
    initialize_suppliers_table()
