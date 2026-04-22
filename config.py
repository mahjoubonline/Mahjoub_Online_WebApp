import os

class Config:
    # سر الأمان للتطبيق
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mahjoub_secret_key_2026')
    
    # رابط قاعدة البيانات (سحبه من المتغيرات التي وضعناها في Railway)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات منصة قمرة
    QUMRA_API_KEY = os.environ.get('QUMRA_API_KEY')
    QUMRA_API_URL = os.environ.get('QUMRA_API_URL')

    # إعدادات لغة التطبيق والتوقيت
    JSON_AS_ASCII = False
