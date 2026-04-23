import os

class Config:
    # 1. جلب الرابط من متغيرات بيئة رويال (Railway)
    # نستخدم get للحصول على الرابط أو None إذا لم يكن موجوداً
    database_url = os.environ.get('DATABASE_URL')
    
    # 2. التصحيح الذكي للرابط (Critical Fix)
    # هذا الجزء يحل مشكلة الانهيار بسبب اختلاف تسمية البروتوكول
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # 3. إسناد الرابط المصحح للمحرك
    SQLALCHEMY_DATABASE_URI = database_url
    
    # 4. إعدادات إضافية لضمان استقرار الأداء
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 5. مفاتيح الأمان وقمرة (تأكد أن الأسماء تطابق ما في صورة رويال)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mahjoub_online_2026_secret')
    QUMRA_API_URL = os.environ.get('QUMRA_API_URL')
    QUMRA_API_KEY = os.environ.get('QUMRA_API_KEY')
