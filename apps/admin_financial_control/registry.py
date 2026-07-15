# 📂 apps/admin_financial_control/registry.py

MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-shield-alt"

# التصحيح: المسار البرمجي هو المفتاح، والاسم العربي هو القيمة
LINKS = {
    "treasury_bp.dashboard": "الخزينة المركزية",
    "wallet_app.dashboard": "محفظة الموردين",
    "admin_exchange.manage_rates": "أسعار الصرف"
}

def register_module(app):
    # إذا كنت تسجل Blueprints هنا، تأكد من إضافتها. 
    # إذا كان هذا الموديول مجرد "حاوية" لروابط موديولات أخرى، فالكود أعلاه يكفي.
    print("✅ [Registry]: تم تسجيل موديول 'الرقابة المالية' بنجاح.")
