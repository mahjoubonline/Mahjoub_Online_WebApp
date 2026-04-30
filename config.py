import os

class Config:
    # جلب الرابط من البيئة (Render) أو استخدام الرابط المباشر الذي قدمته
    # ملاحظة: Render أحياناً يرسل الرابط بـ postgres:// ويجب تحويله لـ postgresql://
    uri = os.environ.get('DATABASE_URL') or 'postgresql://mahjoub_online_1_db_user:S7dxtVGcKwrsM1QEzGOuPPcRL8dKxgXk@dpg-d79tuthr0fns73epej4g-a.oregon-postgres.render.com/mahjoub_online_1_db'
    
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ali_Mahjoub_High_Energy_2026'
