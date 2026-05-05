# config.py
import os

class Config:
    # --- إعدادات قاعدة البيانات (Database Configuration) ---
    # الأولوية دائماً لمتغيرات البيئة في Railway لضمان الاتصال السحابي
    uri = os.environ.get('DATABASE_URL')
    
    # إذا لم يجد DATABASE_URL (أثناء التطوير المحلي)، استخدم الرابط الاحتياطي
    if not uri:
        uri = 'postgresql://mahjoub_online_1_db_user:S7dxtVGcKwrsM1QEzGOuPPcRL8dKxgXk@dpg-d79tuthr0fns73epej4g-a.oregon-postgres.render.com/mahjoub_online_1_db'
    
    # معالجة اختلاف تسمية البروتوكول (خاصة عند التحويل من Heroku/Render إلى Railway)
    # SQLAlchemy يتطلب 'postgresql://' بدلاً من 'postgres://'
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- إعدادات الأمان والجلسات ---
    # سر الأمان السيادي لـ محجوب أونلاين
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ali_Mahjoub_High_Energy_2026'

    # --- إعدادات الأرشفة والاتصال بـ GitHub (Sovereign Assets) ---
    # يتم سحب هذه القيم من إعدادات (Variables) في مشروع Railway الخاص بك
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') 
    GITHUB_REPO = os.environ.get('GITHUB_REPO')
    
    # القيم الاحتياطية في حال لم تكن المتغيرات مهيأة في السيرفر بعد
    if not GITHUB_TOKEN:
        GITHUB_TOKEN = "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"
    
    if not GITHUB_REPO:
        GITHUB_REPO = "alimohm/Mahjoub-Sovereign-Assets"
    
    # مسار المجلد الرئيسي للأرشفة الرقمية
    GITHUB_MAIN_PATH = "Main_Archive"

    # --- إعدادات إضافية للإنتاج (Production Settings) ---
    # لضمان عدم حدوث مهلة زمنية (Timeout) في العمليات الكبيرة
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
