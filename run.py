# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect

# إنشاء التطبيق
app = create_app()

def auto_fix_database():
    """
    دالة فحص وإصلاح هيكل قاعدة البيانات.
    يتم تنفيذها مرة واحدة فقط عند إقلاع التطبيق لضمان استقراره.
    """
    with app.app_context():
        try:
            print("🔧 جاري فحص هيكل قاعدة البيانات...")
            
            # فحص الأعمدة الموجودة في جدول المحافظ
            inspector = inspect(db.engine)
            # التأكد من أن الجدول موجود فعلاً قبل الفحص
            if 'supplier_wallets' in inspector.get_table_names():
                columns = [c['name'] for c in inspector.get_columns('supplier_wallets')]
                
                # قائمة الأعمدة المشفرة المطلوبة
                required_columns = ['_yer_total', '_sar_total', '_usd_total']
                
                for col in required_columns:
                    if col not in columns:
                        print(f"⚠️ العمود {col} مفقود في جدول supplier_wallets، جاري إضافته...")
                        db.session.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN {col} VARCHAR(255) DEFAULT '0.00'"))
                        db.session.commit()
                        print(f"✅ تم إضافة {col} بنجاح.")
                
                print("🚀 قاعدة البيانات محدثة وجاهزة للعمل.")
            else:
                print("⚠️ تحذير: جدول supplier_wallets غير موجود، سيتم إنشاؤه تلقائياً بواسطة SQLAlchemy.")
            
        except Exception as e:
            print(f"❌ خطأ أثناء التحديث التلقائي: {str(e)}")
            db.session.rollback()

# استدعاء دالة الإصلاح قبل بدء السيرفر
auto_fix_database()

if __name__ == "__main__":
    # الحصول على المنفذ من Railway أو استخدام 5000 كافتراضي
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
