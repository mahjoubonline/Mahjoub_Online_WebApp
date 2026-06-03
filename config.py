# coding: utf-8
# ⚙️ مهندس الإعدادات المركزية السحابية - منصة محجوب أونلاين 2026

import os

class Config:
    # 🛡️ مفتاح الأمان السيادي للمنصة (يُجلب من متغيرات البيئة في Render)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SOVEREIGN_KEY_2026')
    
    # 1. جلب رابط قاعدة البيانات السحابية (Neon / Postgres)
    _db_url = os.environ.get('DATABASE_URL')
    
    # 2. ⚡ إصلاح بادئة الرابط تلقائياً لتتوافق مع معايير SQLAlchemy الحديثة ومحرك Psycopg2
    # هذا التعديل يضمن قبول الرابط سواءً بدأ بـ postgres أو postgresql وتحويله للمحرك الآمن فوراً
    if _db_url:
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif _db_url.startswith("postgresql://"):
            _db_url = _db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    # 3. إسناد الرابط المصحح أو الاعتماد على SQLite كخيار احتياطي للمطور محلياً
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///mahjoub_online.db'
    
    # 4. ❌ تعطيل تتبع التعديلات (لإلغاء العمليات الإضافية وتحسين الأداء الاقتصادي للسيرفر)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 5. 💎 حوكمة وإدارة الاتصالات لبيئة Render المستقرة
    # تم ضبط الخواص لضمان استمرارية الاتصال وتفادي أخطاء المهلة (Timeouts) مع الـ Pooling في Neon
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 15,             # الحد الأقصى للاتصالات المتزامنة المفتوحة
        "max_overflow": 10,          # اتصالات إضافية مؤقتة عند الضغط العالي
        "pool_timeout": 30,          # عدد الثواني للانتظار قبل إطلاق استثناء الفشل
        "pool_recycle": 1800,        # إعادة تدوير الاتصال كل 30 دقيقة لمنع موته من طرف الخادم
        "pool_pre_ping": True        # فحص سلامة القناة قبل إرسال أي استعلام لضمان عدم حدوث Crash
    }
    
    # 6. إعدادات البنية التحتية السحابية (Qomra Cloud API)
    QUMRA_API_KEY = os.environ.get('QUMRA_API_KEY')
    QUMRA_API_URL = os.environ.get('QUMRA_API_URL')

    # 7. الحفاظ على ترميز ونقاء النصوص والبيانات باللغة العربية
    JSON_AS_ASCII = False
