LINKS = {
    "treasury_bp.dashboard": "الخزينة المركزية", # تأكد أن هذا هو اسم الـ endpoint في routes.py الخاص بالخزينة
    # ... بقية الروابط
}# 📂 apps/admin_financial_control/registry.py

MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-shield-alt"

# هنا نضع كل الروابط التي ستظهر عند الضغط على "الرقابة المالية"
LINKS = {
    "treasury_bp.dashboard": "الخزينة المركزية",
    "wallet_app.dashboard": "محفظة الموردين",
    "admin_exchange.manage_rates": "أسعار الصرف"
}

def register_module(app):
    # إذا كان هذا الموديول يحتاج لتسجيل Blueprint خاص به، أضفه هنا.
    # إذا كان مجرد "قائمة تجميعية" لروابط موديولات أخرى، اترك دالة التسجيل فارغة.
    print("✅ [Registry]: تم تسجيل موديول 'الرقابة المالية' كقائمة منسدلة بنجاح.")
