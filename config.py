import os

class Config:
    # --- إعدادات قاعدة البيانات (PostgreSQL on Render) ---
    # جلب الرابط من البيئة (Render) أو استخدام الرابط المباشر
    uri = os.environ.get('DATABASE_URL') or 'postgresql://mahjoub_online_1_db_user:S7dxtVGcKwrsM1QEzGOuPPcRL8dKxgXk@dpg-d79tuthr0fns73epej4g-a.oregon-postgres.render.com/mahjoub_online_1_db'
    
    # معالجة اختلاف تسمية البروتوكول في Render
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- إعدادات الأمان والجلسات ---
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ali_Mahjoub_High_Energy_2026'

    # --- إعدادات الأرشفة السيادية (GitHub Sovereign Assets) ---
    # تم ربط المفاتيح الخاصة بمستودع Mahjoub-Sovereign-Assets
    GITHUB_TOKEN = "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"
    GITHUB_REPO = "alimohm/Mahjoub-Sovereign-Assets"
    
    # مسار المجلد الرئيسي للأرشفة داخل المستودع
    GITHUB_MAIN_PATH = "Main_Archive"
