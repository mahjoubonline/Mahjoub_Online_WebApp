import os
from core import create_app, db

# إنشاء التطبيق
app = create_app()

if __name__ == '__main__':
    # الحصول على المنفذ (Port) من نظام التشغيل
    port = int(os.environ.get("PORT", 5000))
    
    # تشغيل السيرفر
    app.run(host='0.0.0.0', port=port, debug=False)
