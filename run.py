from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 1. تهيئة التطبيق
app = create_app()

def prepare_environment():
    """تأمين وجود المجلدات الضرورية في بيئة السيرفر"""
    temp_path = os.path.join('static', 'img', 'temp_uploads')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

if __name__ == '__main__':
    prepare_environment()
    
    # 2. الحصول على المنفذ من نظام التشغيل (ضروري لـ Railway)
    # Railway يمرر رقم المنفذ عبر متغير بيئي اسمه PORT
    port = int(os.environ.get("PORT", 5000))
    
    # 3. تشغيل السيرفر بإعدادات الإنتاج
    # نوقف debug=True عند الرفع النهائي لزيادة الأمان والأداء
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=False
    )
