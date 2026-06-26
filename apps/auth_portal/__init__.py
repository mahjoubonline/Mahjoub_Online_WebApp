# coding: utf-8
# 📂 apps/auth_portal/__init__.py

# هذا الملف يجعل مجلد 'auth_portal' حزمة (Package) بايثون.
# لا نضع هنا منطقاً معقداً لتجنب "الاستيراد الدائري" (Circular Imports).
# كل التسجيل يتم عبر registry.py في نفس المجلد.

from .routes import auth_portal

__all__ = ['auth_portal']
