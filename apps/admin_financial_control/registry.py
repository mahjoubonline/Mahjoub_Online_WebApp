# 📂 apps/admin_platform_treasury/registry.py
from .routes import treasury_bp
# استورد موديول المحفظة هنا لكي تستطيع الإشارة لروابطه
from apps.wallet.routes import wallet_bp 

MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

LINKS = {
    "treasury_bp.dashboard": "كشف حساب المنصة",
    "wallet_bp.wallet_view": "محفظة الموردين" # قم بتعديل هذا الاسم حسب الـ endpoint الحقيقي
}

def register_module(app):
    try:
        app.register_blueprint(treasury_bp, url_prefix='/treasury')
        # لا داعي لتسجيل الـ blueprint هنا مرة أخرى إذا كنت تسجله في ملفه الخاص
        print("✅ [Registry]: تم تسجيل موديول 'الرقابة المالية' ودمج روابط المحفظة.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل التسجيل: {e}")
