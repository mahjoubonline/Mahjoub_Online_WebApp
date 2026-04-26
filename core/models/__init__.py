# --- الترسانة الهيكلية لمحجوب أونلاين ---
# الموقع: core/models/__init__.py

try:
    # الاستيراد النسبي لضمان استقرار الهيكل داخل حزمة core
    from core.models.user import User
    from core.models.supplier import Supplier
    from core.models.product import Product

    # رسالة تأكيد تظهر في سجلات التشغيل للتأكد من سلامة الترسانة
    print("✅ [Models] تم تعميد الموديلات السيادية (User, Supplier, Product) بنجاح.")

except ImportError as e:
    # في حال حدوث خطأ، سيتم طباعته بدقة لتسهيل المعالجة الفنية
    print(f"⚠️ [Critical Error] فشل في ربط الموديلات بالترسانة: {e}")

# تصدير الموديلات لتمكين استدعائها المباشر من db.create_all()
__all__ = ['User', 'Supplier', 'Product']
