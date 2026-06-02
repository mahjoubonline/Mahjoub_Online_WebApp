# 📂 run.py
from apps import create_app
import traceback
import sys

try:
    app = create_app()
    print("✅ تطبيق محجوب أونلاين تم تحميله بنجاح!")
except Exception as e:
    print("❌ كارثة عند الإقلاع:")
    traceback.print_exc()
    # نخرج بكود خطأ بعد طباعة التفاصيل ليراها المبرمج في سجلات Render
    sys.exit(1)
