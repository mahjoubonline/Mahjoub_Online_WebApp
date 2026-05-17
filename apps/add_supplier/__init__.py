# apps/add_supplier/__init__.py
# coding: utf-8

from flask import Blueprint

# 1. إنشاء وتثبيت كائن البلوبرينت الموحد لتستطيع المسارات استيراده بدقة
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    url_prefix='/admin/suppliers'
)

# 2. استدعاء ملف الـ routes في الأسفل بعد إنشاء الكائن لقطع التعارض الدائري نهائياً
# هذا السطر يضمن تسجيل كافة مسارات التعميد والفحص اللحظي داخل النظام فور تشغيل الخادم
from apps.add_supplier import routes
