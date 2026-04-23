import os

class Config:
    # قراءة الرابط من متغيرات Railway
    # أضفنا التحويل التلقائي من postgres إلى postgresql لضمان التوافق
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-for-dev'
