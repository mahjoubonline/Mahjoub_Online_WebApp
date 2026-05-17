# coding: utf-8
# 🛡️ وحدة تهيئة لوحة التحكم - محجوب أونلاين 2026

from flask import Blueprint
import os
import logging

# 1. تحديد المسارات المطلقة لضمان الاستقرار في بيئة Linux (Railway)
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء البلوبرينت المركزي للوحة التحكم
# تم تثبيت الاسم والامتثال للمصنع المركزي في النواة لمنع التعارض الدائري
admin_dashboard_blueprint = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder=template_path
)

# 3. استيراد المسارات (Routes) بشكل متأخر وآمن لحماية العزل التام
try:
    from . import routes
    logging.info("✅ تم ربط محرك لوحة التحكم بنجاح وعمّدت المسارات.")
except ImportError as e:
    logging.error(f"⚠️ خطأ حرج: تعذر تحميل مسارات لوحة التحكم داخلياً: {str(e)}")
