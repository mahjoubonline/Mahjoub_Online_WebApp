# 📂 apps/statement/__init__.py

from flask import Blueprint

# تعريف البلوبرينت الخاص بكشوفات الحساب
statement_bp = Blueprint('statement', __name__, template_folder='templates')

# استيراد المسارات لتفعيلها
from apps.statement import routes

def register_statement(app):
    """تسجيل بلوبرينت كشوفات الحساب بشكل آمن"""
    try:
        app.register_blueprint(statement_bp, url_prefix='/statement')
        print("✅ تم تسجيل بلوبرينت كشوفات الحساب (Statement) بنجاح.")
    except Exception as e:
        print(f"❌ فشل تسجيل بلوبرينت كشوفات الحساب: {e}")
