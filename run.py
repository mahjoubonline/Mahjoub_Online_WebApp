# run.py
import os
from apps import create_app

# إنشاء التطبيق باستخدام المصنع (Factory Pattern)
app = create_app()

if __name__ == "__main__":
    # تشغيل التطبيق (في الإنتاج Gunicorn يتجاهل هذا الجزء)
    app.run()
