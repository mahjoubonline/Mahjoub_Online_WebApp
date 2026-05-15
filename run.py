# coding: utf-8
# 🚀 محرك الإقلاع السيادي لمنصة محجوب أونلاين 2026
# التوثيق: هذا الملف هو المسؤول عن تشغيل التطبيق وربطه بخوادم Railway

import os
import sys

# 1. تأمين المسارات (Environment Setup)
# إضافة المجلد الحالي إلى مسار النظام لضمان استيراد حزمة apps بدون أخطاء
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from apps import create_app, db
except ImportError as e:
    print(f"❌ خطأ حرج: تعذر العثور على حزمة 'apps'. تأكد من وجود ملف __init__.py داخل المجلد. التفاصيل: {e}")
    sys.exit(1)

# 2. إنشاء نسخة التطبيق
app = create_app()

if __name__ == "__main__":
    # 3. إعدادات المنفذ (Port Configuration)
    # Railway يمرر رقم المنفذ ديناميكياً عبر متغير البيئة PORT
    # استخدامه ضروري جداً لكي لا يظهر السيرفر بوضع "النائم"
    port = int(os.environ.get("PORT", 5000))
    
    print(f"📡 جاري تشغيل المحرك على المنفذ: {port}")
    
    try:
        # تشغيل السيرفر مع إتاحة الوصول الخارجي (0.0.0.0)
        # ملاحظة: debug=False في بيئة الإنتاج لضمان استقرار النظام
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=False,
            threaded=True # تفعيل تعدد المسارات لمنع تجمد السيرفر عند الطلبات المتزامنة
        )
    except Exception as e:
        print(f"⚠️ حدث خطأ أثناء محاولة إقلاع السيرفر: {e}")
