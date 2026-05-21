# coding: utf-8
import sys
import traceback
from apps import create_app

# تهيئة التطبيق عبر المصنع المركزي
try:
    app = create_app()
    print("✅ المصنع المركزي للنواة يعمل بنجاح!")
except Exception:
    print("❌ فشل تشغيل المصنع المركزي، التفاصيل أدناه:")
    traceback.print_exc()
    # الخروج بكود 1 يخبر Render أن هناك خطأ في التهيئة
    sys.exit(1)

# هذا الجزء مخصص للتشغيل المحلي فقط (Development)
# عند استخدام gunicorn في الإنتاج، سيتم تجاهل هذا الجزء تلقائياً
if __name__ == "__main__":
    app.run(debug=False)
