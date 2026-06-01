# coding: utf-8
# 🚀 الجسر السحابي: نقطة الانطلاق الموحدة لـ Vercel - منصة محجوب أونلاين 2026

import sys
import os

# إضافة المجلد الرئيسي للمشروع إلى مسارات النظام
# هذا يضمن أن يتمكن Vercel من الوصول إلى مجلد "apps"
# وتفعيل Factory Pattern بنجاح
sys.path.append(os.getcwd())

# استيراد تطبيق Flask من ملف run.py
# (حيث قمت بتعريف app = create_app())
from run import app

# Vercel يبحث عن كائن "app" في هذا الملف ليقوم بتشغيله كدالة سحابية
# لا تقم بإضافة app.run() هنا
