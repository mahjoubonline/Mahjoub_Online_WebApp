from flask import Blueprint

# تعريف الـ Blueprint للقيادة المركزية (محجوب أونلاين)
# تم إعداد المسارات لضمان تحميل القوالب والموارد الثابتة (الأرجواني والذهبي) بكفاءة
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static'
)

# ملاحظة سيادية: يتم استيراد الروابط هنا لمنع "الاستيراد الدائري" (Circular Import)
# هذا يضمن أن جميع الدوال (مثل force_repair وإدارة المحافظ) أصبحت مسجلة ومعرفة لدى التطبيق
try:
    from . import routes
except ImportError as e:
    # تسجيل الخطأ في حال وجود مشكلة في استيراد المسارات لسهولة التصحيح في بيئة الاستضافة
    import logging
    logging.error(f"❌ فشل تحميل مسارات لوحة التحكم: {str(e)}")

# توثيق المكونات النشطة في الـ Blueprint لـ "سوقك الذكي"
# المسارات المتاحة حالياً: 
# - dashboard: لوحة التحكم المركزية
# - manage_suppliers: حوكمة الموردين
# - manage_wallets: إدارة المحافظ السيادية (YER, SAR, USD)
# - withdraw_requests: الهندسة المالية وطلبات السحب
# - force_repair: ترميم قاعدة البيانات والترسانة الرقمية
