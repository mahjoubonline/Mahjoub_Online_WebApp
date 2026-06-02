# coding: utf-8
# 🚀 كود غرس مؤقت لتنظيف كاش السيرفر وقراءة الملف الحالي
import os
import shutil

print("🧹 [START] بدء تنظيف ملفات الكاش المؤقتة (__pycache__)...")
for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__':
            path = os.path.join(root, d)
            try:
                shutil.rmtree(path)
                print(f"✅ تم حذف الكاش بنجاح: {path}")
            except Exception as e:
                print(f"❌ تعذر حذف {path}: {e}")

print("🔍 [CHECK] طباعة الأسطر الأولى من wallet_db.py للتأكد من تحديثه في السيرفر:")
try:
    with open("apps/models/wallet_db.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
        print("================== محتوى أعلى الملف الحالي ==================")
        for line in lines[:15]:  # طباعة أول 15 سطر فقط
            print(line.rstrip())
        print("==========================================================")
except Exception as e:
    print(f"❌ فشل قراءة ملف المحفظة: {e}")

# ------------------------------------------------------------------
# 🟢 الآن يبدأ كود تشغيل Flask الطبيعي بعد التنظيف
# ------------------------------------------------------------------
from apps import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
