import sys
import os

# إضافة المجلد الحالي للمسارات لضمان رؤية مجلد 'apps'
sys.path.append(os.getcwd())

# استيراد دالة المصنع من المجلد الخاص بك
from apps import create_app

# إنشاء التطبيق (Vercel يحتاج كائن 'app' في هذا الملف)
app = create_app()

# الآن Vercel سيجد كائن 'app' وسيقوم بتشغيل المنصة بنجاح
