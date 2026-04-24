from core import create_app, db
from flask import render_template, jsonify
import os

# إنشاء نسخة التطبيق
app = create_app()

# --- [ قسم المسارات الاختبارية والأساسية ] ---

@app.route('/')
def home():
    """الصفحة الرئيسية للمتجر"""
    return "<h1>مرحباً بك في محجوب أونلاين</h1><p>السيرفر يعمل بنجاح!</p>"

@app.route('/test-db')
def test_db():
    """مسار لاختبار الاتصال بقاعدة البيانات"""
    try:
        db.engine.connect()
        return jsonify({"status": "success", "message": "اتصال قاعدة البيانات سليم 100%"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- [ نهاية المسارات ] ---

# كود إنشاء الجداول
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables checked/created successfully.")
    except Exception as e:
        print(f"⚠️ Note: Database connection failed during startup: {e}")

if __name__ == "__main__":
    # الحصول على المنفذ من إعدادات البيئة (مهم جداً لـ Railway)
    port = int(os.environ.get("PORT", 8080))
    # تشغيل التطبيق
    app.run(host='0.0.0.0', port=port)
