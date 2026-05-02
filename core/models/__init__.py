# core/models/__init__.py

# 1. استيراد كائن قاعدة البيانات المركزي
from core import db

# 2. استيراد موديل القائد (المستخدم) - يجب أن يظل الأول دائماً
# هذا يضمن وجود جدول 'user' في الذاكرة قبل ربط أي جداول تجارية به
from .user import User

# 3. استيراد الموديلات التجارية (الموردين والطلبات)
# الترتيب هنا يضمن بناء "الترسانة" دون أخطاء Foreign Key
try:
    from .business import Supplier, Order
except ImportError:
    # في حال لم يتم رفع ملف business.py بعد، سيتم تنبيهك في السجلات
    Supplier = None
    Order = None

# 4. تعريف المكونات المتاحة للاستخدام في النظام
__all__ = ['User', 'Supplier', 'Order']
