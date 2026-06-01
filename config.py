# config.py
# coding: utf-8
# ⚙️ مهندس الإعدادات المركزية - منصة محجوب أونلاين 2026

import os

class Config:
    # مفتاح الأمان السيادي للمنصة
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SOVEREIGN_KEY_2026')
    
    # 1. جلب رابط قاعدة البيانات
    db_url = os.environ.get('DATABASE_URL')
    
    # 2. 🛡️ إصلاح بادئة الرابط ليتوافق مع SQLAlchemy الحديثة
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    # 3. إسناد الرابط المصحح
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///mahjoub_fallback.db'
    
    # إيقاف تتبع التعديلات لرفع الأداء
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 🌐 هندسة النطاقات الذكية لمنع تعارض الـ 404 على سيرفرات Vercel
    # إذا كان التطبيق يعمل على سيرفر Vercel الفعلي، نقوم بضبط SERVER_NAME
    # ولكن إذا طلب المستخدم رابط الفحص الافتراضي لـ Vercel، يتم تصفير الإعداد تلقائياً لتفادي الانهيار
    VERCEL_URL = os.environ.get('VERCEL_URL', '')
    
    if VERCEL_URL and not VERCEL_URL.startswith('mahjoub.online'):
        # إذا كان الرابط هو الرابط الافتراضي لـ Vercel المخصص للفحص، نلغي قيود الحظر ليعمل معك فوراً
        SERVER_NAME = None
    else:
        # عند الدخول من النطاق الرسمي المستقل لـ "سوقك الذكي"
        SERVER_NAME = os.environ.get('SERVER_NAME', 'mahjoub.online')
