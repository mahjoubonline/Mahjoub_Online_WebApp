from flask import Blueprint

# هذا الملف يعمل كجسر يربط المسارات (routes) بالهيكل التنظيمي
# استيراد البلوبرنت الذي عرفناه في ملف routes
from .routes import supplier_bp

# لا نحتاج لكتابة أكواد إضافية هنا لضمان خفة الملف وعدم التكرار
