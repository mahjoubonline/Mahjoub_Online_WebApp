# 📂 apps/admin_dashboard/__init__.py

# هذا الملف يجعل مجلد 'admin_dashboard' حزمة (Package) في Python.
# عادةً لا نحتاج لكتابة الكثير هنا، ولكن إذا كنت ترغب في استيراد المسارات 
# ليتم الوصول إليها مباشرة من 'apps.admin_dashboard'، يمكنك فعل ذلك هنا:

from .routes import admin_dashboard

# هذا يضمن أن عند استيراد التطبيق، يتم التعرف على الـ Blueprint تلقائياً
__all__ = ['admin_dashboard']
