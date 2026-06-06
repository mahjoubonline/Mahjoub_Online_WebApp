# 📂 run.py
import os
from apps import create_app

app = create_app()

def auto_repair_db():
    # التحقق من وجود المتغير الأساسي لقاعدة البيانات
    if not os.environ.get("DATABASE_URL"):
        print("⚠️ GitHub Test Environment Detected: Skipping DB Repair.")
        return
    
    # ... باقي كود الإصلاح الخاص بك ...
